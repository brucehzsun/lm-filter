import kenlm
import nlp
from pycorrector import Corrector


# # 加载训练好的kenlm模型
# model = Corrector(language_model_path='data/wiki_zh.bin')
#
# # 文本纠错
# corrected_sent, detail = model.correct('真麻烦你了。希望你们好好的跳无')
# print(corrected_sent)
# print(detail)

def kenlm_score(text: str, model: kenlm.LanguageModel):
    sentence = [x for x in text]
    sen = ' '.join(sentence)
    print(f"{text}, {model.score(sen)}")


def kenlm_full_score(text: str, model: kenlm.LanguageModel):
    sentence = [x for x in text]
    sentence = ' '.join(sentence)

    total = 0.0
    s_list = ['<s>']
    for x in text:
        s_list.append(x)
    s_list.append('</s>')
    for i, (prob, ngram_length, oov) in enumerate(model.full_scores(sentence)):
        # for prob, ngram_length, oov in model.full_scores(sen, bos=True, eos=True):
        print(f"{s_list[i]},prob={prob},ngram_length={ngram_length},oov={oov}")
        total += prob
    print(f"{text} => {total}")


if __name__ == '__main__':
    model = kenlm.LanguageModel('data/wiki_zh.bin')  # model=kenlm.LanguageModel('test.bin')一样的
    sentences = ["滚滚长江东逝水", "长江滚滚水东逝", "长滚江水东滚逝", '真麻烦你了,希望你们好好的跳无', '真麻烦你了,希望你们好好的跳舞']
    for text in sentences:
        kenlm_score(text, model)
        kenlm_full_score(text, model)
        print("")
