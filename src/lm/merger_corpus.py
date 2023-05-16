import os
import datetime
import time


def merger_wik(file_paths: list, basic_dir: str):
    print(f"start merge multi file to one file...")
    corpus_path = os.path.join(basic_dir, 'rokid_lm.txt')
    total_size = 0
    with open(corpus_path, 'w') as writer:
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                count = 0
                start_time = time.time()
                line = f.readline()  # 读取第一行
                while line is not None and line != '':
                    writer.write(line)
                    count += 1
                    total_size += 1
                    line = f.readline()  # 读取下一行
                    if count % 10000000 == 0:
                        print(f"processed:{count},time={(time.time() - start_time) * 1000}ms")
                used_time = (time.time() - start_time) * 1000
                print(f"writer,path= {file_path}, size={count},total_size={total_size},time={used_time}ms")
    print(f"finish, total size = {total_size},time={datetime.datetime.now()}")


if __name__ == '__main__':
    print(f"start merger corpus process,time={datetime.datetime.now()}")

    root_path = '/data/kenlm_data/data'
    file_paths = []
    file_paths.append(os.path.join(root_path, 'baike_qa', 'baike_qa_valid.json.txt'))
    file_paths.append(os.path.join(root_path, 'baike_qa', 'baike_qa_train.json.txt'))

    file_paths.append(os.path.join(root_path, 'news_zh', 'news2016zh_train.json.txt'))
    file_paths.append(os.path.join(root_path, 'news_zh', 'news2016zh_valid.json.txt'))

    file_paths.append(os.path.join(root_path, 'wiki_zh.txt'))
    file_paths.append(os.path.join(root_path, 'rokid_train.txt'))
    file_paths.append(os.path.join(root_path, 'rokid_train_en.txt'))

    merger_wik(file_paths, root_path)
