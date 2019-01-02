import urllib.request


def jav():
    data = urllib.request.urlopen('http://watch8x.com').read().decode('utf-8')
    stream_url = ''
    temp = data
    while '\'http://' in temp:
        start = temp.index('\'http://')
        temp = temp[start + 1:]
        end = temp.index('\'')
        url = temp[:end]
        temp = temp[end + 1:]
        if url.endswith('.aspx'):
            stream_url = url
            break
    image_url = ''
    temp = data
    while '\'http://' in temp:
        start = temp.index('\'http://')
        temp = temp[start + 1:]
        end = temp.index('\'')
        url = temp[:end]
        temp = temp[end + 1:]
        if url.endswith('ps.jpg'):
            image_url = url
            break
    temp = stream_url.split('/')[3][6:]
    code = temp[:temp.index('-')]
    dic = {}
    dic['code'] = code
    dic['stream_url'] = stream_url
    dic['image_url'] = image_url
    return dic
