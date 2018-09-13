import argparse
import os.path
import re
import time


# 解析命令行参数
def command_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', default=False, help='计算文件的字符数')
    parser.add_argument('-w', action='store_true', default=False, help='计算文件词的数目')
    parser.add_argument('-l', action='store_true', default=False, help='计算文件的行数')
    parser.add_argument('-s', action='store_true', default=False, help='递归处理目录下符合条件的文件')
    parser.add_argument('-a', action='store_true', default=False, help='返回更复杂的数据（代码行 / 空行 / 注释行）')
    parser.add_argument(action="store", dest="file")
    args = parser.parse_args()
    file_path = args.file
    # 通过往字符串中加入各操作的字母传递信息
    param = ''
    if args.c:
        param = param + 'c'
    if args.w:
        param = param + 'w'
    if args.l:
        param = param + 'l'
    if args.s:
        param = param + 's'
    if args.a:
        param = param + 'a'
    # 如果输入的是相对路径，自动补充当前路径
    if "\\" not in file_path:
        file_path = os.path.abspath(os.path.join(os.getcwd(), "..")) + "\\" + file_path
    return param, file_path


def get_chars(file):
    with open(file, 'r', encoding='UTF-8') as f:
        data = f.read()
        print("文件（" + file + "）的字符数： " + str(len(data)))


def get_words(file):
    with open(file, 'r', encoding='UTF-8') as f:
        data = f.read()
        # 将所有不是英文的字符replace成空格，使用split查询list长度即可
        data = re.sub('[^a-zA-Z]', ' ', data)
        print("文件（" + file + "）的词的数目： " + str(len(data.split())))


def get_lines(file):
    with open(file, 'r', encoding='UTF-8') as f:
        data = f.read()
        print("文件（" + file + "）的行数： " + str(len(data.split("\n"))))


def get_appends(file):
    with open(file, 'r', encoding='UTF-8') as f:
        data = f.read()
    empty = 0
    code = 0
    annotation = 0
    # 标识多行注释
    is_annotation = False
    for line in data.split('\n'):
        if is_annotation:
            annotation = annotation + 1
            if '*/' in line:
                is_annotation = False
            continue
            # 去除空格等无用字符
        visual_line = line.replace('\t', '').replace(' ', '')
        if len(visual_line) < 2:
            empty = empty + 1
        elif '/*' in visual_line:
            annotation = annotation + 1
            is_annotation = True
        elif '//' in visual_line:
            annotation = annotation + 1
        else:
            code = code + 1
    print("文件（" + file + "）的空行数： " + str(empty))
    print("文件（" + file + "）的代码行数： " + str(code))
    print("文件（" + file + "）的注释行数： " + str(annotation))


# 通过正则表达式递归查找文件
def get_file_recursive(root, pattern):
    file_list = []
    dir_list = os.listdir(root)
    for i in range(len(dir_list)):
        path = os.path.join(root, dir_list[i])
        if os.path.isdir(path):
            file_list.extend(get_file_recursive(path, pattern))
        elif os.path.isfile(path) and re.match(pattern, dir_list[i]):
            file_list.append(path)
    return file_list


# 通过正则表达式不递归查找文件
def get_file(root, pattern):
    file_list = []
    dir_list = os.listdir(root)
    for i in range(len(dir_list)):
        path = os.path.join(root, dir_list[i])
        if os.path.isfile(path) and re.match(pattern, dir_list[i]):
            file_list.append(path)
    return file_list


def main():
    param, file_path = command_parse()
    # 如果输入的是目录的路径
    if 's' in param:
        # 如果有通配符,识别符合的目录,返回符合的文件路径
        if "*" in file_path or "?" in file_path:
            pattern = r"^" + file_path.split("\\")[-1].replace("*", "[0-9a-zA-Z]*").replace("?", "[0-9a-zA-Z]*") + "$"
            # 获取根路径
            root = os.path.abspath(os.path.join(file_path, ".."))
            file_list = get_file_recursive(root, pattern)
        # 没有通配符，先检测路径是否正确，然后递归
        else:
            if not os.path.isdir(file_path):
                print("输入的路径不是目录！")
                print("ERROR: " + file_path)
                exit()
            # 无通配符，匹配任意字符
            file_list = get_file_recursive(file_path, "[\s\S]*")
    # 如果输入的是文件的路径
    else:
        file_list = []
        if "*" in file_path or "?" in file_path:
            pattern = r"^" + file_path.split("\\")[-1].replace("*", "[0-9a-zA-Z]*").replace("?", "[0-9a-zA-Z]*") + "$"
            # 获取根路径
            root = os.path.abspath(os.path.join(file_path, ".."))
            file_list = get_file(root, pattern)
        else:
            # 判断路径是否是文件的路径
            if not os.path.isfile(file_path):
                print("输入的路径不是文件！")
                print("ERROR: " + file_path)
                exit()
            file_list.append(file_path)
    for file in file_list:
        if 'c' in param:
            get_chars(file)
        if 'w' in param:
            get_words(file)
        if 'l' in param:
            get_lines(file)
        if 'a' in param:
            get_appends(file)


if __name__ == '__main__':
    pretime = time.time()
    main()
    print("处理完成！共使用：" + str(time.time() - pretime) + "秒")
