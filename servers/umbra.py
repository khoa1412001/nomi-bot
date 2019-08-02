from discord.ext import commands
from modules.webhook import kms
from modules import nomi_water_pack
import discord, asyncio, datetime, pytz, random

class Umbra(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.use_channels = {}
    self.use_roles = {}

  def find_channels(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'Umbra'):
        channels = guild.channels
        for channel in channels:
          self.use_channels[channel.name] = channel
        roles = guild.roles
        for role in roles:
          self.use_roles[role.name] = role
        break

  async def daily_time_handle(self):
    await self.bot.wait_until_ready()
    while (True):
      now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
      if (now.hour in [17] and now.minute in [55]):
        str = f'{self.use_roles["Member"].mention}, Urus in next 5 minutes.'
        await self.use_channels['kms-update'].send(str)
        await asyncio.sleep(60)
      elif (now.hour in [9, 16, 18] and now.minute in [55]):
        str = f'{self.use_roles["Member"].mention}, Flag Race in next 5 minutes.'
        await self.use_channels['kms-update'].send(str)
        await asyncio.sleep(60)
      else:
        await asyncio.sleep(30)

  async def kms_update(self):
    await self.bot.wait_until_ready()
    while (True):
      choice = random.choice([0,1,2])
      if (choice == 0):
        kms.get_soups()
        url = kms.get_latest_notice()
        embed = discord.Embed()
        embed.add_field(
          name = 'A new notice has been released, click to see now',
          value = url,
          inline = False
        )
        await self.use_channels['kms-update'].send(embed = embed)
      elif (choice == 1):
        kms.get_soups()
        url = kms.get_latest_update()
        embed = discord.Embed()
        embed.add_field(
          name = 'Some update for you',
          value = url,
          inline = False
        )
        await self.use_channels['kms-update'].send(embed = embed)
      elif (choice == 2):
        kms.get_soups()
        url = kms.get_latest_event()
        embed = discord.Embed()
        embed.add_field(
          name = 'Check out the event are ongoing',
          value = url,
          inline = False
        )
        await self.use_channels['kms-update'].send(embed = embed)
      loop1800 = random.choice(range(10, 16)) + 1
      await asyncio.sleep(1800 * loop1800)

  async def send_packs(self):
    await self.bot.wait_until_ready()
    while (True):
      image_url = nomi_water_pack.hasunoai.get_random()
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.use_channels['cosplay'].send(embed = embed)
      image_url = nomi_water_pack.hanime.get_random()
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.use_channels['qbu-nsfw'].send(embed = embed)
      await asyncio.sleep(30)

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_channels()
    loop = asyncio.get_event_loop()
    loop.create_task(self.daily_time_handle())
    #loop.create_task(self.kms_update())
    loop.create_task(self.send_packs())


def setup(bot):
  bot.add_cog(Umbra(bot))
