#!/bin/zsh

export PYTHONPATH=$(pwd):$PYTHONPATH
CORPUS_PATH=/Users/brucesun/asr-corpus/lm
python3 src/lm/wk_zh_2019_filter.py --data_path $CORPUS_PATH | tee -a logs/wiki.log
python3 src/lm/nwes_zh_filter.py --data_path $CORPUS_PATH | tee -a logs/news.log
python3 src/lm/baike_qa_filter.py --data_path $CORPUS_PATH | tee -a logs/baike.log
