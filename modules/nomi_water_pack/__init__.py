import random 

packs = {}

def load(name):
  f = open(f'modules/nomi_water_pack/resources/{name}.nomi', 'r')
  urls = f.readlines()
  f.close()
  global packs
  packs[name] = []
  for url in urls:
    packs[name].append(url[:-1])

def get_random(name):
  global packs
  random.choice(packs[name])

load('hasunoai')
load('hanime')
load('ulzzang_face')
load('favorite_asian_girls')
load('instababes.asian')
