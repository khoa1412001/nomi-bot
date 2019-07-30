from modules import webhook
from bs4 import BeautifulSoup
import urllib.request
import random

def get_latest_notice():
  global some_notices
  return some_notices[random.choice([0,1,2])]

def get_latest_update():
  global some_updates
  return some_updates[random.choice([0,1,2])]

def get_latest_event():
  global some_events
  return some_events[random.choice([0,1,2])]

def get_latest_notices():
  global soup_notice
  tags = soup_notice.find_all('a')
  global some_notices
  some_notices = []
  for tag in tags:
    link = tag.get('href')
    if (link is not None) and (link.startswith('/News/Notice/')):
      if (not link.endswith('/All')) and (not link.endswith('/Notice')) and (not link.endswith('/Inspection')):
        url = 'https://maplestory.nexon.com' + link
        if (url not in some_notices):
          some_notices.append(url)

def get_latest_updates():
  global soup_update
  tags = soup_update.find_all('a')
  global some_updates
  some_updates = []
  for tag in tags:
    link = tag.get('href')
    if (link is not None) and (link.startswith('/news/update/')):
      url = 'https://maplestory.nexon.com' + link
      if (url not in some_updates):
        some_updates.append(url)

def get_latest_events():
  global soup_event
  tags = soup_event.find_all('a')
  global some_events
  some_events = []
  for tag in tags:
    link = tag.get('href')
    if (link is not None) and (link.startswith('/News/Event/Ongoing/')):
      url = 'https://maplestory.nexon.com' + link
      if (url not in some_events):
        some_events.append(url)

def get_soups():
  headers = { 'User-Agent': webhook.USER_AGENT }

  url = 'https://maplestory.nexon.com/News/Notice'
  request = urllib.request.Request(url, headers = headers)
  response = urllib.request.urlopen(request)
  html = response.read()
  global soup_notice
  soup_notice = BeautifulSoup(html, 'html.parser')
  get_latest_notices()

  url = 'https://maplestory.nexon.com/News/Update'
  request = urllib.request.Request(url, headers = headers)
  response = urllib.request.urlopen(request)
  html = response.read()
  global soup_update
  soup_update = BeautifulSoup(html, 'html.parser')
  get_latest_updates()

  url = 'https://maplestory.nexon.com/News/Event'
  request = urllib.request.Request(url, headers = headers)
  response = urllib.request.urlopen(request)
  html = response.read()
  global soup_event
  soup_event = BeautifulSoup(html, 'html.parser')
  get_latest_events()