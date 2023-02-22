import os
import json
import re
from src.utils import en_dict_util
from src.utils import text_filter


def split_json_text(line: str):
    result = []
    json_data = json.loads(line)
    # 处理category
    title_list = text_filter.split_text(json_data['keywords'])
    if len(title_list) > 0:
        result.extend(title_list)

    # 处理 title,desc,answer
    title_list = text_filter.split_text(json_data['desc'])
    if len(title_list) > 0:
        result.extend(title_list)

    desc_list = text_filter.split_text(json_data['title'])
    if len(desc_list) > 0:
        result.extend(desc_list)

    answer_list = text_filter.split_text(json_data['source'])
    if len(answer_list) > 0:
        result.extend(answer_list)

    content_list = text_filter.split_text(json_data['content'])
    if len(content_list) > 0:
        result.extend(content_list)

    return result


def process_baike_file(dir_path: str, file_name: str, en_dict: dict, corpus: str):
    path = os.path.join(dir_path, file_name)
    writer_path = os.path.join("data", corpus, file_name + ".txt")
    raw_writer_path = os.path.join("raw_data", corpus, file_name + ".txt")
    print(f"start process {file_name}")
    total_count = 0
    with open(path) as file, open(writer_path, "w") as writer, open(raw_writer_path, 'w') as raw_writer:
        lines = file.readlines()
        total_lines = len(lines)
        print(f"total count = {total_lines}")
        count = 0
        for line in lines:
            texts = split_json_text(line)
            count += 1
            if count % 10000 == 0:
                print(f"processed:{count}/{total_lines}...")
            for text in texts:
                if text.__contains__('??????'):
                    # 处理乱码
                    continue
                text_list = text_filter.filter_text(text)
                for t in text_list:
                    t, raw_data = text_filter.to_lm_str(t, en_dict)
                    if t:
                        writer.write(t + "\n")
                        total_count += 1
    print(f"{file_name} file finished,count={total_count}")
    return total_count


def process_corpus(dir_path: str, corpus: str):
    dict_path = 'cet4_dict.txt'
    en_dict: dict = en_dict_util.read_en_dict(dict_path)
    print(f"en_dict={len(en_dict)}")

    path = os.path.join(dir_path, corpus)
    total_count = 0
    for file_name in os.listdir(path):
        if not file_name.startswith("."):
            # if file_name == 'news2016zh_train.json':
            # todo delete
            # continue
            count = process_baike_file(path, file_name, en_dict, corpus)
            total_count += count
            break
    print(f"{corpus} finish,total_count={total_count} >>>>>>>>>>>>>>")


if __name__ == '__main__':
    path = "/Users/brucesun/asr-corpus/lm"
    corpus = 'new2016zh'
    process_corpus(path, corpus)
