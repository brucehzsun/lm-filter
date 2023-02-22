#!/bin/zsh

export PYTHONPATH=${pwd}:$PYTHONPATH
#python wiki_zh/wk_zh_2019_filter.py
#python wiki_zh/merger.py

python src/baike_qa/baike_qa_filter.py