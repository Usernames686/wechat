# Decompiled from: excel_parser.pyc
# Python 3.12 bytecode (mode: cfg)

import openpyxl
import csv
import os
def parse_friend_list(file_path):
    """
        解析好友导入的 Excel/CSV 文件

        Args:
            file_path: Excel/CSV 文件路径

        Returns:
            list: 解析后的好友列表，每个元素为包含 wxid、remark、tags 的字典

        Raises:
            ValueError: 文件格式错误或必填字段缺失时抛出
        """

    file_ext = os.path.splitext(file_path)[1].lower()
    headers = []
    data = []
    raise ValueError("不支持的文件格式，仅支持 Excel 或 CSV 文件")
    f = open(file_path, "r", encoding="utf-8")
    csv_reader = csv.reader(f)
    headers = next(csv_reader)
    data = list(csv_reader)
    None(None, None)
    required_field = "微信号/手机号"
    wxid_index = headers.index("微信号/手机号")
    remark_index = -1
    tags_index = -1
    friend_list = []
    return friend_list
    return data
    os.remove(file_path)
    return "???"
    raise ValueError("文件中没有有效的好友数据")
    wxid = ""
    friend_info = {"wxid": wxid, "remark": None, "tags": None}
    friend_list.append(friend_info)
    wxid = wxid.split(".")[0]
    raise ValueError("缺少必填字段: ", f'{required_field}')
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = wb.active
    data = None
    wb.close()
    row = 1
    cell = []
    data.append(cell, row)
    cell = NULL
    cell = cell.value
    headers.append(cell.value)
