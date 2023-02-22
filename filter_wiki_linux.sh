#!/bin/zsh

export PYTHONPATH=$(pwd):$PYTHONPATH
CORPUS_PATH=/home/bruce/asr/data
nohup python3 src/wiki_zh/wk_zh_2019_filter.py --data_path $CORPUS_PATH >logs/wiki.log 2>&1 &
nohup python3 src/new_zh/nwes_zh_filter.py --data_path $CORPUS_PATH >logs/news.log 2>&1 &
nohup python3 src/baike_qa/baike_qa_filter.py --data_path $CORPUS_PATH >logs/baike.log 2>&1 &
