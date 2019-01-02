import urllib.request, json, random


safe_max_page = 152601
explicit_max_page = 19101


def safe(num):
    urls = []
    pages = random.sample(range(1, safe_max_page), num)
    for page in pages:
        url_str = 'https://konachan.com/post.json?tags=rating:safe&limit=1&page={}'.format(page)
        data = json.loads(urllib.request.urlopen(url_str).read().decode())
        urls.append(data[0]['file_url'])
    return urls


def explicit(num):
    urls = []
    pages = random.sample(range(1, explicit_max_page), num)
    for page in pages:
        url_str = 'https://konachan.com/post.json?tags=rating:explicit&limit=1&page={}'.format(page)
        data = json.loads(urllib.request.urlopen(url_str).read().decode())
        urls.append(data[0]['file_url'])
    return urls
