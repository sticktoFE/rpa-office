import pandas as pd
import numpy as np
from openpyxl.utils import get_column_letter
import xlwings as xw
from pathlib import Path

"""DataFrame保存为excel并自动设置列宽"""
# 导出excel时，里面内容统一宽度导致很多内容显示不出来，此处解决自动根据内容自动调整宽度功能
# 把多个excel合并到一个excel中
def to_excel_auto_column_weight(pd_list: dict, file_name):
    with pd.ExcelWriter(file_name) as excel_writer:
        for sheet_name, df in pd_list.items():
            # 数据 to 写入器，并指定sheet名称，不输出索引
            df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
            # 计算每列表头的字符宽度
            column_widths = (
                df.columns.to_series()
                .apply(lambda x: len(str(x).encode("utf-8")))
                .values
            )
            # 计算每列的最大字符宽度
            max_widths = (
                df.astype(str)
                .applymap(lambda x: len(str(x).encode("utf-8")))
                .agg(max)
                .values
            )
            # 取前两者中每列的最大宽度
            widths = np.max([column_widths, max_widths], axis=0)
            # 指定sheet，设置该sheet的每列列宽
            worksheet = excel_writer.sheets[sheet_name]
            for i, width in enumerate(widths, 1):
                # openpyxl引擎设置字符宽度时会缩水0.5左右个字符，所以干脆+2使左右都空出一个字宽。
                worksheet.column_dimensions[get_column_letter(i)].width = width + 2


def excel_auto_column_weight(excel_path):
    app = xw.App(visible=False, add_book=False)  # visible运行中是否展示excel
    wb = app.books.open(excel_path)
    # sht = wb.sheets.active
    for sheet in wb.sheets:  # loop through `dict` of dataframes
        """设置单元格大小"""
        sheet.autofit()  # 自动调整单元格大小。
        # sheet.range('a1:d50').column_width = 5    # 设置第1-4列的列宽。
        # sheet.range(1,4).row_height = 20     # 设置第1行 4行高。
    wb.save()
    wb.close()
    app.quit()


# 合并多个excel到一个excel
def merge_excel(source_excel_dir: Path, pupose_excel_name="merge_excel.xlsx"):
    excel_result = {}
    # glob指当前目录下所有的excel文件，如果包括子目录，应为 rglob('*.pdf')
    for file in source_excel_dir.glob("*.xlsx"):
        excel_result[file.stem] = pd.read_excel(file)
        # 删除此文件
        file.unlink()
    # 将转换的图片保存到对应imgs的对应子目录下
    pupose_excel_path = source_excel_dir / pupose_excel_name
    # 文件存在需先删掉
    if pupose_excel_path.exists():
        pupose_excel_path.unlink()
    to_excel_auto_column_weight(excel_result, pupose_excel_path)


def convert_to_number(letter, columnA=0):
    """
    字母列号转数字
    columnA: 你希望A列是第几列(0 or 1)? 默认0
    return: int
    """
    ab = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letter0 = letter.upper()
    w = 0
    for _ in letter0:
        w *= 26
        w += ab.find(_)
    return w - 1 + columnA


def convert_to_letter(number, columnA=0):
    """
    数字转字母列号
    columnA: 你希望A列是第几列(0 or 1)? 默认0
    return: str in upper case
    """
    ab = "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n = number - columnA
    x = n % 26
    if n >= 26:
        n = int(n / 26)
        return convert_to_letter(n, 1) + ab[x + 1]
    else:
        return ab[x + 1]
