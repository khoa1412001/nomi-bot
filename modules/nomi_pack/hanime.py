import random 

urls = []

def load():
    f = open('resources/hanime_pack.nomi', 'r')
    lines = f.readlines()
    f.close()
    global urls
    for line in lines:
        url = line[:-1]
        urls.append(url)

def get_random():
    global urls
    return random.choice(urls)

load()
