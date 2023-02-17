from multiprocessing import Pipe
from myutils.DateAndTime import clock
from route.common import format_result_with_pos, get_pos_contents
# 2、定义client用于访问子进程中的服务Process
class OCRRequestProcess:
    def __init__(self,**kwargs):
        self.server_end_conn,self.client_end_conn = Pipe()
        # 开一个守护进程来作为服务，运行在整个程序期间
        from model.OCRServer import POCRServerProcess  # ,getOCRInfoWithInference
        self.p = POCRServerProcess(self.server_end_conn,'anne')
        #一定要在p.start()前设置,设置p为守护进程,禁止p创建子进程,并且父进程代码执行结束,p即终止运行
        self.p.daemon=True
        # if not self.p.is_alive():
        self.p.start()
    # 发送图片并获取ocr结果
    @clock
    def ocr(self,cv2_img):
        cv2_img_c = cv2_img.copy()
        # ocr方法支持 传一个图片列表进行批量识别，所以返回的[result1,result2.....]
        # 所以注意单个图片时也是一个[result],目前应用都是一个图片，所以下面结果直接取returnResult[0]
        # 后面根据需要，再使用批量图片上传的功能
        self.client_end_conn.send((cv2_img_c,'ocr',None))
        returnResult = self.client_end_conn.recv()
        returnResult = [str(line[1][0]) if len(line)>0 else '' for line in returnResult[0]]
        # time.sleep(10)  # 制造阻塞
        return cv2_img_c,returnResult
    # 发送图片并获取ocr结果
    @clock
    def ocr_structure(self,cv2_img):
        cv2_img_c = cv2_img.copy()
        #注意：send()和recv()方法使用pickle模块对对象进行序列化
        self.client_end_conn.send((cv2_img_c,'structure',True))
        result = self.client_end_conn.recv()
        #先按y方向排序 在x方向排序 lambda x, y: f"{str(x) if x is not None else ''} {str(y) if y is not None else ''}", row.values.tolist()
        result_sorted = sorted(result,key=lambda x:(x["bbox"][1],x["bbox"][0]))
        result_pos_content = []
        html_content = []
        # 为了打印看输出结构信息
        # print("-----------")
        # for oneitem in result:
        #     oneitem.pop("img")
        #     oneitem['res'].pop('cell_bbox')
        #     print(f'result--oneitem{oneitem}')
        # for oneitem in result_sorted:
        #     print(f'result_sorted--oneitem{oneitem}')
        result_pd = []
        # ocr_content_tmp = None
        for region in result_sorted:
            # 清理下数据减少内存
            region.pop("img")
            if region['type'].lower() == 'table' and len(region['res']) > 0 and 'html' in region['res']:
                # 清理下数据减少内存
                region['res'].pop('cell_bbox')
                # print("structure-table识别的原始信息：：")
                # print(region)
                # **2假设一个图片文档，遇到表格table时，把之前的非表格内容做一个格式化，并装到结果pd里
                if result_pos_content:
                    content_list = list(zip(*result_pos_content))[2]
                    # 去重，并恢复原来顺序
                    content_list = sorted(set(content_list),key=content_list.index)
                    result_pd.append('\n'.join(content_list))
                    result_pos_content.clear()
                result_pd.append(format_result_with_pos(get_pos_contents(region['res'],from_source = "structure-table",draw_img = cv2_img_c,table_pos = region['bbox'])))
                html_content.append(region['res']['html'])
            else:
                # print("structure识别的原始信息：：")
                # print(region)   
                # if ocr_content_tmp != ocr_content:
                #**2
                result_pos_content.extend(get_pos_contents(region['res'],from_source = "structure",draw_img = cv2_img_c))
                #**1
                # result_pd.append(get_pos_contents(region['res'],from_source = "structure",draw_img = cv2_img_c)[0][2])
        #**2剩余的非表格内容统一装到结果pd里
        if result_pos_content:
            content_list = list(zip(*result_pos_content))[2]
            # 去重，并恢复原来顺序
            content_list = sorted(set(content_list),key=content_list.index)
            result_pd.append('\n'.join(content_list))
        #**1 TypeError: unhashable type: 'DataFrame'
        # result_pd = sorted(set(result_pd),key=result_pd.index)
        return cv2_img_c,result_pd,html_content