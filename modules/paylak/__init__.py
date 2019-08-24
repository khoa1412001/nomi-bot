import discord, youtube_dl

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl = None
p = None

def prepare():
  global p
  p = Player()
  global ytdl
  ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
  if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')
  
class Song(discord.PCMVolumeTransformer):
  def __init__(self, source, *, volume = 1.0, title, url, duration):
    super().__init__(source, volume)
    self.title = title
    self.url = url
    self.duration = duration

  @classmethod
  async def from_url(cls, url, *, loop = None, stream = False, volume = 1.0):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
    if 'entries' in data:
      data = data['entries'][0]
    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, options = '-vn'), volume = volume, data['title], data['url'], data['duration'])

class Player():
  queue = {}
  cur_song_index = {}
  is_playing = {}
  loop = {}
  stream = {}
  volume = {}

  def init_guild(self, guild):
    if guild not in self.queue:
      self.queue[guild] = []
    if guild not in self.cur_song_index:
      self.cur_song_index[guild] = 0
    if guild not in self.is_playing:
      self.is_playing[guild] = False 
    if guild not in self.loop:
      self.loop[guild] = False
    if guild not in self.stream:
      self.stream[guild] = False
    if guild not in self.volume:
      self.volume[guild] = 1.0
  
  def add(self, guild, song):
    self.queue[guild].append(song)

  def remove(self, guild, index):
    if (guild in queue):
      if (index > -1) and (index < len(queue[guild])):
        self.queue[guild].pop(index)
  
  def clear(self, guild):
    queue[guild] = []

class MusicGuild(discord.Guild):
  playlist = []
  is_playing = False
  options = {
    'loop':False,
    'stream':False,
    'volume':1.0
  }

  def add(self, song):
    for s in self.playlist:
      if s.title == song.title:
        return
    self.playlist.append(song)

  def remove(self, index):
    if (index > -1) and (index < len(self.playlist)):
      self.playlist.pop(index)

  def clear(self):
    self.playlist = []

