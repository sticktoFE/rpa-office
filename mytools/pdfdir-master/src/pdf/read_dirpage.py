from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path 
# 每个书签的索引格式
# {'/Title': '书签名', '/Page': '指向的目标页数', '/Type': '类型'}

directory_str = ""

def bookmark_listhandler(list):
    global directory_str
    for message in list:
        if isinstance(message, dict):
            directory_str += message["/Title"] + "\n"
            print(message['/Title'])
        else:
            bookmark_listhandler(message)

readFile = f"{Path(__file__).parent}/统计学习方法.pdf"

def handlePDF2():
    with open(readFile, "rb") as f: #也可直接PdfFileReader(readFile)
        pdfFileReader = PdfFileReader(f)
        # 检索文档中存在的文本大纲,返回的对象是一个嵌套的列表
        text_outline_list = pdfFileReader.getOutlines()
        print('********')
        # print(pdf.)
        bookmark_listhandler(text_outline_list)
        
        # 获取 PDF 文件的文档信息
        documentInfo = pdfFileReader.get.getDocumentInfo()
        print('documentInfo = %s' % documentInfo)
        # 获取页面布局
        pageLayout = pdfFileReader.getPageLayout()
        print('pageLayout = %s ' % pageLayout)

        # 获取页模式
        pageMode = pdfFileReader.getPageMode()
        print('pageMode = %s' % pageMode)

        xmpMetadata = pdfFileReader.getXmpMetadata()
        print('xmpMetadata = %s ' % xmpMetadata)

        # 获取 pdf 文件页数及内容
        pageCount = pdfFileReader.getNumPages()
        print('pageCount = %s' % pageCount)
        for index in range(0, pageCount):
            # 返回指定页编号的 pageObject
            pageObj = pdfFileReader.getPage(index)
            print('index = %d , pageObj = %s' % (index, type(pageObj))) # <class 'PyPDF2.pdf.PageObject'>
            # 获取 pageObject 在 PDF 文档中处于的页码
            pageNumber = pdfFileReader.getPageNumber(pageObj)
            print('pageNumber = %s ' % pageNumber)
            extractedText = pageObj.extractText()
            print(f'pageContent = {extractedText}\n')

        with open(f"{Path(__file__).parent}/统计学习方法目录.txt", "w", encoding="utf-8") as f:
            f.write(directory_str)


# import fitz
# file = 'test.pdf'
# doc = fitz.open(readFile)
# nums = doc._getXrefLength()
# print(nums)
# for i in range(1, nums):
#     # 定义对象字符串
#     text = doc._getXrefString(i)
#     print(i, text)

import fitz
import re
import os

file_path = readFile # PDF 文件路径
dir_path = f"{Path(__file__).parent}/temp" # 存放图片的文件夹

def pdf2image1(path, pic_path):
    checkIM = r"/Subtype(?= */Image)"
    pdf = fitz.open(path)
    lenXREF = pdf._getXrefLength()
    count = 1
    for i in range(1, lenXREF):
        text = pdf.xref_object(i)
        isImage = re.search(checkIM, text)
        if not isImage:
            continue
        pix = fitz.Pixmap(pdf, i)
        new_name = f"img_{count}.png"
        pix.writePNG(os.path.join(pic_path, new_name))
        count += 1
        pix = None

pdf2image1(file_path, dir_path)