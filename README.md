## 收集到的语料

累计：3.2136亿条语料(处理后)

### news_2016_zh 语料

清洗后的语料数：24138.4891 万条

### wiki_zh_2019

清洗后的语料数：3258.2909 万条

### baike_qa_2016

清洗后的语料数：4739.2483万条

## 清洗命令

```buildoutcfg
nohup python3 src/new_zh/nwes_zh_filter.py > logs/news.log 2>&1 & 
nohup python3 src/baike_qa/baike_qa_filter.py >logs/baike.log 2>&1 & 
nohup python3 ./filter_wiki.sh > logs/wiki.log 2>&1 &

```
