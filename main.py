from discord.ext import commands
import discord, os, random, asyncio
from modules import water_pack, chitchat, paylak

token = os.getenv('token')
prefix_char = '#'
bot = commands.Bot(
  command_prefix = prefix_char
)

async def on_music_update():
  await bot.wait_until_ready()
  while True:
    p = paylak.p
    for guild in p.queue:
      if guild.voice_client:
        if not guild.voice_client.is_playing():
          if not p.is_playing[guild]:
            if p.cur_song_index[guild] < len(p.queue[guild]):
              song = p.queue[guild][p.cur_song_index[guild]]
              guild.voice_client.play(song)
              print(song.title)
              p.is_playing[guild] = True
          else:
            p.cur_song_index[guild] += 1
            p.is_playing[guild] = False
    await asyncio.sleep(1)

@bot.event
async def on_ready():
  await bot.change_presence(
    activity = discord.Activity(
      type = discord.ActivityType.watching,
      name = 'NTR hentai'
    ),
    status = discord.Status.do_not_disturb
  )
  loop = asyncio.get_event_loop()
  loop.create_task(on_music_update())

@bot.event
async def on_message(message):
  if (message.author.id != bot.user.id):
    if (len(message.mentions) == 1) and (bot.user.mentioned_in(message)):
      async with message.channel.typing():
        delay_time = random.choice(range(45, 100)) / 100.0
        await asyncio.sleep(delay_time)
      logic = chitchat.Logic(message.content)
      req, res, cou = logic.request, logic.response, logic.counts
      if (res == 'not found response'):
        str = (
          '```[ERROR]```'
          f'No response found.\n'
          f'request: {req}\n'
        )
        cog = bot.get_cog('NomiHostData')
        await cog.my_channels['talking'].send(str)
      else:
        await message.channel.send(f'{message.author.mention} {res}')
        str = (
          '```[DEBUG]```'
          f'request: {req}\n'
          f'response: {res}\n'
          f'counts: {cou}\n'
        )
        cog = bot.get_cog('NomiHostData')
        await cog.my_channels['talking'].send(str)
  if (message.content.startswith(prefix_char)):
    await bot.process_commands(message)

@bot.command()
async def join(ctx):
  if ctx.author.voice:
    channel = ctx.author.voice.channel.connect()
    if ctx.voice_clien.channel is not None:
      await ctx.voice_client.move_to(channel)
      await ctx.send(f'Moved to `{channel.name}`.')
    else:
      await channel.connect()
      await ctx.send(f'Joined `{channel.name}`.')
  else:
    await ctx.send('Error: you are not in any voice channel.')

@bot.command()
async def leave(ctx):
  if ctx.author.voice and ctx.voice_client:
    if (ctx.author.voice.channel == ctx.voice_client.channel):
      await ctx.voice_client.disconnect()
      await ctx.send('Left voice.')
    else:
      await ctx.send('Error: you are in another voice channel.')
  else:
    await ctx.send('Error: you or me are not in voice.')

@bot.command()
async def play(ctx, *, url):
  async with ctx.typing():
    song = await paylak.Song.from_url(url, loop=bot.loop)
    paylak.p.add(ctx.guild, song)
  await ctx.send(f'Added to queue: {song.title}.')

@bot.command()
async def stop(ctx):
  if ctx.voice_client.is_playing():
    await ctx.voice_client.stop()

@bot.command()
async def pause(ctx):
  if ctx.voice_client.is_paused():
    await ctx.send('Error: voice are already paused.')
  else:
    await ctx.voice_client.stop()

@bot.command()
async def resume(ctx):
  if ctx.voice_client.is_playing():
    await ctx.voice_client.resume()
  else:
    await ctx.send('Error: voice are not paused to resume.')

@play.before_invoke
async def ensure_voice(ctx):
  if ctx.voice_client is None:
    if ctx.author.voice:
      await ctx.author.voice.channel.connect()
    else:
      await ctx.send('Error: you are not connected to a voice channel.')
      raise commands.CommandError('Author not connected to a voice channel.')

chitchat.prepare()
water_pack.prepare()
paylak.prepare()
bot.load_extension('servers.nomi-host-data')
bot.load_extension('servers.umbra')
bot.load_extension('servers.asteria')
bot.run(token)
