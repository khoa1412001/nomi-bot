from discord.ext import commands
from modules import nomi_water_pack
import discord, asyncio, random

class Asteria(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.my_guild = None
    self.my_channels = {}

  def find_objects(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'Asteria'):
        self.my_guild = guild
        channels = guild.channels
        for channel in channels:
          self.my_channels[channel.name] = channel
        break

  async def send_packs(self):
    await self.bot.wait_until_ready()
    while (True):
      image_url = nomi_water_pack.get_random('hasunoai')
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['jap-cos'].send(embed = embed)

      image_url = nomi_water_pack.get_random('hanime')
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['hentai-pic'].send(embed = embed)

      image_urls = [nomi_water_pack.get_random('ulzzang_face'), nomi_water_pack.get_random('ulzzang__girlz')]
      image_url = random.choice(image_urls)
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['korean'].send(embed = embed)

      image_urls = [nomi_water_pack.get_random('favorite_asian_girls'), nomi_water_pack.get_random('instababes.asian'), nomi_water_pack.get_random('69pretty.official')]
      image_url = random.choice(image_urls)
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['mixed'].send(embed = embed)

      image_urls = [nomi_water_pack.get_random('vietnamesexybabe'), nomi_water_pack.get_random('vneseg'), nomi_water_pack.get_random('angels.in.vn'), nomi_water_pack.get_random('girl_xinh')]
      image_url = random.choice(image_urls)
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['vn'].send(embed = embed)
      
      image_url = nomi_water_pack.get_random('hoingamgaitay')
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['western'].send(embed = embed)
      
      await asyncio.sleep(1800)

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_objects()
    loop = asyncio.get_event_loop()
    loop.create_task(self.send_packs())

def setup(bot):
  bot.add_cog(Asteria(bot))
