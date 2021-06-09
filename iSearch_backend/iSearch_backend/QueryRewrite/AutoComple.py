import json
import jieba
from gensim.models import word2vec, KeyedVectors


class AutoComplete():
    '''
    word_freq: 词频词典路径
    model_path: 模型路径
    '''

    def __init__(self, word_freq_path, model_path):
        self.word_freq_path = word_freq_path
        self.model_path = model_path
        # self.model = word2vec.Word2Vec.load(self.model_path)
        self.model = KeyedVectors.load_word2vec_format(
            self.model_path,
            binary=True
        )
        with open(self.word_freq_path, 'r') as f:
            self.word_freq = json.load(f)
            # print(len(self.word_freq))

    def search_with_prefix(self, prefix):
        candidate_phrases = []

        for item in self.word_freq.items():
            if item[0].startswith(prefix) and len(item[0]) > 1:
                candidate_phrases.append(item)

        candidate_phrases.sort(key=lambda x: x[1], reverse=True)
        candidate_phrases = list(map(lambda x: x[0], candidate_phrases))
        if len(candidate_phrases) > 10:
            candidate_phrases = candidate_phrases[:10]

        return candidate_phrases

    def normal_complete(self, query):
        '''
        仅仅针对最后一个字符，返回改字符开头的词，按词频从高到低排序
        '''
        if len(query) == 0:
            return []

        prefix = query[-1]
        candidate_phrases = self.search_with_prefix(prefix)

        if len(candidate_phrases) == 0:
            return candidate_phrases

        return [query[:-1]+phrase for phrase in candidate_phrases]

    def comprehensive_complete(self, query):
        '''
        使用了jieba分词，对分词结果的最后一个词按词频检索，并且如果分词结果长度>2，还会考虑和前一个词的匹配度
        '''
        if len(query) == 0:
            return []

        phrases = jieba.lcut_for_search(query.strip(), HMM=True)
        candidate_phrases = self.search_with_prefix(phrases[-1])

        if len(phrases) <= 1:
            return candidate_phrases
        else:
            try:
                target_phrase = phrases[-2]
                candidate_phrases.sort(key=lambda x: self.model.similarity(
                    x, target_phrase), reverse=True)
            except:
                pass

        sentences = [phrases[:-1]+[phrase] for phrase in candidate_phrases]
        return [''.join(sentence) for sentence in sentences]

# if __name__ == '__main__':
#     ac = AutoComplete('./QueryRewrite/resources/word_freq.json', './QueryRewrite/model/word2vec.model.bin')
    # print(ac.normal_complete('ceshi'))
    # print(ac.comprehensive_complete('ceshi'))
