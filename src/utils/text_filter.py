# coding:utf-8

import re
from src.utils import number_util

pattern_special = re.compile(r"<.*>")

replace_map = {'～': '到', '.': "", ':': '', '°': '度', '－': ' ', '_': ' ', 'km²': "平方千米", "km": "千米", '×': '乘',
               '<': ' ', '\\': ' ', 'kg': '千克'}
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
enOnlyPattern = re.compile(r'^[a-z A-Z]+$')
# enOnlyPattern = re.compile('^w+$')
digitPattern = re.compile(r'^[0-9０-９]+$')
splitPattern = re.compile(r"[,，.。？?！!：;；/:／、\r\n]")
replaceSpacePattern = re.compile(r"[、]")
replaceTitlePattern = re.compile("^\d[\.\．]")


def split_text(text: str, filter_bad_text: bool):
    result = []
    try:
        text = number_util.enDigitReplace(text)
        text = number_util.floatDigitReplace(text)

        for value in splitPattern.split(text):
            value = value.strip()
            if value is None:
                continue
            if filter_bad_text and value.__contains__('??????????'):
                continue
            result.append(value)
        return result
    except ValueError:
        print(f"ValueError:{text}")


def filter_text(text: str):
    ret = pattern_special.search(text)
    if ret:
        raw_text = re.sub(r"<.*>", '\n', text)

    ret = []
    text = text.strip()

    # 替换
    for k, v in replace_map.items():
        text = text.replace(k, v)
    # 去掉1. 2. 3. ⒊
    text = replaceTitlePattern.sub('', text)
    text = replaceSpacePattern.sub(' ', text)

    # 不包含中文场景全部不要
    result = zhPattern.search(text)
    if result is None:
        return None

    result = digitPattern.search(text)
    if result:
        return None

    text = text.strip()
    if 1 < len(text) < 80:
        ret.append(text)
    return ret


def filter_raw_text(raw_text: str, en_dict: dict, filter_bad_text: bool):
    result = []
    raw_data = []
    text_list = split_text(raw_text, filter_bad_text)
    if text_list is None:
        return None, None

    for text in text_list:
        corpus = filter_text(text)
        if corpus is None:
            continue
        for t in corpus:
            ret, raw_ret = to_lm_str(t, en_dict)
            if ret is None or ret == '':
                continue
            result.append(ret)
            raw_data.append(raw_ret)
    return result, raw_data


def is_chinese_char(ch: chr):
    # return ('\u4e00' <= ch <= '\u9FFF') or ('\uAC00' <= ch <= '\uD7AF') or ('\u3040' <= ch <= '\u31FF')  # 中文 韩文 日文
    return ('\u4e00' <= ch <= '\u9FFF')  # 中文 韩文 日文


def add_word_to_list(word: str, output: list, en_dict: dict):
    word = word.strip()
    if word == '':
        return

    if enOnlyPattern.search(word):
        # 英文
        # if en_dict.get(word.lower()):
        output.append(word)
    else:
        output.append(word)


# output.append(word)


def to_lm_str(data: str, en_dict: dict):
    text = data.strip()
    if text is None or text == '':
        return None, None

    text = number_util.convert_number(text)

    output = []
    word = ''
    pre_char: chr = None
    for ch in text:
        if is_chinese_char(ch):  # 中文 韩文 日文
            # 1.中文需要
            if ch == word:
                output.append(ch)
                add_word_to_list(ch, output, en_dict)
                pre_char = ch
            else:
                add_word_to_list(word, output, en_dict)
                add_word_to_list(ch, output, en_dict)
                pre_char = ch
            word = ''
        if ch.lower() in 'abcdefghijklmnopqrstuvwxyz' or ch.lower() in 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ':
            # 英文字母 需要
            word += ch
            pre_char = ch
        elif ch == ' ':  # 空格 区分单词
            add_word_to_list(word, output, en_dict)
            pre_char = ch
            word = ''
        else:  # 标点符号等, 面积147km² => 面 积 147 km²
            if (pre_char is not None) and (pre_char in number_util.number) and ch not in number_util.number:
                add_word_to_list(word, output, en_dict)
                word = ''
                pre_char = ch
                # if not ch.strip() == '':
                #     word += ch
            # else:
            #     word += ch

    if word:
        add_word_to_list(word, output, en_dict)

    if len(output) > 1:
        return " ".join(output), text
    else:
        return None, None


def convert_to_lm_text(corpus: str):
    en_word = ''
    lm_corpus = []
    for ch in corpus:
        if is_chinese_char(ch):  # 中文 韩文 日文
            # 1.中文需要
            if en_word.strip() != '':
                lm_corpus.append(en_word.strip())
                en_word = ''

            if ch.strip() != '':
                lm_corpus.append(ch.strip())
        if ch.lower() in 'abcdefghijklmnopqrstuvwxyz':
            # 英文字母 需要
            en_word += ch.strip().lower()
        elif ch == ' ':  # 空格 区分单词
            if en_word.strip() != '':
                lm_corpus.append(en_word.strip())
            en_word = ''
        else:
            pass
    if en_word.strip() != '':
        lm_corpus.append(en_word.strip())

    return ' '.join(lm_corpus)
