from src.utils import text_filter
import re

if __name__ == '__main__':
    corpus_list = ['啊第二节课SECOND CLASS', 'hello word', '面积147km²', 'NINETY FIVE TIMES FROM CLASSES',
                   '然后 AFTER 表示在什么什么之后 AFTER CLASS 的意思就是课下放学后']
    for corpus in corpus_list:
        text = text_filter.convert_to_lm_text(corpus)
        print(text)
