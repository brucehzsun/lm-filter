import os

if __name__ == '__main__':
    titles = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z']
    with open("CET4.txt", 'r') as f, open("../cet4_dict.txt", 'w') as writer:
        result = []
        for line in f.readlines():
            if line.strip() == '':
                continue
            line = line.replace('\n', '')
            if line in titles:
                continue
            words = line.split(' ')
            result.append(words[0])
            writer.write(words[0].lower()+"\n")

        # writer.writelines(result)