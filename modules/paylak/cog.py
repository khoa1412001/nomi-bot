from discord.ext import commands
import asyncio, discord
from modules import paylak

class PayLak(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.music_guilds = {}

  def find_objects(self):
    guilds = self.bot.guilds
    for guild in guilds:
      self.music_guilds[guild.id] = paylak.MusicGuild(guild)

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_objects()
    loop = asyncio.get_event_loop()
    loop.create_task(self.on_music_update())

  async def on_music_update(self):
    await self.bot.wait_until_ready()
    while not discord.opus.is_loaded():
      await asyncio.sleep(1)
    print('opus is loaded')
    while True:
      for id in self.music_guilds:
        guild = self.music_guilds[id]
        if guild.master.voice_client:
          if len(guild.master.voice_client.channel.members) == 1:
            await guild.master.voice_client.disconnect()
            continue
          if not guild.master.voice_client.is_playing():
            if not guild.is_playing:
              if guild.current < len(guild.playlist):
                temp = guild.playlist[guild.current]
                song = await paylak.Song.from_url(url = temp.url, loop = self.bot.loop, stream = guild.stream)
                guild.master.voice_client.play(song)
                if guild.text_channel is not None:
                  await guild.text_channel.send(f'Now playing `{song.title}`.')
                guild.is_playing = True
            else:
              if not guild.loop:
                guild.current += 1
              guild.is_playing = False
      await asyncio.sleep(2)

  @commands.command(aliases = ['q', 'playlist', 'list'])
  async def queue(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    if len(guild.playlist) > 0:
      index = 0
      text = ''
      for song in guild.playlist:
        text += f'[{index}] song.title [{song.duration}]\n'
      text = '```\n' + text + '```'
      await ctx.send(text)
    else:
      await ctx.send('There is no song in queue now.')

  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice:
      channel = ctx.author.voice.channel
      if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
        await ctx.send(f'Moved to `{channel.name}`.')
      else:
        await channel.connect()
        await ctx.send(f'Joined `{channel.name}`.')
    else:
      await ctx.send('Error: you are not in any voice channel.')

  @commands.command()
  async def leave(self, ctx):
    if ctx.author.voice and ctx.voice_client:
      if (ctx.author.voice.channel == ctx.voice_client.channel):
        await ctx.voice_client.disconnect()
        await ctx.send('Left voice.')
      else:
        await ctx.send('Error: you are in another voice channel.')
    else:
      await ctx.send('Error: you or me are not in voice.')

  @commands.command(aliases = ['play', 'p'])
  async def add(self, ctx, *, url):
    guild = self.music_guilds[ctx.guild.id]
    async with ctx.typing():
      song = await paylak.Song.from_url(url, loop = self.bot.loop, stream = guild.stream)
    if song.url == 'error':
      await ctx.send('Error: no song found or broken link.')
    else:
      guild.add(song)
      await ctx.send(f'Added to queue: `{song.title} [{song.duration}]`.')
      guild.text_channel = ctx.channel

  @commands.command(aliases = ['delete'])
  async def remove(self, ctx, *, keyword):
    guild = self.music_guilds[ctx.guild.id]
    if keyword[0] in ['0','1','2','3','4','5','6','7','8','9']:
      index = int(keyword)
      song = guild.playlist[index]
      song.cleanup()
      guild.remove(index)
      await ctx.send(f'Removed from queue: `{song.title}`.')

  @commands.command(aliases = ['clean', 'removeall'])
  async def clear(self):
    guild = self.music_guilds[ctx.guild.id]
    for song in guild.playlist:
      song.cleanup()
    guild.clear()
    await ctx.send('Cleared queue.')
        
  @commands.command()
  async def stop(self, ctx):
    if ctx.voice_client.is_playing():
      ctx.voice_client.stop()
      await ctx.send('Stopped.')
    else:
      await ctx.send('Error: there is nothing to stop.')

  @commands.command()
  async def pause(self, ctx):
    if ctx.voice_client.is_paused():
      await ctx.send('Error: voice are already paused.')
    else:
      ctx.voice_client.pause()
      await ctx.send('Paused.')

  @commands.command()
  async def resume(self, ctx):
    if ctx.voice_client.is_paused():
      ctx.voice_client.resume()
      await ctx.send('Resumed.')
    else:
      await ctx.send('Error: voice are not paused to resume.')

  @commands.command(aliases = ['back'])
  async def previous(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    guild.current -= 1
    if guild.current < 0:
      guild.current = 0
    guild.is_playing = False
    if ctx.voice_client.is_playing():
      ctx.voice_client.stop()
    await ctx.send('Backed to previous song.')

  @commands.command(aliases = ['skip', 'forward'])
  async def next(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    guild.current += 1
    if guild.current > len(guild.playlist):
      guild.current = len(guild.playlist)
    guild.is_playing = False
    if ctx.voice_client.is_playing():
      ctx.voice_client.stop()
    await ctx.send('Skipped to next song.')

  @commands.command()
  async def loop(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    guild.loop = not guild.loop
    if guild.loop:
      await ctx.send('Loop is on.')
    else:
      await ctx.send('Loop is off.')

  @commands.command()
  async def stream(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    guild.stream = not guild.stream
    if guild.stream:
      await ctx.send('Stream is on.')
    else:
      await ctx.send('Stream is off.')

  @commands.command(aliases = ['clean', 'restart'])
  async def reset(self, ctx):
    if ctx.voice_client:
      await ctx.voice_client.disconnect()
    guild = self.music_guilds[ctx.guild.id]
    for song in guild.playlist:
      song.cleanup()
    self.music_guilds[ctx.guild.id] = paylak.MusicGuild(ctx.guild)
    await ctx.send('All music data on this server has been reset.')

  @add.before_invoke
  @remove.before_invoke
  @previous.before_invoke
  @next.before_invoke
  @stop.before_invoke
  @pause.before_invoke
  @resume.before_invoke
  async def ensure_voice(self, ctx):
    if not ctx.author.voice:
      await ctx.send('Error: you are not in any voice channel')
      raise commands.CommandError('')
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await channel.connect()
    else:
      await ctx.voice_client.move_to(channel)

def setup(bot):
  bot.add_cog(PayLak(bot))
