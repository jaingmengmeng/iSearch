from gensim.models import word2vec
from .word_seg import Word_Segment
from .AutoCorrecterr4Chinese import AutoCorrecter
import os
from tqdm import tqdm


class QueryRewrite():

    '''
    stopwords_path: 停用词表路径
    file_path: 所有文档的文件夹路径,用于训练模型，如果模型已经训练好就不需要输入了
    dict_path: 所有文档的词频词典路径
    model_path: 模型保存和读取的路径
    cn_dict_path: 中文词词典路径
    '''

    def __init__(self, stopwords_path, file_path=None, dict_path="./resources/word_freq.json", model_path='./model/word2vec.model', cn_dict_path="./resources/cn_dict.txt"):
        self.file_path = file_path
        self.stopwords_path = stopwords_path
        self.model_path = model_path
        self.dict_path = dict_path
        self.segmenter = Word_Segment(stopwords_path)
        self.autocorrecter = AutoCorrecter(
            self.segmenter, self.dict_path, self.file_path, cn_dict_path)
        # print(self.stopwords)
        if not os.path.exists(self.model_path):
            self.train()
        self.model = word2vec.Word2Vec.load(self.model_path, allow_pickle=True)

    def train(self):
        print('start training...')
        docs = []
        if self.file_path is None:
            print("please input the path of whole docments!")
        for fname in tqdm(os.listdir(self.file_path)):
            with open(os.path.join(self.file_path, fname)) as f:
                text = ''.join(f.read().strip().split('\n'))
            docs.append(self.segmenter.word_segment(text))
        # docs = MyDocs(self.file_path, self.segmenter)
        model = word2vec.Word2Vec(docs, min_count=1, window=3)

        print('training complete...')
        model.save(self.model_path)

    def normal_extract(self, query):
        '''
        去除停用词的普通模式,包含自动纠错
        '''
        query = self.autocorrecter.auto_correct_sentence(query)
        result = self.segmenter.word_segment(query)
        return " ".join(result)

    def comprehensive_extract(self, query):
        '''
        利用word2vec进行相关词检索的增强模式，包含自动纠错
        返回：修正过后的query， 前十个相关词， 增强后的关键词
        '''
        corrected_query = self.autocorrecter.auto_correct_sentence(query)
        words = self.segmenter.word_segment(corrected_query)
        similar_words = self.model.wv.most_similar(words, topn=3)
        similar_words = list(map(lambda x: x[0], similar_words))
        associate_words = list(
            map(lambda x: x[0], self.model.wv.most_similar(words, topn=100)))
        # print(similar_words)
        return (corrected_query, associate_words, " ".join(words+similar_words))


# 输入你的停用词文件位置、词频词典位置、所有doc的位置、模型位置以及中文词典的位置
# qr = QueryRewrite(stopwords_path='./resources/stopwords.txt', file_path="./files", dict_path="./resources/word_freq.json", model_path='./model/word2vec.model', cn_dict_path="./resources/cn_dict.txt")
# print('Query: 元气森林白讨含糖量！')
# print('normal mode:', qr.normal_extract('元气森林白讨含糖量！'))
# print('advanced mode:', qr.comprehensive_extract('元气森林白讨含糖量！'))
