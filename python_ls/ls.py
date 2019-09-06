"""
Version: Python3.7
Author: OniOn
Site: http://www.cnblogs.com/TM0831/
Time: 2019/9/6 21:41
"""
import os
import time
import argparse
import terminaltables


def get(path):
    """
    获取指定路径下的内容
    :param path: 路径
    :return:
    """
    if os.path.isdir(path):  # 判断是否是真实路径
        files = os.listdir(path)
        return files
    else:
        print("No such file or directory")
        exit()


def get_all(path):
    """
    获取指定路径下的全部内容
    :param path: 路径
    :return:
    """
    if os.path.isdir(path):
        files = [".", ".."] + os.listdir(path)
        return files
    else:
        print("No such file or directory")
        exit()


def check_arg(data):
    """
    检查参数信息
    :param data: 命令行参数（dict）
    :return:
    """
    assert type(data) == dict
    if not data["path"]:
        data["path"] = "."
    # a参数
    if data["a"]:
        files = get_all(data["path"])
    else:
        files = get(data["path"])
    # r参数
    if data["r"]:
        files = files[::-1]
    # t参数
    if data["t"]:
        files = sorted(files, key=lambda x: os.stat(x).st_mtime)
        for i in range(len(files)):
            files[i] = [files[i], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(files[i]).st_mtime))]
    # l参数
    if data["l"]:
        result = []
        for i in range(len(files)):
            file = files[i][0] if data["t"] else files[i]
            # 获取文件信息
            file_info = os.stat(file)
            # k参数
            if data["k"]:
                # 格式化时间，文件大小用KB表示
                result.append([file, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_info.st_ctime)),
                               "%.3f KB" % (file_info.st_size / 1024)])
            else:
                # 格式化时间，文件大小用B表示
                result.append([file, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_info.st_ctime)),
                               "{} Byte".format(file_info.st_size)])
        if data["t"]:
            for i in result:
                i.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(i[0]).st_mtime)))

        show_file(result, True, True) if data["t"] else show_file(result, True, False)
        return
    show_file(files, False, True) if data["t"] else show_file(files, False, False)


def show_file(files, has_l, has_t):
    """
    格式化输出文件信息
    :param files: 文件列表
    :param has_l: 是否有l参数
    :param has_t: 是否有t参数
    :return:
    """
    # 根据参数信息设置表头
    if not has_l:
        if not has_t:
            table_data = [["ID", "FILE_NAME"]]
            for i in range(len(files)):
                table_data.append([i + 1, files[i]])
        else:
            table_data = [["ID", "FILE_NAME", "FILE_MTIME"]]
            for i in range(len(files)):
                table_data.append([i + 1] + files[i])
    else:
        if not has_t:
            table_data = [["ID", "FILE_NAME", "FILE_CTIME", "FILE_SIZE"]]
        else:
            table_data = [["ID", "FILE_NAME", "FILE_CTIME", "FILE_SIZE", "FILE_MTIME"]]
        for i in range(len(files)):
            table_data.append([i + 1] + files[i])

    # 创建AsciiTable对象
    table = terminaltables.AsciiTable(table_data)
    # 设置标题
    table.title = "file table"
    for i in range(len(table.column_widths)):
        if i != 1:
            # 居中显示
            table.justify_columns[i] = "center"
    print(table.table)


def main():
    """
    主函数，设置和接收命令行参数，并根据参数调用相应方法
    :return:
    """
    # 创建解析器
    parse = argparse.ArgumentParser(description="Python_ls")
    # 可选参数
    parse.add_argument("-a", "-all", help="Show all files", action="store_true", required=False)
    parse.add_argument("-l", "-long", help="View in long format", action="store_true", required=False)
    parse.add_argument("-k", help="Expressed in bytes", action="store_true", required=False)
    parse.add_argument("-r", "-reverse", help="In reverse order", action="store_true", required=False)
    parse.add_argument("-t", help="Sort by modified time", action="store_true", required=False)
    parse.add_argument("-V", "-Version", help="Get the version", action="store_true", required=False)
    # 位置参数
    parse.add_argument("path", type=str, help="The path", nargs="?")

    # 命令行参数信息
    data = vars(parse.parse_args())
    assert type(data) == dict
    if data["V"]:
        print("Python_ls version: 1.0")
        return
    else:
        check_arg(data)


if __name__ == '__main__':
    main()