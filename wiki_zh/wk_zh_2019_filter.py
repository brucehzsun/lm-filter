import os
import json
import re

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
delete_list = ['《', '》', '（）', "「", "」", '）', '（', '“', '”', '(', ')', '〈', '〉', '-', '{', '}', '"', '·', '|',
               ',', '‧', '[', ']', '*', '#', '%', '±', '℃', ' ', '〇', '．', '……', '=']
replace_map = {'～': '到', '.': "", ':': '', '°': '度', '－': ' '}


def parse_text(text: str):
    ret = []
    for v in text.split("\n\n"):
        v = v.strip()
        if v == '':
            continue
        for value in re.split(r"[，。？?！!：;；/:、／\n]", v):
            value = value.strip()
            # 删除
            for replace in delete_list:
                value = value.replace(replace, "")
            # 替换
            for k, v in replace_map.items():
                value = value.replace(k, v)
            # 去掉1. 2. 3.
            value = re.sub("^\d.", '', value)
            # 是否包含中文字符
            result = zhPattern.search(value)
            if result:
                if (result.end() - result.start()) == 1:
                    continue
            # 全中文情况下去除空格
            result = re.findall(r'[a-zA-Z0-9]+', value)
            if not result:
                value = value.replace(' ', '')
            value = value.strip()
            if len(value) < 3:
                continue
            ret.append(value)
            print(value)
        # if v.startwith("1\")
    return ret


def parse_wk_file(path: str, name: str):
    file_path = os.path.join(path, name)
    print(f"file_path={file_path}")
    ret = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            fcc_data = json.loads(line)
            for key, value in fcc_data.items():
                if key == "id":
                    continue
                elif key == "url":
                    continue
                elif key == "title":
                    print('')
                    result = parse_text(value)
                    ret.extend(result)
                elif key == "text":
                    result = parse_text(value)
                    ret.extend(result)
                else:
                    print(f"unknown key = {key} = > {value}")
                    exit(-1)
    return ret

    # with open(file_path) as file:
    #     while()


def writer_file(result: list, dir_name: str):
    path = os.path.join("data", dir_name + ".txt")
    with open(path, 'w') as f:
        for text in result:
            result = ['<s>']
            for char in text:
                result.append(char)
            result.append('</s>')
            f.write(" ".join(result).strip() + "\n")


def process_text():
    path = "/Users/brucesun/asr-corpus/lm/wiki_zh"
    for dir_name in os.listdir(path):
        if not dir_name.startswith("."):
            for file_name in os.listdir(os.path.join(path, dir_name)):
                result = parse_wk_file(os.path.join(path, dir_name), file_name)
                writer_file(result, dir_name)
                break
            break


if __name__ == '__main__':
    process_text()
    # text = ["爱我中华", '中华人民共和国']
    # writer_file(text, 'test')
