import argparse
import os.path


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
    return param, file_path


def get_appends(file):
    with open(file, 'r') as f:
        data = f.read()
    empty = 0
    code = 0
    annotation = 0
    is_annotation = False
    for line in data.split('\n'):
        if is_annotation:
            annotation = annotation + 1
            if '*/' in line:
                is_annotation = False
            continue
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


def get_chars(file):
    with open(file, 'r') as f:
        data = f.read()
        print("文件（" + file + "）的字符数： " + str(len(data)))


def get_words(file):
    with open(file, 'r') as f:
        data = f.read()
        print("文件（" + file + "）的词的数目： " + str(len(data.split())))


def get_lines(file):
    with open(file, 'r') as f:
        data = f.read()
        print("文件（" + file + "）的行数： " + str(len(data.split("\n"))))


def get_file_by_dir(root, suffix):
    file_list = []
    dir_list = os.listdir(root)
    for i in range(len(dir_list)):
        path = os.path.join(root, dir_list[i])
        if os.path.isdir(path):
            file_list.extend(get_file_by_dir(path, suffix))
        else:
            if suffix == '':
                file_list.append(path)
            else:
                if '.' in path and path.split('.')[1] == suffix:
                    file_list.append(path)
    return file_list


def main():
    param, file_path = command_parse()
    # 判断是否需要返回更复杂的数据
    append = False
    if 'a' in param:
        append = True
    # 如果输入的是目录的路径
    if 's' in param:
        # 如果有通配符，识别后缀
        suffix = ''
        if '*.' in file_path:
            suffix = file_path.split('*.')[1]
            file_path = file_path.split('\*.')[0]
        # 判断路径是否是目录的路径
        if not os.path.isdir(file_path):
            print("输入的路径不是目录！")
            print("ERROR: " + file_path)
            exit()
        # 递归遍历子目录中所有符合条件的文件
        file_list = get_file_by_dir(file_path, suffix)
        for file in file_list:
            if 'c' in param:
                get_chars(file)
            if 'w' in param:
                get_words(file)
            if 'l' in param:
                get_lines(file)
            if 'a' in param:
                get_appends(file)
    # 如果输入的是文件的路径
    else:
        # 判断路径是否是文件的路径
        if not os.path.isfile(file_path):
            print("输入的路径不是文件！")
            print("ERROR: " + file_path)
            exit()
        if 'c' in param:
            get_chars(file_path)
        if 'w' in param:
            get_words(file_path)
        if 'l' in param:
            get_lines(file_path)
        if 'a' in param:
            get_appends(file_path)


if __name__ == '__main__':
    main()
