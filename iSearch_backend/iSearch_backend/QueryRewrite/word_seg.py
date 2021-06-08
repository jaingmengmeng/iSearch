import os
import re
import string
import unicodedata
import jieba
from zhon.hanzi import punctuation

class Word_Segment:
    def __init__(self, path='./resources/stopwords.txt'):
        # from nltk.corpus import stopwords
        # stop_words = stopwords.words('english')
        self.stop_words = self.result = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]

    def word_segment(self, text):
        seg = jieba.lcut_for_search(text.strip(), HMM=True)
        result = []
        for word in seg:
            if word not in self.stop_words and not self.is_number(word) and not self.is_special(word) and not self.has_punc(word):
                result.append(word)
        return result

    def is_special(self, s):
        try:
            if re.search(r'[a-zA-Z\s]', s) != None and len(s)==1:
                return True
        except:
            pass
        return False

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def has_punc(self, s):
        if re.search(r'[%s]+' % (punctuation + string.punctuation), s) != None:
            return True
        return False