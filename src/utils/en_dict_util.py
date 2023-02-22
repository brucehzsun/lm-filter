import os

def read_en_dict(path: str):
    en_dict = {}
    with open(path) as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            en_dict[line] = True
    return en_dict