#!/bin/zsh

export PYTHONPATH=$(pwd):$PYTHONPATH
nohup python3 src/lm/wk_zh_2019_filter.py --data_path /data/lm_corpus >logs/wiki.log 2>&1 &
nohup python3 src/lm/news_zh_filter.py --data_path /data/lm_corpus >logs/news.log 2>&1 &
nohup python3 src/lm/baike_qa_filter.py --data_path /data/lm_corpus >logs/baike.log 2>&1 &
# 完成
nohup python3 src/lm/rokid_train.py --corpus /data/lm_corpus >logs/rokid.log 2>&1 &

# 完成
nohup python3 src/lm/rokid_train_en.py >logs/rokid_en.log 2>&1 &

# python3 src/lm/merger_corpus.py