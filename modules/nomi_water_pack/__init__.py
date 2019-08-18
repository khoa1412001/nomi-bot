import random 

packs_name = [
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

class WaterPack():
  packs = {}

  def __init__(self):
    for pack_name in packs_name:
      self.load(pack_name)

  def load(self, name):
    f = open(f'modules/nomi_water_pack/resources/{name}.nomi', 'r')
    urls = f.readlines()
    f.close()
    self.packs[name] = []
    for url in urls:
      self.packs[name].append(url[:-1])

  def get_random_one(self, name):
    return random.choice(self.packs[name])
  
  def get_random(self, names):
    return self.get_random_one(self.packs[random.choice(names)])
