from modules import talking_nomi

def read_requests():
  f = open('modules/talking_nomi/data/requests.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    talking_nomi.all_reqs[key] = value

def read_response():
  f = open('modules/talking_nomi/data/responses.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    talking_nomi.all_ress[key] = value

def read_request_to_response():
  f = open('modules/talking_nomi/data/request_to_response.nomi', 'r')
  lines = f.readlines()
  f.close()
  for line in lines:
    str_split = line.split('::')
    key = str_split[0]
    value = str_split[1].split('||')
    talking_nomi.req_to_res[key] = value