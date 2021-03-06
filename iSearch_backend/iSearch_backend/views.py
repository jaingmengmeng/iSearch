import json

from django.http import HttpResponse
from whoosh.filedb.filestore import FileStorage

from .QueryRewrite import QueryRewrite
from .QueryRewrite.AutoComple import AutoComplete

qr = QueryRewrite.QueryRewrite(
    stopwords_path='./iSearch_backend/QueryRewrite/resources/stopwords.txt',
    model_path='./iSearch_backend/QueryRewrite/model/word2vec.model.bin',
    dict_path="./iSearch_backend/QueryRewrite/resources/word_freq.json",
    cn_dict_path="./iSearch_backend/QueryRewrite/resources/cn_dict.txt"
)

ac = AutoComplete(
    './iSearch_backend/QueryRewrite/resources/word_freq.json',
    './iSearch_backend/QueryRewrite/model/word2vec.model.bin'
)


def myFind(query):
    # print(query)
    ret_result = []
    ix_path = './iSearch_backend/indexdir/'
    ix_name = 'ir_index_name'
    storage = FileStorage(ix_path)
    with storage.open_index(indexname=ix_name).searcher() as searcher:
        results = searcher.find("content", query, limit=None)
        for r in results:
            ret_result.append({
                "url": 'https://www.36kr.com/p/'+r['path'],
                "title": r['title'],
                "abstract": r['abstract']
            })
    return ret_result


def hello(request):
    return HttpResponse("Welcome to iSearch ~")


def mark_red(text, word_list):
    for word in word_list:
        text = text.replace(
            word, '<em style="color: #f73131; font-style: normal;">' + word + '</em>')
    return text


def search(request):
    relevant_num = 30

    query = request.GET.get("q")
    page_size = int(request.GET.get('page_size'))
    page_num = int(request.GET.get('page_num'))

    qr_result = qr.comprehensive_extract(query)
    qr_segment_result = qr.normal_extract(query).split(' ')

    relevant_list = []
    relevant_list = qr_result[1][:relevant_num]

    corrected_query = qr_result[0]
    doc_list = []
    doc_list = myFind(corrected_query)

    for i in range(page_size * (page_num - 1), page_size * page_num):
        if i < len(doc_list):
            doc_list[i]['title'] = mark_red(
                doc_list[i]['title'], qr_segment_result)
            doc_list[i]['abstract'] = mark_red(
                doc_list[i]['abstract'], qr_segment_result)

    res = {
        "corrected_query": corrected_query,
        "doc_list_len": len(doc_list),
        "doc_list": doc_list[page_size * (page_num - 1): page_size * page_num],
        "relevant_list": relevant_list
    }
    return HttpResponse(json.dumps(res, indent=2, ensure_ascii=False))


def autocomplete(request):
    autocomplete_num = 10
    query = request.GET.get("q")
    autocomplete_list = ac.comprehensive_complete(query)[:autocomplete_num]
    return HttpResponse(json.dumps(autocomplete_list, indent=2, ensure_ascii=False))
