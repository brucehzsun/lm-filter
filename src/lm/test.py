from src.utils import text_filter
import re
from src.utils import number_util
import cn2an

if __name__ == '__main__':
    corpus_list = ['矩震级高达8.1,震源深度15千米',
                   '关东大地震死亡人数估计大约介于100,000至142,000人',
                   '日本时间12时1分与3分又分别发生规模7.3与7.2的余震'
                   ]
    for corpus in corpus_list:
        text_list = text_filter.split_text(corpus)
        for text in text_list:
            for t in text_filter.filter_text(text):
                ret, raw_ret = text_filter.to_lm_str(t, None)
                print(ret)
