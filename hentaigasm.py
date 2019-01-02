import urllib.request


def hentai():
    data = urllib.request.urlopen('http://hentaigasm.com/?orderby=rand').read().decode('utf-8')
    image_url = ''
    temp = data
    while '"http://' in temp:
        start = temp.index('"http://')
        temp = temp[start + 1:]
        end = temp.index('"')
        url = temp[:end]
        temp = temp[end + 1:]
        if url.startswith('http://hentaigasm.com/preview/') and url.endswith('.jpg'):
            image_url = url
            break
    name = image_url[30:][:-4]
    stream_url = 'http://hentaigasm.com/' + '-'.join(name.lower().split())
    image_url = image_url.replace(' ', '%20')
    dic = {}
    dic['name'] = name
    dic['stream_url'] = stream_url
    dic['image_url'] = image_url
    return dic
