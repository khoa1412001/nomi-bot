from discord.ext import commands
import discord, asyncio
from modules import nomi_water_pack

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
      image_url = nomi_water_pack.o.get_random(['hasunoai'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['jap-cos'].send(embed = embed)

      image_url = nomi_water_pack.o.get_random(['hanime'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['hentai-pic'].send(embed = embed)

      image_url = nomi_water_pack.o.get_random(['ulzzang_face', 'ulzzang__girlz'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['korean'].send(embed = embed)

      image_url = nomi_water_pack.o.get_random(['favorite_asian_girls', 'instababes.asian', '69pretty.official'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['mixed'].send(embed = embed)

      image_url = nomi_water_pack.o.get_random(['vietnamesexybabe', 'vneseg', 'angels.in.vn', 'girl_xinh'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['vn'].send(embed = embed)
      
      image_url = nomi_water_pack.o.get_random('[hoingamgaitay]')
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
