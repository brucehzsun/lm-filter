import os
import json
import re
from utils import number_util

number = '0123456789１２３４５６７８９０'
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
pattern_special = re.compile(r"<.*>")
delete_first = ['<br>', '</br>', '<div>', '</div>']
delete_list = ['《', '》', '（）', "「", "」", '）', '（', '“', '”', '(', ')', '〈', '〉', '-', '–', '{', '}', '"', '·', '|',
               ',', '‧', '[', ']', '*', '#', '%', '±', '℃', ' ', '〇', '．', '……', '=', '&', '『', '』', '˭', '※', '〔 ',
               '【', '】', '+', '™', '®', '・']
replace_map = {'～': '到', '.': "", ':': '', '°': '度', '－': ' ', 'km²': "平方米", "km": "千米", '×': '乘'}


def read_en_dict(path: str):
    en_dict = {}
    with open(path) as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            en_dict[line] = True
    return en_dict


def is_chinese_char(ch: chr):
    return ('\u4e00' <= ch <= '\u9FFF') or ('\uAC00' <= ch <= '\uD7AF') or ('\u3040' <= ch <= '\u31FF')  # 中文 韩文 日文


def add_word_to_list(word: str, output: list, en_dict: dict):
    if not word:
        return

    word = word.strip()
    if word == '':
        return

    if is_chinese_char(word):
        output.append(word)
    elif word.isalpha():
        # 英文
        if en_dict.get(word.lower()):
            output.append(word)
    else:
        output.append(word)


def filter_raw_text(raw_text: str, en_dict: dict):
    result = []
    raw_data = []
    text_list = parse_text(raw_text)
    for text in text_list:
        ret = to_lm_str(text, en_dict)
        if ret is not None:
            result.append(ret)
            raw_data.append(text)
    return result, raw_data


def to_lm_str(text: str, en_dict: dict):
    text = number_util.convert_number(text)

    output = []
    word = ''
    pre_char: chr = None
    for ch in text:
        if is_chinese_char(ch):  # 中文 韩文 日文
            add_word_to_list(word, output, en_dict)
            word = ''
            if not ch.strip() == '':
                output.append(ch)
        elif ch == ' ':  # 空格 区分单词
            add_word_to_list(word, output, en_dict)
            word = ''
        else:  # 标点符号等, 面积147km² => 面 积 147 km²
            if (pre_char is not None) and (pre_char in number) and ch not in number:
                add_word_to_list(word, output, en_dict)
                word = ''
                if not ch.strip() == '':
                    word += ch
            else:
                word += ch
        pre_char = ch
    if word:
        add_word_to_list(word, output, en_dict)

    if len(output) > 1:
        return " ".join(output)
    else:
        return None


def parse_text(text: str):
    for split in delete_first:
        text = text.replace(split, '\n')

    ret = pattern_special.search(text)
    if ret:
        text = re.sub(r"<.*>", '', text).replace(' ', '')

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
                if len(value) < 2:
                    continue
                else:
                    # 全中文情况下去除空格
                    result = re.findall(r'[a-zA-Z0-9]+', value)
                    if not result:
                        value = value.replace(' ', '')
                    value = value.strip()
                    if len(value) > 1:
                        ret.append(value)
            else:
                if len(value) > 1:
                    ret.append(value)
    return ret


def read_wk_file(path: str, name: str):
    file_path = os.path.join(path, name)
    ret = []
    lines = 0
    with open(file_path, 'r') as file:
        for line in file.readlines():
            lines = lines + 1
            fcc_data = json.loads(line)
            for key, value in fcc_data.items():
                if key == "id":
                    continue
                elif key == "url":
                    continue
                elif key == "title":
                    # result = parse_text(value)
                    ret.append(value)
                elif key == "text":
                    # result = parse_text(value)
                    ret.append(value)
                else:
                    print(f"unknown key = {key} = > {value}")
                    exit(-1)
    return ret


def process_dir(path: str, dir_name: str, corpus: str, en_dict: dict):
    count = 0
    out_path = os.path.join("data", corpus, dir_name + ".txt")
    raw_path = os.path.join("raw_data", corpus, dir_name + ".txt")
    with open(out_path, 'w') as f, open(raw_path, 'w') as writer:
        for file_name in os.listdir(os.path.join(path, dir_name)):
            if file_name.startswith("."):
                continue
            file_count = 0
            lines = read_wk_file(os.path.join(path, dir_name), file_name)
            # TODO 生成临时语料
            for line in lines:
                data, raw_data = filter_raw_text(line, en_dict)
                for v in raw_data:
                    writer.write(v + "\n")
                for text in data:
                    if text.strip() != '':
                        f.write(text + "\n")
                        count = count + 1
                        file_count = file_count + 1
            print(f"{file_name},lines={len(lines)},size={file_count}")
    print(f"dir_finish={dir_name},size={count}>>>>>>")
    return count


def process_corpus(dir_path: str, corpus: str):
    dict_path = 'cet4_dict.txt'
    en_dict: dict = read_en_dict(dict_path)
    print(f"en_dict={len(en_dict)}")

    path = os.path.join(dir_path, corpus)
    count = 0
    for dir_name in os.listdir(path):
        if not dir_name.startswith("."):
            count += process_dir(path, dir_name, corpus, en_dict)
    print(f"{corpus} finish,count={count} >>>>>>>>>>>>>>")


if __name__ == '__main__':
    path = "/Users/brucesun/asr-corpus/lm"
    corpus = 'wiki_zh'
    process_corpus(path, corpus)

    # text = ["爱我中华", '中华人民共和国']
    # writer_file(text, 'test')
