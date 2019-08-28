from discord.ext import commands
import asyncio
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
                song = await paylak.Song.from_url(url = temp.url, loop = self.bot.loop, stream = guild.stream, volume = guild.volume)
                guild.master.voice_client.play(song)
                guild.is_playing = True
            else:
              if not guild.loop:
                guild.current += 1
              guild.is_playing = False
      await asyncio.sleep(2)

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

  @commands.command()
  async def play(self, ctx, *, url):
    guild = self.music_guilds[ctx.guild.id]
    async with ctx.typing():
      song = await paylak.Song.from_url(url, loop = self.bot.loop, stream = guild.stream, volume = guild.volume)
    guild.add(song)
    await ctx.send(f'Added to queue: `{song.title} [{song.duration}]`.')

  @commands.command()
  async def stop(self, ctx):
    if ctx.voice_client.is_playing():
      ctx.voice_client.stop()
    else:
      await ctx.send('Error: there is nothing to stop.')

  @commands.command()
  async def pause(self, ctx):
    if ctx.voice_client.is_paused():
      await ctx.send('Error: voice are already paused.')
    else:
      ctx.voice_client.pause()

  @commands.command()
  async def resume(self, ctx):
    if ctx.voice_client.is_paused():
      ctx.voice_client.resume()
    else:
      await ctx.send('Error: voice are not paused to resume.')

  @commands.command()
  async def skip(self, ctx):
    if ctx.voice_client.is_playing():
      ctx.voice_client.stop()
    guild = self.music_guilds[ctx.guild.id]
    guild.current += 1
    guild.is_playing = False
    await ctx.send('Skipped.')

  @commands.command()
  async def loop(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    guild.loop = not guild.loop
    if guild.loop:
      await ctx.send('Loop is `on`.')
    else:
      await ctx.send('Loop is `off`.')

  @commands.command()
  async def stream(self, ctx):
    guild = self.music_guilds[ctx.guild.id]
    guild.stream = not guild.stream
    if guild.stream:
      await ctx.send('Stream is `on`.')
    else:
      await ctx.send('Stream is `off`.')

  @commands.command()
  async def reset(self, ctx):
    if ctx.voice_client:
      await ctx.voice_client.disconnect()
    self.music_guilds[ctx.guild.id] = paylak.MusicGuild(guild)
    await ctx.send('All music data has been reset.')

  @play.before_invoke
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
