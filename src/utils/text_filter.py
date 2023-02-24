# coding:utf-8

import re
from src.utils import number_util

pattern_special = re.compile(r"<.*>")

replace_map = {'～': '到', '.': "", ':': '', '°': '度', '－': ' ', '_': ' ', '一': ' ', 'km²': "平方米", "km": "千米", '×': '乘',
               '<': ' ', '\\': ' '}
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
enOnlyPattern = re.compile(r'^[a-z A-Z]+$')
# enOnlyPattern = re.compile('^w+$')
digitPattern = re.compile(r'^[0-9０-９]+$')
splitPattern = re.compile(r"[,，.。？?！!：;；/:／、\r\n]")
replaceSpacePattern = re.compile(r"[、]")
replaceTitlePattern = re.compile("^\d[.．]")


def split_text(text: str):
    result = []
    for value in splitPattern.split(text):
        value = value.strip()
        if value:
            result.append(value)
    return result


def filter_text(raw_text: str):
    ret = pattern_special.search(raw_text)
    if ret:
        raw_text = re.sub(r"<.*>", '\n', raw_text)

    ret = []
    for text in split_text(raw_text):
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
            continue

        result = digitPattern.search(text)
        if result:
            continue

        text = text.strip()
        if 1 < len(text) < 80:
            ret.append(text)
    return ret


def is_chinese_char(ch: chr):
    # return ('\u4e00' <= ch <= '\u9FFF') or ('\uAC00' <= ch <= '\uD7AF') or ('\u3040' <= ch <= '\u31FF')  # 中文 韩文 日文
    return ('\u4e00' <= ch <= '\u9FFF')  # 中文 韩文 日文


def add_word_to_list(word: str, output: list, en_dict: dict):
    word = word.strip()
    if word == '':
        return

    if enOnlyPattern.search(word):
        # 英文
        if en_dict.get(word.lower()):
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
            add_word_to_list(word,output,en_dict)
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
