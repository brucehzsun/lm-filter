## news_2016_zh 语料
2.3395 亿条 
#### news2016zh_valid

语料数：

#### news2016zh_train

语料数：23395.0991 万条


nohup python3 src/new_zh/nwes_zh_filter.py > logs/news.log 2>&1 &
nohup python3 src/baike_qa/baike_qa_filter.py > logs/baike.log 2>&1 &
nohup python3 ./filter_wiki.sh > logs/wiki.log 2>&1 &
