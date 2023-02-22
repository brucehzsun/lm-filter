import os


def merger_wik(path: str, corpus: str):
    count = 0
    path = os.path.join(path, corpus)
    with open(path + ".txt", 'w') as writer:
        for file_name in os.listdir(path):
            with open(os.path.join(path, file_name), 'r') as f:
                lines = f.readlines()
                writer.writelines(lines)
                print(f"writer {file_name}, size={len(lines)}")
                count += len(lines)
    print(f"finish, total size = {count}")


if __name__ == '__main__':
    path = "data"
    corpus = 'wiki_zh'
    merger_wik(path, corpus)
