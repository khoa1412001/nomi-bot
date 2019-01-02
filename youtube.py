import utils,urllib.request

def search(query):
    url='https://youtube.com/results?search_query={}'.format(query)
    headers={ 
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Safari/537.36'
    }
    req=urllib.request.Request(url,headers=headers)
    data=urllib.request.urlopen(req).read().decode()
    url_list=[]
    while '"/watch?' in data:
        start=data.index('"/watch?')
        data=data[start+10:]
        end=data.index('"')
        url=data[:end]
        if 'list=' not in url:
            url_list.append('https://youtu.be/' + url)
        data=data[end+1:]
    return url_list

utils.variables['youtube_results']=[]
