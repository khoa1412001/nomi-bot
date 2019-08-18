import youtube_dl

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

def prepare():
  if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')
  ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Song(discord.PCMVolumeTransformer):
  def __init__(self, source, *, data, volume = 1.0):
    super().__init__(source, volume)
    self.data = data
    self.title = data['title']
    self.url = data['url']
    self.duration = data['duration']

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):
      loop = loop or asyncio.get_event_loop()
      data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
      if 'entries' in data:
        data = data['entries'][0]
      filename = data['url'] if stream else ytdl.prepare_filename(data)
      return cls(discord.FFmpegPCMAudio(filename, options = '-vn'), data=data)

class Player():
  queue = []
  volume = 1.0
  
  def add(self, song):
    queue.append(song)

  def remove(self, index):
    if (index > -1) and (index < len(queue)):
      queue.pop(index)
  
  def clear(self):
    queue = []
