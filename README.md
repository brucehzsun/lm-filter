## news_2016_cn 语料
23395.0991 万条 
#### news2016zh_valid

语料数：

#### news2016zh_train

语料数：23395.0991 万条

nohup python3 src/new_zh/nwes_zh_filter.py > log.txt 2>&1 &
nohup ./filter_text.sh >> log.txt 2>&1 &

nohup ./filter_text.sh > nohup.out 2> nohup.err < /dev/null &
