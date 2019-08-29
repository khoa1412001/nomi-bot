import random

all_reqs = {}
all_ress = {}
req_to_res = {}
all_similars = {}

def read(name):
  f = open(f'modules/chitchat/resources/{name}.nomi', 'r')
  lines = f.readlines()
  f.close()
  dic = {}
  for line in lines:
    line = line[:-1].split('::')
    key = line[0]
    value = line[1].split('||')
    dic[key] = value
  return dic

def prepare():
  global all_reqs, all_ress, req_to_res, all_similars
  all_reqs = read('requests')
  all_ress = read('responses')
  req_to_res = read('request_to_response')
  all_similars = read('similars')

class Logic():
  def __init__(self, req):
    self.request = self.remove_mention_and_space(req)
    self.response = 'not found response'
    self.counts = {}
    self.parse_sentence(self.request)

  def remove_mention_and_space(self, text):
    words = text.split()
    mention = ''
    for word in words:
        if (word.startswith('<@')):
            mention = word
            break
    text = text.replace(mention, '')
    return ' '.join(text.split())

  def parse_counts(self):
    for key in self.counts:
      value = self.counts[key] / len(all_reqs[key])
      self.counts[key] = round(value, 4)
    max_count = 0
    for key in self.counts:
      if self.counts[key] > max_count:
        max_count = self.counts[key]
    keys = []
    for key in self.counts:
      if self.counts[key] == max_count:
        keys.append(key)
    if self.request == '':
      self.response = random.choice(all_ress['res0'])
    elif len(keys) > 0:
      response_keys = req_to_res[random.choice(keys)]
      self.response = random.choice(all_ress[random.choice(response_keys)])

  def give_point(self, key, point):
    if not key in self.counts:
       self.counts[key] = 0.0
    self.counts[key] += point
    
  def parse_word(self, word):
    if word[-1] in [',','.','?','!',';',':','"','\'']:
      word = word[:-1]
    for key in all_reqs:
      if word in all_reqs[key]:
        self.give_point(req_key, 1.0)   
      else:
        for similar_word in all_similars:
          if (word in all_similars[similar_word]) and (similar_word in all_reqs[key]):
            self.give_point(req_key, 0.8)

  def parse_sentence(self, sentence):
    words = self.request.lower().split()
    for word in words:
        self.parse_word(word)
    self.parse_counts()
