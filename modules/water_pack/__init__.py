import random 

packs = [
  'hasunoai', 
  'hanime', 
  'ulzzang__girlz', 
  'ulzzang_face', 
  'favorite_asian_girls', 
  'instababes.asian', 
  'vietnamesexybabe', 
  'vneseg', 
  'angels.in.vn', 
  'girl_xinh', 
  'hoingamgaitay', 
  '69pretty.official'
]
o = None

def prepare():
  global o
  o = Ocean()

class River():
  name = ''
  data = []
  
  def __init__(self, name):
    self.name = name
    self.load(name)

  def load(self, name):
    f = open(f'modules/nomi_water_pack/resources/{name}.nomi', 'r')
    urls = f.readlines()
    f.close()
    self.data = []
    for url in urls:
      self.data.append(url[:-1])

  def get_random(self):
    return random.choice(self.data)

class Ocean():
  data = []

  def __init__(self):
    global packs
    for pack_name in packs:
      self.data.append(River(pack_name))
  
  def get_random(self, names):
    indexs = []
    i = 0
    for r in self.data:
      if r.name in names:
        indexs.append(i)
      i += 1
    i = random.choice(indexs)
    return self.data[i].get_random()
