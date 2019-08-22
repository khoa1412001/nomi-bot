from discord.ext import commands
import discord, asyncio, datetime, pytz
from modules import water_pack

class Umbra(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.my_guild = None
    self.my_channels = {}
    self.my_roles = {}
    self.last_online = {}

  def find_objects(self):
    guilds = self.bot.guilds
    for guild in guilds:
      if (guild.name == 'Umbra'):
        self.my_guild = guild
        channels = guild.channels
        for channel in channels:
          self.my_channels[channel.name] = channel
        roles = guild.roles
        for role in roles:
          self.my_roles[role.name] = role
        break
        
  async def print_last_online(self):
    await self.bot.wait_until_ready()
    while (True):
      now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
      if (now.hour in [0, 12] and now.minute in [0]):
        members = self.my_guild.members
        str = ''
        for member in members: 
          if member.bot:
            continue
          if (member.id not in self.last_online):
            self.last_online[member.id] = 'No information'
          str += f'{member.name}#{member.discriminator} ({member.display_name}) : {self.last_online[member.id]}\n'
        f = open('temp.txt', 'w')
        f.write(str)
        f.close()
        f = open('temp.txt', 'rb')
        file = discord.File(
          fp = f,
          filename = 'online-status.txt'
        )
        await self.my_channels['online-status'].send(file = file)
        f.close()
        os.remove('temp.txt')
        await asyncio.sleep(60)
      else:
        await asyncio.sleep(30)

  async def daily_time_handle(self):
    await self.bot.wait_until_ready()
    while (True):
      now = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
      if (now.hour in [17] and now.minute in [55]):
        str = f'{self.my_roles["Member"].mention}, Urus in next 5 minutes.'
        await self.my_channels['kms-daily'].send(str)
        await asyncio.sleep(60)
      elif (now.hour in [9, 16, 18] and now.minute in [55]):
        str = f'{self.my_roles["Member"].mention}, Flag Race in next 5 minutes.'
        await self.my_channels['kms-daily'].send(str)
        await asyncio.sleep(60)
      else:
        await asyncio.sleep(30)

  async def send_packs(self):
    await self.bot.wait_until_ready()
    while (True):
      image_url = water_pack.o.get_random(['hasunoai'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['cosplay'].send(embed = embed)

      image_url = water_pack.o.get_random(['hanime'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['qbu-nsfw'].send(embed = embed)

      image_url = water_pack.o.get_random(['ulzzang_face', 'ulzzang__girlz'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['ulzzang'].send(embed = embed)

      image_url = water_pack.o.get_random(['favorite_asian_girls', 'instababes.asian'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['asian'].send(embed = embed)

      image_url = water_pack.o.get_random(['vietnamesexybabe', 'vneseg', 'angels.in.vn', 'girl_xinh'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['cây-nhà-lá-vườn'].send(embed = embed)
      
      image_url = water_pack.o.get_random(['hoingamgaitay'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['not-for-qbu'].send(embed = embed)
      
      image_url = water_pack.o.get_random(['69pretty.official'])
      embed = discord.Embed()
      embed.set_image(url = image_url)
      await self.my_channels['mixed'].send(embed = embed)
      
      await asyncio.sleep(5400)

  @commands.Cog.listener()
  async def on_ready(self):
    self.find_objects()
    loop = asyncio.get_event_loop()
    loop.create_task(self.daily_time_handle())
    loop.create_task(self.send_packs())
    loop.create_task(self.print_last_online())
    
  @commands.Cog.listener()
  async def on_member_update(self, before, after):
    if (after.guild == self.my_guild):
      if (after.status != discord.Status.offline):
        self.last_online[after.id] = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%d")

def setup(bot):
  bot.add_cog(Umbra(bot))
