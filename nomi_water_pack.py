import os, urllib.request, random


anwp = []
unwp = []


def download_and_read(url):
    urllib.request.urlretrieve(url, 'temp')
    f = open('temp', 'r')
    lines = f.readlines()
    f.close()
    os.remove('temp')
    url_list = []
    for line in lines:
        url_list.append(line[:-1])
    return url_list
    
    
def asia_pack(num):
    return random.sample(anwp, num)
    
    
def us_uk_pack(num):
    return random.sample(unwp, num)
    
    
anwp = download_and_read('https://www.dropbox.com/s/jzhj8wghcn6a4mv/anwp.txt?dl=1')
unwp = download_and_read('https://www.dropbox.com/s/1pnqdbytqmzjfxb/unwp.txt?dl=1')
