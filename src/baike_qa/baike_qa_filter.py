import os
import json
import re
import sys
import argparse
from src.utils import en_dict_util
from src.utils import text_filter


def split_json_text(line: str):
    result = []
    json_data = json.loads(line)
    # 处理category
    for value in re.split(r"[-/]", json_data['category']):
        result.append(value)

    # 处理 title,desc,answer
    title_list = text_filter.split_text(json_data['title'])
    if len(title_list) > 0:
        result.extend(title_list)

    desc_list = text_filter.split_text(json_data['desc'])
    if len(desc_list) > 0:
        result.extend(desc_list)

    answer_list = text_filter.split_text(json_data['answer'])
    if len(answer_list) > 0:
        result.extend(answer_list)

    return result


def process_baike_file(dir_path: str, file_name: str, en_dict: dict, corpus: str):
    path = os.path.join(dir_path, file_name)
    writer_path = os.path.join("data", corpus, file_name + ".txt")
    print(f"start process {file_name}")
    sys.stdout.flush()
    total_count = 0
    with open(path) as file, open(writer_path, "w") as writer:
        lines = file.readlines()
        total_lines = len(lines)
        count = 0
        for line in lines:
            count = count + 1
            if count % 10000 == 0:
                print(f"processed:{count}/{total_lines},count={total_count}...")
                sys.stdout.flush()
            for text in split_json_text(line):
                if text.__contains__('??????'):
                    # 处理乱码
                    continue

                text_list = text_filter.filter_text(text)
                for t in text_list:
                    t = t.strip()
                    if t != '':
                        t, raw_data = text_filter.to_lm_str(t, en_dict)
                        if t:
                            writer.write(t + "\n")
                            total_count += 1
    print(f"{file_name} file finished,count={total_count}")
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
    print(f"{corpus} finish,total_count={total_count} >>>>>>>>>>>>>>")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='process your lm corpus')
    parser.add_argument('--data_path', required=True, type=str, help='path of lm corpus')
    args = parser.parse_args()

    path = args.data_path
    print(f"start baike_qa corpus process,path={path}")
    # path = "/Users/brucesun/asr-corpus/lm"
    # path = "/home/bruce/asr/data"
    corpus = 'baike_qa2019'
    process_corpus(path, corpus)
