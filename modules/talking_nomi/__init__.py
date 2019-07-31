#same word
#same meaning

from modules.talking_nomi import external_resource
import random

all_reqs = {}
all_ress = {}
req_to_res = {}
all_similars = {}

def fix_request(str):
    words = str.split()
    mention = ''
    for word in words:
        if (word.startswith('<@')):
            mention = word
            break
    return str.replace(mention, '')

def return_error():
    global request, response, counts
    return request, response, counts

def before_parse():
    global counts, request, response
    counts = {}
    request = fix_request(request)
    response = ''

def parse_counts():
    max = 0
    for key in counts:
        if counts[key] > temp_max:
            temp_max = counts[key]
    request_keys = []
    for key in counts:
        if counts[key] == temp_max:
            request_keys.append(key)
    global response
    if len(request_keys) > 0:
        response_keys = req_to_res[random.choice(request_keys)]
        response = random.choice(all_ress[random.choice(response_keys)])
    else:
        response = 'not found response'

def count(key, point):
    global counts
    if not key in counts:
       counts[key] = 0.0
    counts[key] += point
    
def parse_word(word):
    for req_key in all_reqs:
        req_data = all_reqs[req_key]
        if word in req_data:
            count(req_key, 1.0)
            continue
        if word in all_similars:
            similar_words = all_similars[word]
            for similar_word in similar_words:
                if similar_word in req_data:
                    count(req_key, 0.8)
                    continue


def parse_sentence(sentence):
    global request
    request = sentence
    before_parse()
    if (request != ''):
        words = request.lower().split()
        for word in words:
            parse_word(word)
        parse_counts()
    else:
        global response
        response = 'wut?'
    return response

external_resource.read_requests()
external_resource.read_response()
external_resource.read_request_to_response()
external_resource.read_similars()
