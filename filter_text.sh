#!/bin/zsh

export PYTHONPATH=`pwd`:$PYTHONPATH
python3 src/new_zh/nwes_zh_filter.py
python3 src/wiki_zh/wk_zh_2019_filter.py
python3 src/wiki_zh/merger.py
python3 src/baike_qa/baike_qa_filter.py
