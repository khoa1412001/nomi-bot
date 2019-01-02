import random

def_res='Sorry, now I can\'t understand what you just said but `don\'t worry`, I learn everyday.'
alternative_word={}
request={}
request_type={}
result={}
cmd_response={}

def read_alternative_word(file_name):
    f=open(file_name, 'r')
    lines=f.readlines()
    f.close()
    dic={}
    for line in lines:
        temp=line[:-1].split('::')
        key=temp[0]
        dic[key]=temp[1].split(' ')
    global alternative_word
    alternative_word=dic

def read_request(file_name):
    f=open(file_name, 'r')
    lines=f.readlines()
    f.close()
    dic={}
    dic2={}
    for line in lines:
        temp=line.split(']')
        temp2=temp[0][1:]
        temp3=temp[1].split('::')
        key=temp3[0]
        dic[key]=temp3[1][:-1].split(' ')
        dic2[key]=temp2
    global request
    request=dic
    global request_type
    request_type=dic2

def read_result(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    dic = {}
    for line in lines:
        temp = line[:-1].split('::')
        key = temp[0]
        dic[key] = temp[1].split('|')
    global result
    result = dic
    

def read_cmd_response(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    f.close()
    dic = {}
    for line in lines:
        temp = line[:-1].split('::')
        key = temp[0]
        dic[key] = temp[1].split('|')
    global cmd_response
    cmd_response = dic


def create_req(string):
    temp = string.lower().split()
    word = temp[0]
    if word.startswith('<@'):
        temp = temp[1:]
    new_string = ' '.join(temp)
    req = new_string.split()
    return req


def req_to_res(string):
    req = create_req(string)
    req_len = {}
    count = {}
    for key in request:
        req_len[key] = len(request[key])
        count[key] = 0
    signs = []
    words = []
    for word in req:
        if len(word) > 3 and word[-3:] in ['...']:
            words.append(word[:-3])
            signs.append(word[-3:])
        elif len(word) > 2 and word[-2:] in ['!?','~~']:
            words.append(word[:-2])
            signs.append(word[-2:])
        elif len(word) > 1 and word[0] in ['•','*','-','+',"'",'"','(','[','{']:
            words.append(word[1:])
            signs.append(word[0])
        elif len(word) > 1 and word[-1] in [',','?','.','!',';',':',"'",'"',')',']','}']:
            words.append(word[:-1])
            signs.append(word[-1])
        else:
            words.append(word)
    for key in request:
        for word_request in request[key]:
            for word in words:
                if word == word_request:
                    count[key] += 1
                else:
                    if word_request in alternative_word:
                        if word in alternative_word[word_request]:
                            count[key] += 1
            for sign in signs:
                if sign == word_request:
                    count[key] += 1 
    max_key = max(count, key = count.get)
    max_count = count[max_key]
    max_keys = [key for key in count if count[key] == max_count]
    res = default_res
    if len(req) == 0:
        res = random.choice(['Type something please.','Why did you mention me?','What did you mention me for?'])
    elif max_count == 0:
        res = default_res
    elif len(max_keys) == 1:
        res = random.choice(result[max_key])
    elif len(max_keys) > 1:
        count_ratio = 0.0
        for key in count:
            temp = count[key] / req_len[key]
            if temp > count_ratio:
                count_ratio = temp
                res = random.choice(result[key])
        if count_ratio == 0.0:
            res = default_res
    else:
       res = default_res
    return res


def command_response(key):
    res = random.choice(cmd_response[key])
    return res


read_alternative_word('data/alternative_word.nomi')
read_request('data/request.nomi')
read_result('data/result.nomi')
read_cmd_response('data/cmd_response.nomi')
