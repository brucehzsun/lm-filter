import cn2an
import re
from wiki_zh import wk_zh_2019_filter as wk

NUM_DICT = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}

pattern_date = re.compile(r'\d{1,4}(年|月|日|小时|分钟|秒)')  # 查找日期时间数字
pattern_number = re.compile(r'\d+')
pattern_phone = re.compile(
    r'((\d{11})|((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})))')  # 查找电话号码
number = '0123456789'


def convert_normal_number(text: str):
    letters = [x for x in text]
    ret = pattern_number.search(text)
    while ret is not None:
        num = "".join(letters[ret.start():ret.end()])
        text = text.replace(num, cn2an.an2cn(num))
        ret = pattern_number.search(text)
        letters = [x for x in text]
    return text


def convert_phone_number(text: str):
    letters = [x for x in text]
    ret = pattern_phone.search(text)
    while ret is not None:
        for i in range(ret.span()[0], ret.span()[1]):
            if letters[i] in number:
                letters[i] = NUM_DICT[text[i]]
        ret = pattern_phone.search(''.join(letters))
    return "".join(letters)


def convert_data_number(text: str):
    letters = [x for x in text]
    ret = pattern_date.search(text)
    while ret is not None:
        for i in range(ret.span()[0], ret.span()[1]):
            if letters[i] in number:
                letters[i] = NUM_DICT[text[i]]
        ret = pattern_date.search(''.join(letters))
    return "".join(letters)


def convert_number(text: str):
    text = convert_data_number(text)
    text = convert_phone_number(text)
    text = convert_normal_number(text)
    return text



