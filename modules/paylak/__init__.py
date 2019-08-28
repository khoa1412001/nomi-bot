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

def prepare():
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
    return cls(discord.FFmpegPCMAudio(filename, options = '-vn'), volume = volume, title = data['title'], url = url, duration = data['duration'])

class MusicGuild():
  def __init__(self, guild):
    self.id = guild.id
    self.master = guild
    self.playlist = []
    self.current = 0
    self.is_playing = False
    self.loop = False
    self.stream = False
    self.volume = 1.0

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

