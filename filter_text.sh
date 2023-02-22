#!/bin/zsh

export PYTHONPATH=$pwd:$PYTHONPATH
python src/new_zh/nwes_zh_filter.py
python src/wiki_zh/wk_zh_2019_filter.py
python src/wiki_zh/merger.py
python src/baike_qa/baike_qa_filter.py
