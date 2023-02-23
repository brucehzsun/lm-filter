import argparse
import os
import datetime


def merger_wik(file_paths: list):
    print(f"start merge multi file to one file...")
    corpus_path = os.path.join('data', 'rokid_lm.txt')
    count = 0
    with open(corpus_path, 'w') as writer:
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                writer.writelines(lines)
                print(f"writer,path= {file_path}, size={len(lines)},time={datetime.datetime.now()}")
                count += len(lines)
    print(f"finish, total size = {count},time={datetime.datetime.now()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='merge your lm corpus')
    parser.add_argument('--data_path', required=True, type=str, help='path of lm corpus')
    args = parser.parse_args()

    path = args.data_path
    print(f"start merger corpus process,path={path},time={datetime.datetime.now()}")

    file_paths = []
    file_paths.append(os.path.join('data', 'baike_qa2019', 'baike_qa_valid.json.txt'))
    file_paths.append(os.path.join('data', 'baike_qa2019', 'baike_qa_train.json.txt'))

    file_paths.append(os.path.join('data', 'new2016zh', 'news2016zh_train.json.txt'))
    file_paths.append(os.path.join('data', 'new2016zh', 'news2016zh_valid.json.txt'))

    file_paths.append(os.path.join('data', 'wiki_zh.txt'))

    merger_wik(file_paths)
