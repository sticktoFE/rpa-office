import numpy as np
import fitz  # fitz就是pip install PyMuPDF
from  pathlib import Path
from myutils.office_tools import merge_excel
from route.OCRRequest import OCRRequest
# 3. PDF批量转图片
## 在pdf目录下,通过批量将这些PDF文件的每一页解析并转存成图片，做好下一步的识别准备。
class OCRPDF():
    def __init__(self):
        self.ocr_request = OCRRequest()

    # 1、先把pdf拆成一个个图片
    # 2、利用模型识别图片相应内容
    # 1、PDF批量转成图片
    # 在pdf目录下,通过批量将这些PDF文件的每一页解析并转存成图片，做好下一步的识别准备。
    def split_pdf_pic(self, pdfPath):
        self.info_path = pdfPath.parent / pdfPath.stem
        self.info_path.mkdir(exist_ok=True)
        pdfDoc = fitz.open(pdfPath)
        # 每个尺寸的缩放系数为4，这将为我们生成分辨率提高4的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            # 注意，设置过大，可能导致图片识别不出来，因为分辨率变大，里面的内容会变模糊
            # 如发现有图片识别不出来，可调小这两个参数
        # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_x = 3
        zoom_y = 3
        rotate = 0
        for page in pdfDoc.pages():
            mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            # 将图片写入指定的文件夹内,调试用，可注释掉
            # pix.save(self.info_path/f'page_{page.number+1}.png')  
            img_bytes = pix.pil_tobytes(format="png", optimize=True) #pillow格式的字节组
            img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n) #np格式
            self.ocr_request.infopic_info_save(img_np,self.info_path,f'page_{page.number+1}')
        merge_excel(self.info_path)
    # 遍历filepath下所有pdf文件，转换成图片并保存到imgs下的对应子目录下
    def split_pdfs_pic(self, pdfdirpath: Path):
        # 遍历filepath下所有文件
        # files = os.listdir(filepath)
        # glob指当前目录下所有的pdf文件，如果包括子目录，应为 rglob('*.pdf')
        for file in pdfdirpath.glob('*.pdf'):
            # 将转换的图片保存到对应imgs的对应子目录下
            self.split_pdf_pic(file)
            
if __name__ == '__main__':
    from  pathlib import Path 
    # import sys
    parent_dir = Path(__file__).parent
    # print(parent_dir)
    # sys.path.append(parent_dir.parent)
    # 遍历PDF文件并转换图片
    pdfocr = OCRPDF()
    pdfDir = parent_dir/'report'
    pdfocr.split_pdfs_pic(pdfDir)
