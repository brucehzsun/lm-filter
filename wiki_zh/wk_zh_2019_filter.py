import os
import json
import re

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
delete_list = ['《', '》', '（）', "「", "」", '）', '（', '“', '”', '(', ')', '〈', '〉', '-', '–', '{', '}', '"', '·', '|',
               ',', '‧', '[', ']', '*', '#', '%', '±', '℃', ' ', '〇', '．', '……', '=', '&', '『', '˭']
replace_map = {'～': '到', '.': "", ':': '', '°': '度', '－': ' '}
number = '0123456789'

def is_chinese_char(ch: chr):
    return ('\u4e00' <= ch <= '\u9FFF') or ('\uAC00' <= ch <= '\uD7AF') or ('\u3040' <= ch <= '\u31FF')  # 中文 韩文 日文


def to_lm_str(text: str):
    output = ['<s>']
    buffer = ''
    pre_char: chr = None
    for s in text:
        if is_chinese_char(s):  # 中文 韩文 日文
            if buffer:
                output.append(buffer)
            buffer = ''
            if not s.strip() == '':
                output.append(s)
        else:  # 标点符号等, 面积147km² => 面 积 147 km²
            if (pre_char is not None) and (pre_char in number) and s not in number:
                if buffer:
                    output.append(buffer)
                buffer = ''
                if not s.strip() == '':
                    buffer += s
            else:
                buffer += s
        pre_char = s
    if buffer:
        output.append(buffer)
    output.append('</s>')
    return " ".join(output)


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
            else:
                continue
            # 全中文情况下去除空格
            result = re.findall(r'[a-zA-Z0-9]+', value)
            if not result:
                value = value.replace(' ', '')
            value = value.strip()
            if len(value) < 3:
                continue
            ret.append(value)
        # if v.startwith("1\")
    return ret


def parse_wk_file(path: str, name: str):
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
                    result = parse_text(value)
                    ret.extend(result)
                elif key == "text":
                    result = parse_text(value)
                    ret.extend(result)
                else:
                    print(f"unknown key = {key} = > {value}")
                    exit(-1)
    print(f"{name},lines={lines},size={len(ret)}")
    return ret


def process_dir(path: str, dir_name: str, corpus: str):
    count = 0
    out_path = os.path.join("data", corpus, dir_name + ".txt")
    raw_path = os.path.join("raw_data", corpus, dir_name + ".txt")
    with open(out_path, 'w') as f, open(raw_path, 'w') as raw_f:
        for file_name in os.listdir(os.path.join(path, dir_name)):
            raw_f.write(f"\n{file_name}>>>>")
            result = parse_wk_file(os.path.join(path, dir_name), file_name)
            count += len(result)
            for text in result:
                raw_f.write(text + "\n")
                ret = to_lm_str(text)
                f.write(ret + "\n")
    print(f"dir_finish={dir_name},size={count}>>>>>>")
    return count


def process_corpus(dir_path: str, corpus: str):
    path = os.path.join(dir_path, corpus)
    count = 0
    for dir_name in os.listdir(path):
        if not dir_name.startswith("."):
            count += process_dir(path, dir_name, corpus)
            break
    print(f"{corpus} finish,count={count} >>>>>>>>>>>>>>")


if __name__ == '__main__':
    path = "/Users/brucesun/asr-corpus/lm"
    corpus = 'wiki_zh'
    process_corpus(path, corpus)
    # text = ["爱我中华", '中华人民共和国']
    # writer_file(text, 'test')
