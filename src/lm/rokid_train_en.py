import argparse
import datetime
import os
from src.utils import text_filter
import sys


def process_corpus(file_path: str, corpus_name: str):
    out_path = os.path.join("data", corpus_name + ".txt")
    count = 0
    with open(file_path, 'r') as f, open(out_path, 'w') as writer:
        lines = f.readlines()
        total_len = len(lines)
        for line in lines:
            line = line.replace('\n', '')
            corpus = line.split(' ', 1)[1]
            if (count == 0):
                print(f"origin={line},corpus={corpus}")
            lm_text = text_filter.convert_to_lm_text(corpus)
            if lm_text is None or lm_text == '':
                continue
            writer.write(lm_text + "\n")
            count = count + 1
            if count % 10000 == 0:
                print(f"process {count}/{total_len}")
                sys.stdout.flush()
        sys.stdout.flush()
    print(f"process_corpus finish,{corpus_name},size={count}>>>>>>")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='process your lm corpus')
    # parser.add_argument('--corpus', required=True, type=str, help='path of lm corpus')
    args = parser.parse_args()

    corpus_path = "raw_data/train_rokidcs.text";
    print(f"start rokid train corpus process,path={corpus_path},time={datetime.datetime.now()}")

    # path = "/Users/brucesun/asr-corpus/lm"
    # path = "/home/bruce/asr/data"
    corpus_name = 'rokid_train_en.txt'
    process_corpus(corpus_path, corpus_name)
