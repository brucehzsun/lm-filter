from src.utils import text_filter
import re
from src.utils import number_util
import cn2an

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

if __name__ == '__main__':
    corpus_list = ['啊第二节课SECOND CLASS', 'hello word', '面积147km²']
    for corpus in corpus_list:
        text = text_filter.convert_to_lm_text(corpus)
        print(text)
