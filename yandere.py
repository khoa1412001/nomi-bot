import urllib.request, json, random


safe_max_page = 234701
explicit_max_page = 38901


def safe(num):
    urls = []
    pages = random.sample(range(1, safe_max_page), num)
    for page in pages:
        url_str = 'https://yande.re/post.json?tags=rating:safe&limit=1&page={}'.format(page)
        data = json.loads(urllib.request.urlopen(url_str).read().decode())
        urls.append(data[0]['file_url'])
    return urls


def explicit(num):
    urls = []
    pages = random.sample(range(1, explicit_max_page), num)
    for page in pages:
        url_str = 'https://yande.re/post.json?tags=rating:explicit&limit=1&page={}'.format(page)
        data = json.loads(urllib.request.urlopen(url_str).read().decode())
        urls.append(data[0]['file_url'])
    return urls
