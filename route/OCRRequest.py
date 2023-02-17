import json
from copy import deepcopy
import cv2
from docx import Document, shared
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from paddleocr.ppocr.utils.logging import get_logger
from paddleocr.ppstructure.recovery.recovery_to_doc import sorted_layout_boxes
from paddleocr.ppstructure.recovery.table_process import HtmlToDocx
from paddleocr.ppstructure.table.predict_table import to_excel
from myutils.DateAndTime import clock

logger = get_logger()


# 1、正常线程调用
class OCRRequest:
    def __init__(self,output="../output",**kwargs):
        from model.OCRServer import POCRServer
        self.ocr_server = POCRServer()
        self.output = output
    def set_output_filepath(self,output):
        self.output = output
    # keep_format 0表示返回模型原始识别信息，1返回识别到的字符串列表 2返回的内容保持和识别的对象布局一致
    @clock
    def upload_ocr_thread(self, cv2_img, keep_format="0"):
        # print(f"OCRRequest in  {QThread.currentThread()}线程中")
        cv2_img_c = cv2_img.copy()
        returnResult = self.ocr_server.ocr(cv2_img_c)
        # 如果不保持图片原始布局，就只要识别的内容
        if keep_format =="1":
            returnResult = [str(line[1][0]) for line in returnResult]
        if keep_format =="2":
            returnResult = keep_source_contents_align(returnResult,from_source = "ocr",draw_img = cv2_img_c)
        # time.sleep(10)  # 制造阻塞
        return cv2_img_c,returnResult
        # 把图片识别出内容,组合成有效信息返回
    @clock
    def upload_ocr_structure_thread(self, oneimg, keep_format="2",only_layout=False,):
        return_result = []
        html_content = []
        # oneimg = np.ascontiguousarray(oneimg)
        # draw_img = cv2.UMat(draw_img).get()
        oneimg_c = oneimg.copy()
        if only_layout:
            return_result = self.ocr_server.ocr_structure(oneimg_c,only_layout=only_layout)
            print(return_result)
            return oneimg_c,return_result,html_content
        result = self.ocr_server.ocr_structure(oneimg_c,return_ocr_result_in_table=True)
        # 由于识别的结果 可能顺序乱了，要做个排序
        result.sort(key=lambda x:(x["bbox"][1],x["bbox"][0])) #先按y方向排序 在x方向排序
        # 结构化输出 
        if keep_format =="0":
            return_result = result
        elif keep_format =="2":
            for region in result:
                if region['type'].lower() == 'table' and len(region['res']) > 0 and 'html' in region['res']:
                    return_result.extend(keep_source_contents_align(region['res'],from_source = "structure-table",draw_img = oneimg_c))
                    html_content.append(region['res']['html'])
                else:    
                    return_result.extend(keep_source_contents_align(region['res'],from_source = "structure",draw_img = oneimg_c))
        return oneimg_c,return_result,html_content

    # 把图片识别出内容,并保存到相应目录
    # 1、保存在每张图片对应的子目录下,
        # 仿照save_structure_res逻辑重写，理由是，这个方法是一个图片一个目录来存放结果报文、excel、figure,
        # 而重新定义的是一个图片相关信息通过文件名目录来体现信息来自同一图片，所有信息都放在同一目录info_dir下，就这点区别
        # 2、仿照convert_info_docx重写版面恢复成word逻辑，一则里面的逻辑基于save_structure_res，二则为了减少迭代识别res
        #的迭代次数
    def infopic_info_save(self, oneimg, info_dir, info_filename_prefix, save_pdf=False):
        oneimg_c = oneimg.copy()
        # _, result, _ = self.upload_ocr_structure_thread(oneimg_c, keep_format="0")
        result = self.ocr_server.ocr_structure(oneimg_c,return_ocr_result_in_table=True)
        # 版面恢复
        # save_structure_res(result, self.output, '.')
        # for line in result:
        #     line.pop('img')
        #     print(line)
        h, w, _ = oneimg_c.shape
        res = sorted_layout_boxes(result, w)
        res_cp = deepcopy(res)
        # for word
        doc = Document()
        doc.styles['Normal'].font.name = 'Times New Roman'
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        doc.styles['Normal'].font.size = shared.Pt(6.5)
        flag = 1
        with open(info_dir.joinpath(f'{info_filename_prefix}_res.txt'), 'w', encoding='utf-8') as f:
            for region in res_cp:
                # for word begin
                if flag == 2 and region['layout'] == 'single':
                    section = doc.add_section(WD_SECTION.CONTINUOUS)
                    section._sectPr.xpath('./w:cols')[0].set(qn('w:num'), '1')
                    flag = 1
                elif flag == 1 and region['layout'] == 'double':
                    section = doc.add_section(WD_SECTION.CONTINUOUS)
                    section._sectPr.xpath('./w:cols')[0].set(qn('w:num'), '2')
                    flag = 2
                # for word end
                roi_img = region.pop('img')
                pic_fig_region = ".".join([str(i) for i in region["bbox"]])
                if region['type'].lower() == 'table' and len(region['res']) > 0 and 'html' in region['res']:
                    # 表格图片区域--下面尽管变量没用但需要pop,否则因为存在ndarray,f.write(..这一句会报错
                    region['res'].pop('boxes')
                    # table_img = region['res'].pop('boxes')
                    # 表格转化成exce
                    excel_path = info_dir.joinpath(f'{info_filename_prefix}_{pic_fig_region}.xlsx')
                    to_excel(region['res']['html'], excel_path)
                    # for word
                    paragraph = doc.add_paragraph()
                    new_parser = HtmlToDocx()
                    new_parser.table_style = 'TableGrid'
                    table = new_parser.handle_table(html=region['res']['html'])
                    new_table = deepcopy(table)
                    new_table.alignment = WD_TABLE_ALIGNMENT.CENTER
                    paragraph.add_run().element.addnext(new_table._tbl)
                elif region['type'].lower() == 'figure':
                    img_path = info_dir.joinpath(f'{info_filename_prefix}_{pic_fig_region}.jpg')
                    cv2.imencode(".jpg", roi_img)[1].tofile(img_path)
                    # for word
                    paragraph_pic = doc.add_paragraph()
                    paragraph_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = paragraph_pic.add_run("")
                    if flag == 1:
                        run.add_picture(str(img_path), width=shared.Inches(5))
                    elif flag == 2:
                        run.add_picture(str(img_path), width=shared.Inches(2))
                elif region['type'].lower() == 'title':
                    doc.add_heading(region['res'][0]['text'])
                else:
                    paragraph = doc.add_paragraph()
                    paragraph_format = paragraph.paragraph_format
                    for i, line in enumerate(region['res']):
                        if i == 0:
                            paragraph_format.first_line_indent = shared.Inches(0.25)
                        text_run = paragraph.add_run(line['text'] + ' ')
                        text_run.font.size = shared.Pt(10)
                # 最后把整个信息保存到文件中，ensure_ascii=False是为了避免像中文中这种“\u51fa\u751f\u5730”ASCII编码
                f.write(f'{json.dumps(region, ensure_ascii=False)}\n')
        # save to docx
        docx_path = info_dir.joinpath(f'{info_filename_prefix}_word.docx')
        doc.save(docx_path)
        logger.info(f'docx save to {docx_path}')
        # save to pdf
        if save_pdf:
            pdf_path = info_dir.joinpath(f'{info_filename_prefix}_pdf.pdf')
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            logger.info(f'pdf save to {pdf_path}')
        return result, oneimg

"""
    其他脚本直接引用此实例化的对象可以实现单例模型，除非特别需要单独实例化，
    可以一直引用此对象，保证整个程序只有一个实例，节约系统资源,不用轻易实例化
    上面实例，如果后期需要多线程，再思考多实例问题
"""
# ocr_request = OCRRequest() 

# ocr_request_process = OCRRequestProcess()    
 
# if __name__ == '__main__':
# ocr = PaddleOCR(use_angle_cls=True, lang='ch') # need to run only once to download and load model into memory
# img_path = os.path.join(dirName,'01.png')
# result = ocr.ocr(img_path, cls=True)
# for line in result:
#     print(line)
