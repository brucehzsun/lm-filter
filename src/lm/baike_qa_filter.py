import datetime
import os
import json
import re
import sys
import argparse
from src.utils import en_dict_util
from src.utils import text_filter


def parse_json_text(line: str):
    result = []
    json_data = json.loads(line)
    # 处理category
    for value in re.split(r"[-/]", json_data['category']):
        result.append(value)

    # 处理 title,desc,answer
    title_list = json_data['title']
    if len(title_list) > 0:
        result.append(title_list)

    desc_list = json_data['desc']
    if len(desc_list) > 0:
        result.append(desc_list)

    answer_list = json_data['answer']
    if len(answer_list) > 0:
        result.append(answer_list)

    return result


def process_baike_file(dir_path: str, file_name: str, en_dict: dict, corpus_name: str):
    out_dir = os.path.join('/data/kenlm_data/data', corpus_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    path = os.path.join(dir_path, file_name)
    writer_path = os.path.join(out_dir, file_name + ".txt")
    print(f"start process {file_name},time={datetime.datetime.now()}")
    sys.stdout.flush()
    total_count = 0
    with open(path) as file, open(writer_path, "w") as writer:
        lines = file.readlines()
        total_lines = len(lines)
        count = 0
        for line in lines:
            count = count + 1
            if count % 10000 == 0:
                print(f"processed:{count}/{total_lines},count={total_count},time={datetime.datetime.now()}...")
                sys.stdout.flush()
            for text in parse_json_text(line):
                data_list, raw_data_list = text_filter.filter_raw_text(text, en_dict, False)
                for t in data_list:
                    writer.write(t + "\n")
                    total_count += 1
    print(f"{file_name} file finished,count={total_count},time={datetime.datetime.now()}")
    sys.stdout.flush()
    return total_count


def process_corpus(dir_path: str, corpus: str):
    dict_path = 'cet4_dict.txt'
    en_dict: dict = en_dict_util.read_en_dict(dict_path)
    print(f"en_dict={len(en_dict)}")

    path = os.path.join(dir_path, corpus)
    total_count = 0
    for file_name in os.listdir(path):
        if not file_name.startswith("."):
            count = process_baike_file(path, file_name, en_dict, corpus)
            total_count += count
    print(f"{corpus} finish,total_count={total_count},time={datetime.datetime.now()} >>>>>>>>>>>>>>")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='process your lm corpus')
    parser.add_argument('--data_path', required=True, type=str, help='path of lm corpus')
    args = parser.parse_args()

    path = args.data_path
    print(f"start baike_qa corpus process,path={path},time={datetime.datetime.now()}")
    # path = "/Users/brucesun/asr-corpus/lm"
    # path = "/home/bruce/asr/data"
    corpus = 'baike_qa'
    process_corpus(path, corpus)
