from src.utils import text_filter

if __name__ == '__main__':
    corpus_list = ["I am a teacher",
                   "我有很多特殊字符好像有9个how are you﹏和……",
                   "18601291823"
                   ]
    # for corpus in corpus_list:
    #     text_list = text_filter.filter_text(corpus)
    for text in corpus_list:
        print(f"{text}")
        for ch in text:
            if ch.isalpha():
                print(f"ch is alpha={ch}")
            # if text_filter.is_chinese_char(ch):
            #     print(ch)
            # if ch in '0123456789':
            #     print(f"数字={ch}")
            # if ch.lower() in 'abcdefghijklmnopqrstuvwxyz':
            #     print(f"英文={ch}")
