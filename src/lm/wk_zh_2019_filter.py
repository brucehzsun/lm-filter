import argparse
import datetime
import os
import json
import sys
import time

from src.utils import text_filter
from src.utils import en_dict_util


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
    out_dir = os.path.join('/data/kenlm_data/data', corpus)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    out_path = os.path.join(out_dir, dir_name + ".txt")
    with open(out_path, 'w') as f:
        for file_name in os.listdir(os.path.join(path, dir_name)):
            if file_name.startswith("."):
                continue
            file_count = 0
            lines = read_wk_file(os.path.join(path, dir_name), file_name)
            # TODO 生成临时语料
            for line in lines:
                data, raw_data = text_filter.filter_raw_text(line, en_dict, False)
                if data is None or data == '':
                    continue
                for text in data:
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


def merger_wik(path: str, corpus: str):
    print(f"start merge multi file to one file...")
    count = 0
    path = os.path.join(path, corpus)
    with open(path + ".txt", 'w') as writer:
        for file_name in os.listdir(path):
            with open(os.path.join(path, file_name), 'r') as f:
                lines = f.readlines()
                writer.writelines(lines)
                print(f"writer {file_name}, size={len(lines)},time={datetime.datetime.now()}")
                count += len(lines)
    print(f"finish, total size = {count},time={datetime.datetime.now()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='process your lm corpus')
    parser.add_argument('--data_path', required=True, type=str, help='path of lm corpus')
    args = parser.parse_args()

    path = args.data_path
    print(f"start wiki_zh corpus process,path={path},time={datetime.datetime.now()}")

    # path = "/Users/brucesun/asr-corpus/lm"
    # path = "/home/bruce/asr/data"
    corpus = 'wiki_zh'
    process_corpus(path, corpus)

    # merger multi file to one file
    merger_wik('data', corpus)
