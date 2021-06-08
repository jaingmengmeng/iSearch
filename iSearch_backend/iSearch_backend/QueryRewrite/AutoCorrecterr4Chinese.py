# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import pinyin
import jieba
import string
import re
import json
import os
from collections import Counter
from tqdm import tqdm


class AutoCorrecter():
    def __init__(self, segmenter, dict_path="./resources/word_freq.json", file_path="./files", cn_dict_path="./resources/cn_dict.txt"):

        self.FILE_PATH = file_path
        self.PUNCTUATION_LIST = string.punctuation
        self.PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）"
        self.segmenter = segmenter
        self.dict_path = dict_path
        self.cn_dict_path = cn_dict_path
        if not os.path.exists(self.dict_path):
            self.construct_dict(self.FILE_PATH)
        with open(self.dict_path, "r", encoding="utf-8") as f:
            self.phrase_freq = json.load(f)

    def construct_dict(self, file_path):

        word_freq = Counter()

        for fname in tqdm(os.listdir(file_path)):
            dfs = 12
            with open(os.path.join(file_path, fname)) as f:
                text = ''.join(f.read().strip().split('\n'))
                words = self.segmenter.word_segment(text)
            word_freq.update(words)

        with open(self.dict_path, 'w', encoding='utf-8') as f:
            json.dump(dict(word_freq), f)

    def load_cn_words_dict(self, file_path):
        cn_words_dict = ""
        with open(file_path, "r") as f:
            for word in f:
                cn_words_dict += word.strip().encode("utf-8").decode("utf-8")
        return cn_words_dict

    def edits1(self, phrase, cn_words_dict):
        "All edits that are one edit away from `phrase`."
        phrase = phrase.encode("utf-8").decode("utf-8")
        splits = [(phrase[:i], phrase[i:]) for i in range(len(phrase) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:]
                    for L, R in splits if R for c in cn_words_dict]
        inserts = [L + c + R for L, R in splits for c in cn_words_dict]
        return set(deletes + transposes + replaces + inserts)

    def known(self, phrases):
        return set(phrase for phrase in phrases if phrase.encode("utf-8").decode("utf-8") in self.phrase_freq)

    def get_candidates(self, error_phrase, cn_dict_path):

        candidates_1st_order = []
        candidates_2nd_order = []
        candidates_3nd_order = []

        error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/")
        cn_words_dict = self.load_cn_words_dict(cn_dict_path)
        candidate_phrases = list(self.known(
            self.edits1(error_phrase, cn_words_dict)))

        for candidate_phrase in candidate_phrases:
            candidate_pinyin = pinyin.get(
                candidate_phrase, format="strip", delimiter="/").encode("utf-8").decode("utf-8")
            if candidate_pinyin == error_pinyin:
                candidates_1st_order.append(candidate_phrase)
            elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
                candidates_2nd_order.append(candidate_phrase)
            else:
                candidates_3nd_order.append(candidate_phrase)

        return candidates_1st_order, candidates_2nd_order, candidates_3nd_order

    def auto_correct(self, error_phrase):

        c1_order, c2_order, c3_order = self.get_candidates(
            error_phrase, self.cn_dict_path)
        # print c1_order, c2_order, c3_order
        if c1_order:
            return max(c1_order, key=self.phrase_freq.get)
        elif c2_order:
            return max(c2_order, key=self.phrase_freq.get)
        else:
            return max(c3_order, key=self.phrase_freq.get)

    def auto_correct_sentence(self, error_sentence, verbose=False):

        jieba_cut = jieba.cut(error_sentence.encode(
            "utf-8").decode("utf-8"), cut_all=False)
        seg_list = "\t".join(jieba_cut).split("\t")

        correct_sentence = ""

        for phrase in seg_list:

            correct_phrase = phrase
            # check if item is a punctuation
            if phrase not in self.PUNCTUATION_LIST.encode("utf-8").decode("utf-8") and re.search(r'[a-zA-Z0-9]', phrase) is None:
                # check if the phrase in our dict, if not then it is a misspelled phrase
                if phrase.encode("utf-8").decode("utf-8") not in self.phrase_freq.keys():
                    correct_phrase = self.auto_correct(
                        phrase.encode("utf-8").decode("utf-8"))
                    if verbose:
                        print(phrase, correct_phrase)

            correct_sentence += correct_phrase

        return correct_sentence


# if __name__=="__main__":
# 	from word_seg import Word_Segment

# 	autocorrecter = AutoCorrecter(Word_Segment('stopwords.txt'))

# 	err_sent_1 = '白讨元气森林'
# 	print("Test case 1:")
# 	correct_sent = autocorrecter.auto_correct_sentence(err_sent_1, True)
# 	print("original sentence:" + err_sent_1 + "\n==>\n" + "corrected sentence:" + correct_sent)
