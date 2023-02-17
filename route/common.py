
import cv2
import pandas as pd
# 设置 pd数据打印格式，为了保证排列整齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width',200)# 设置打印宽度（**重要**）
pd.set_option('expand_frame_repr',False) #数据超过总宽度后，是否折叠显示    
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)           
""" 
    这个从横向、纵向尽量保持识别对象的原貌结构，要用这个
    structure-table out_info输入数据结构
        {"boxes": [[[557.0, 15.0], [592.0, 15.0], [592.0, 52.0], [557.0, 52.0]],
                [[222.0, 18.0], [309.0, 18.0], [309.0, 51.0], [222.0, 51.0]], ...]], 
            "rec_res": [["指", 0.6355153918266296], ["释义项", 0.8654652237892151],... ], 
            "html": "<html><body><table><thead><tr><td>释义项</td><td>指</td><td>释义内容</td></tr></thead><tbody><tr><td>中国证监会、证监会</td><td>指</td><td>中国证券监督管理委员会</td></tr><tr><td>深交所、交易所</td><td>指</td><td>深圳证券交易所</td></tr><tr><td>公司、本公司、我公司或国农科技</td><td>指</td><td>深圳中国农大科技股份有限公司</td></tr><tr><td>中农大投资</td><td>指</td><td>深圳中农大科技投资有限公司</td></tr><tr><td>深圳国科投资、国科投资、深圳国科</td><td>指</td><td>深圳国科投资有限公司</td></tr><tr><td>国科互娱、广州国科、广州互娱</td><td>指</td><td>广州国科互娱网络科技有限公司</td></tr><tr><td>火舞软件</td><td>指</td><td>广州火舞软件开发股份有限公司</td></tr><tr><td>山东华泰</td><td>指</td><td>山东北大高科华泰制药有限公司</td></tr><tr><td>报告期</td><td>指</td><td>2018年1月1日-2018年12月31日</td></tr></table></body></html>"}}
        Returns:
            _type_: _description_
"""
def get_pos_contents(out_info, from_source="ocr", draw_img = None,table_pos =[0,0,0,0]):
    # sourcery skip: default-mutable-arg
    temp_list = []
    left_top_x = 0
    left_top_y = 0
    right_bottom_x = 0
    right_bottom_y = 0
    ocr_content = None
    # table情况下，位置信息是一个 二维数组，每个元素都是一个格子的上左，上右，下右，下左的坐标
    info_list = out_info["boxes"] if from_source == "structure-table" else out_info
    # 1、以左上角坐标为准，把识别的内容通过y方向归类到每一行里，每一行做一下x方向的排序
    # info_list是一个字典列表
    for i,one_item in enumerate(info_list):
        if from_source == "ocr":
            left_top_x = one_item[0][0][0]
            left_top_y = one_item[0][0][1]
            right_bottom_x = one_item[0][2][0]
            right_bottom_y = one_item[0][2][1]
            ocr_content = one_item[1][0]
        elif from_source == "structure":
            left_top_x = one_item["text_region"][0][0]
            left_top_y = one_item["text_region"][0][1]
            right_bottom_x = one_item["text_region"][2][0]
            right_bottom_y = one_item["text_region"][2][1]
            ocr_content = one_item["text"]
        elif from_source == "structure-table":
            left_top_x = one_item[0]
            left_top_y = one_item[1]
            right_bottom_x = one_item[2]
            right_bottom_y = one_item[3]
            # 上面坐标识别的是全部table的cell，但内容如果为空，下面就没有了，需要做个判断
            # 必须 return_ocr_result_in_table=True 才会有rec_res
            ocr_content = out_info["rec_res"][i][0] if i < len(out_info["rec_res"]) else " "
        # 对识别的图片区域通过画矩形标识出来
        if draw_img is not None:
            # paddle自带的画矩形，以下两种方法，1是在右边显示识别的文字，而不是在文字上直接显示识别框，体验不好，2因为识别为Figure,不显示识别框
            # 所以重新设计，也不困难
            # 1、先用这种方式，这个识别框和图片没有合二为一，略显不足
            # font_path = 'PaddleOCR/doc/fonts/simfang.ttf' # PaddleOCR下提供字体包
            # im_show = draw_structure_result(cv2_img, result,font_path=font_path)
            # 2、本想在图片上实时显示识别的文字内容，可模型识别为图片 暂时先这样吧
            # cv2_img12 = cv2_img[..., ::-1]
            # layout_res = self.ocr_structure_sys.table_layout.detect(cv2_img12)
            # # im_show = lp.draw_box(cv2_img12, layout_res, box_width=5, show_element_type=True,show_element_id=True)
            # im_show = pil2cv(im_show)
            # 图片对象，左上角坐标，右下角坐标，颜色，宽度
            cv2.rectangle(draw_img,(int(left_top_x+table_pos[0]), int(left_top_y+table_pos[1])),(int(right_bottom_x+table_pos[0]), int(right_bottom_y+table_pos[1])),(255,0,i),2)
        # 把获取的内容装配到list,structure模型存在 类型为 title和figure 时，内容一样的情况，
        # 此处根据内容进行过滤，免得前台展示时重复 
        temp_list.append([left_top_x,left_top_y,ocr_content])
    return temp_list
""" 
    对识别结果进行格式化调整
"""  
def format_result_with_pos(temp_list):
    line_dict = {}
    temp_y = 0
    # 最终生成一个以横坐标x值（合并后的）为列名的空PD
    result_pd,final_column_dict = get_x_code_value(temp_list)
    # 按照列名，把每一个识别块儿形成dict,并添加到上面的PD中
    #  先对temp_list 按left_top_y进行正序排列
    for i,one_item in enumerate(temp_list):
        left_top_x = one_item[0]
        left_top_y = one_item[1]
        ocr_content = one_item[2]
        # 认为两个文字块儿的左上角坐标y值相差不超过6，认为是一行的
        if i != 0 and abs(left_top_y - temp_y) >= 10:
            result_pd = result_pd.append(line_dict.copy(),ignore_index=True)
            # 新的一行开始入列表
            line_dict.clear()
        column_id = final_column_dict[left_top_x]
        if column_id in line_dict:
            line_dict[column_id] = line_dict[column_id] + ocr_content
        else:
            line_dict[column_id] = ocr_content
        # 识别的一个文字块儿的左上角的坐标的y值
        temp_y = left_top_y
        # 循环到最后一个元素时，添加进去，不能遗漏了
        if i == len(temp_list)-1:
            result_pd = result_pd.append(line_dict,ignore_index=True)
    # source_pd = source_pd.drop(source_pd.index[0])
    result_pd = result_pd.fillna('')
    return result_pd #result_pd.values.tolist()
# 为x坐标建立粗粒度的编码值
# 在x坐标这个维度的列表，很多值比较接近，视为在一列，进行合并
# 形式为 {x1= x1,x2=x1,x3= x2,x4=x2。。。}
def get_x_code_value(temp_list):
    # 识别出全部的不重复的x坐标值
    column_set = {source[0] for source in temp_list}  #{}表示set
    column_set = sorted(column_set)
    final_column_dict ={}
    x_code_value = 0
    for i,value in enumerate(column_set):
        # 阈值代表着超过这个值就分成两个列
        # 在分辨率一样情况下 阈值越小越容易把两个值分成两列
        # 阈值一样情况下，分辨率越大越容易把两个值分成两列
        if i == 0 or abs(value - x_code_value) >= 40:
            x_code_value = value
        final_column_dict[value] = x_code_value
    # 最终生成一个以横坐标x值（合并后的）为列名的空PD
    return pd.DataFrame(columns= sorted(set(final_column_dict.values()))),final_column_dict #set具有顺序随机性，所以要相比上面再排一次序