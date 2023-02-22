import os
import json
import sys
from src.utils import text_filter
from src.utils import en_dict_util


def filter_raw_text(raw_text: str, en_dict: dict):
    result = []
    raw_data = []
    text_list = text_filter.split_text(raw_text)
    for text in text_list:
        for t in text_filter.filter_text(text):
            ret, raw_ret = text_filter.to_lm_str(t, en_dict)
            if ret is not None:
                result.append(ret)
                raw_data.append(raw_ret)
    return result, raw_data


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
                # for v in raw_data:
                # writer.write(v + "\n")
                # writer.write(line + "\n")
                for text in data:
                    if text.strip() != '':
                        f.write(text + "\n")
                        count = count + 1
                        file_count = file_count + 1
            print(f"{file_name},lines={len(lines)},size={file_count}")
            sys.stdout.flush()
    print(f"dir_finish={dir_name},size={count}>>>>>>")
    return count


def process_corpus(dir_path: str, corpus: str):
    dict_path = 'cet4_dict.txt'
    en_dict: dict = en_dict_util.read_en_dict(dict_path)
    print(f"en_dict={len(en_dict)}")
    sys.stdout.flush()

    path = os.path.join(dir_path, corpus)
    count = 0
    for dir_name in os.listdir(path):
        if not dir_name.startswith("."):
            count += process_dir(path, dir_name, corpus, en_dict)
    print(f"{corpus} finish,count={count} >>>>>>>>>>>>>>")


if __name__ == '__main__':
    path = "/Users/brucesun/asr-corpus/lm"
    path = "/home/bruce/asr/data"
    corpus = 'wiki_zh'
    process_corpus(path, corpus)

    # text = ["爱我中华", '中华人民共和国']
    # writer_file(text, 'test')
