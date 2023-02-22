from src.utils import text_filter
from src.utils import en_dict_util as en

if __name__ == '__main__':
    dict_path = '../../cet4_dict.txt'
    en_dict: dict = en.read_en_dict(dict_path)

    data = ['35', '苏常柴Ａ 000570 11', '0 1', ' 15']
    for text in data:
        texts = text_filter.split_text(text)
        for t in texts:
            for sub_t in text_filter.filter_text(t):
                ret = text_filter.to_lm_str(sub_t, en_dict)
                print(ret)
