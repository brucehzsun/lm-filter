import re
from src.utils import number_util

delete_first = ['<br>', '</br>', '<div>', '</div>']
pattern_special = re.compile(r"<.*>")

delete_list = ['《', '》', '（）', "「", "」", '）', '（', '“', '”', '(', ')', '〈', '〉', '-', '–', '{', '}', '"', '·', '|',
               ',', '‧', '*', '#', '%', '±', '℃', ' ', '〇', '．', '……', '=', '&', '『', '』', '˭', '※', '〔 ', '≤', '≥',
               '【', '】', '〔', '〕', '［', '］', '[', ']', '〖', '〗', '+', '™', '®', '・', '~', '`', '①', '②', '③', '④', '⑤',
               '⑥', '⑦', '⑧', "'", '∶', '＂', '★', '⒈', '⒉', '⒊', '⒋', '＠', '——', '^', '％', '<', '>', '●', '→', '＝',
               '――――――', '∴', '@', '◢', '△']
replace_map = {'～': '到', '.': "", ':': '', '°': '度', '－': ' ', '_': ' ', '一': ' ', 'km²': "平方米", "km": "千米", '×': '乘',
               '<': ' ', '\\': ' '}
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
digitPattern = re.compile(r'^[0-9０-９]+$')
splitPattern = re.compile(r"[,，.。？?！!：;；/:、／\r\n]")


def split_text(text: str):
    result = []
    for value in splitPattern.split(text):
        value = value.strip()
        if value:
            result.append(value)
    return result


def filter_text(text: str):
    for split in delete_first:
        text = text.replace(split, '\n')

    ret = pattern_special.search(text)
    if ret:
        text = re.sub(r"<.*>", '', text).replace(' ', '')

    ret = []
    for v in text.split("\n\n"):
        v = v.strip()
        if v == '':
            continue
        for value in split_text(v):
            value = value.strip()
            # 删除
            for replace in delete_list:
                value = value.replace(replace, "")
            # 替换
            for k, v in replace_map.items():
                value = value.replace(k, v)
            # 去掉1. 2. 3. ⒊
            value = re.sub("^\d.", '', value)
            # 是否包含中文字符
            result = zhPattern.search(value)
            if result:
                if len(value) < 2:
                    continue
                else:
                    # 全中文情况下去除空格
                    result = re.findall(r'[a-zA-Z0-9]+', value)
                    if not result:
                        value = value.replace(' ', '')
                    value = value.strip()
                    if 1 < len(value) < 60:
                        ret.append(value)
            elif value.isalpha():
                # 英文场景
                if 1 < len(value) < 60:
                    ret.append(value)
            else:
                # 非中文和英文场景
                result = digitPattern.search(value)
                if result:
                    # 纯数字不处理
                    continue
                    # elif 1 < len(value) < 60:
                    # ret.append(value)
    return ret


def is_chinese_char(ch: chr):
    return ('\u4e00' <= ch <= '\u9FFF') or ('\uAC00' <= ch <= '\uD7AF') or ('\u3040' <= ch <= '\u31FF')  # 中文 韩文 日文


def add_word_to_list(word: str, output: list, en_dict: dict):
    if not word:
        return

    word = word.strip()
    if word == '':
        return

    if is_chinese_char(word):
        output.append(word)
    elif word.isalpha():
        # 英文
        if en_dict.get(word.lower()):
            output.append(word)
    elif word.isnumeric():
        return
    else:
        output.append(word)


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
            add_word_to_list(word, output, en_dict)
            word = ''
            if not ch.strip() == '':
                output.append(ch)
        elif ch == ' ':  # 空格 区分单词
            add_word_to_list(word, output, en_dict)
            word = ''
        else:  # 标点符号等, 面积147km² => 面 积 147 km²
            if (pre_char is not None) and (pre_char in number_util.number) and ch not in number_util.number:
                add_word_to_list(word, output, en_dict)
                word = ''
                if not ch.strip() == '':
                    word += ch
            else:
                word += ch
        pre_char = ch
    if word:
        add_word_to_list(word, output, en_dict)

    if len(output) > 1:
        return " ".join(output), text
    else:
        return None, None
