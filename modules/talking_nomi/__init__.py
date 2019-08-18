import random

all_reqs = {}
all_ress = {}
req_to_res = {}
all_similars = {}
ready = False

def read_requests():
  global all_reqs
  f = open('modules/talking_nomi/resources/requests.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    line = line[:-1]
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    all_reqs[key] = value

def read_response():
  global all_ress
  f = open('modules/talking_nomi/resources/responses.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    line = line[:-1]
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    all_ress[key] = value

def read_request_to_response():
  global req_to_res
  f = open('modules/talking_nomi/resources/request_to_response.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    line = line[:-1]
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    req_to_res[key] = value

def read_similars():
  global all_similars
  f = open('modules/talking_nomi/resources/similars.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    line = line[:-1]
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    all_similars[key] = value

def prepare():
  read_requests()
  read_responses()
  read_request_to_response()
  read_similars()
  global ready
  ready = True

class Logic():
  request = ''
  response = ''
  count = {}

  def __init__(self, req):
    global ready
    if (ready):
      self.parse_sentence(req)
      if (self.response == 'not found response'):
        print('An no-response logic has been occurred.')
    else:
      print('The external resources is not readied for parsing logic.')

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
      self.response = all_ress['res0']
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
    for req_key in all_reqs:
      req_data = all_reqs[req_key]
      if word in req_data:
        self.give_point(req_key, 1.0)
      else:
        if word in all_similars:
          similar_words = all_similars[word]
          for similar_word in similar_words:
            if similar_word in req_data:
              self.give_point(req_key, 0.8)

  def parse_sentence(self, sentence):
    self.request = remove_mention_and_space(sentence)
    self.response = 'not found response'
    self.count = {}
    words = self.request.lower().split()
    for word in words:
        self.parse_word(word)
    self.parse_counts()
