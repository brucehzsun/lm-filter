from src.utils import text_filter
import re

if __name__ == '__main__':
    # corpus_list = ['啊第二节课SECOND CLASS', 'hello word', '面积147km²', 'NINETY FIVE TIMES FROM CLASSES',
    #                '然后AFTER表示在什么什么之后AFTER CLASS的意思就是课下放学后']
    # for corpus in corpus_list:
    #     text = text_filter.convert_to_lm_text(corpus)
    #     print(text)
    list1 = ['AAAA','BBBB']
    list2 = ['CCCC']
    list2.extend(list1)
    print(list2)