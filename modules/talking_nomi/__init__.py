#same word
#same meaning

from modules.talking_nomi import external_resource
import random

all_reqs = {}
all_ress = {}
req_to_res = {}
all_similars = {}

def fix_request(text):
    words = text.split()
    mention = ''
    for word in words:
        if (word.startswith('<@')):
            mention = word
            break
    text = text.replace(mention, '')
    return ' '.join(text.split())

def return_error():
    global request, response, counts
    return request, response, counts

def before_parse():
    global counts, request, response
    counts = {}
    request = fix_request(request)
    response = ''

def parse_counts():
    for key in counts:
        value = counts[key] / len(all_reqs[key])
        counts[key] = round(value, 4)
    max_count = 0
    for key in counts:
        if counts[key] > max_count:
            max_count = counts[key]
    keys = []
    for key in counts:
        if counts[key] == max_count:
            keys.append(key)
    global request, response
    if request == '':
        response = random.choice(['What?', 'Wut?', 'Nani?', 'Hello?', 'nAni dEsu kA?'])
    elif len(keys) > 0:
        response_keys = req_to_res[random.choice(keys)]
        response = random.choice(all_ress[random.choice(response_keys)])
    else:
        response = 'not found response'

def count(key, point):
    global counts
    if not key in counts:
       counts[key] = 0.0
    counts[key] += point
    
def parse_word(word):
    if word[-1] in [',','.','?','!',';',':','"','\'']:
        word = word[:-1]
    for req_key in all_reqs:
        req_data = all_reqs[req_key]
        if word in req_data:
            count(req_key, 1.0)
        else:
            if word in all_similars:
                similar_words = all_similars[word]
                for similar_word in similar_words:
                    if similar_word in req_data:
                        count(req_key, 0.8)

def parse_sentence(sentence):
    global request
    request = sentence
    before_parse()
    words = request.lower().split()
    for word in words:
        parse_word(word)
    parse_counts()
    global response
    return response

external_resource.read_requests()
external_resource.read_response()
external_resource.read_request_to_response()
external_resource.read_similars()
