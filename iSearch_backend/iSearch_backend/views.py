import json

from django.http import HttpResponse


def hello(request):
    return HttpResponse("Welcome to iSearch ~")


def Unicode():
    import random
    val = random.randint(0x4e00, 0x9fbf)
    return chr(val)


def search(request):
    query = request.GET.get("q")
    page_size = request.GET.get('page_size')
    page_num = request.GET.get('page_num')

    import random
    length = random.randint(5, 99)
    doc_list = []
    relevant_list = []
    for i in range(length):
        doc_list.append(
            {
                "url": "https://www.baidu.com/",
                "title": ''.join([Unicode() for i in range(random.randint(5, 50))]),
                "abstract": ''.join([Unicode() for i in range(random.randint(5, 500))])
            }
        )
        relevant_list.append(''.join([Unicode()
                             for i in range(random.randint(5, 50))]))
    res = {
        "doc_list": doc_list, "relevant_list": relevant_list
    }

    str_json = json.dumps(res, indent=2, ensure_ascii=False)
    return HttpResponse(str_json)


def autocomplete(request):
    query = request.GET.get("q")

    import random
    length = random.randint(5, 30)
    autocomplete_list = []
    for i in range(length):
        autocomplete_list.append(
            query + ''.join([Unicode() for i in range(random.randint(5, 50))])
        )

    str_json = json.dumps(autocomplete_list, indent=2, ensure_ascii=False)
    return HttpResponse(str_json)
