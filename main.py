import datetime,random,asyncio
import discord,utils,logic,stream
import konachan,yandere,hentaigasm,watch8x,youtube
from discord.ext import commands as cmds

token=utils.variables['token']
prefix_char=utils.variables['prefix_char']
bot=cmds.Bot(command_prefix = prefix_char)
bot.remove_command('help')

async def log(content,use_time=True):
    channel=utils.config['log_channel']
    if channel==None:
        print('Error: Not found log channel.')
        return
    if use_time:
        await channel.send(f'[{str(datetime.datetime.now())}]\n{message}')
    else:
        await channel.send(content)
    print(content)
        
def init_variables():
    utils.variables['log_channel']=bot.get_channel(utils.variables['log_channel_id'])
    
async def init_activity():
    activity=discord.Activity(name='NTR hentai.',type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    init_variables()
    await init_activity()
    msg=(
        '```'
        f'version: {str(datetime.datetime.now())}\n'
        f'discord.py: {discord.__version__}\n'
        '```'
        )
    await log(msg,use_time=False)
    
@bot.event
async def on_message(message):
    guild, channel, sender, msg = message.guild, message.channel, message.author, message. content
    if sender.id!=bot.user.id:
        if len(message.mentions)==1 and bot.user.mentioned_in(message):
            async with channel.typing():
                delay_time=int(random.choice(range(40, 100))) / 100.0
                rely=utils.to_emoji(logic.req_to_res(msg))
                await asyncio.sleep(delay_time)
                await channel.send(f'{sender.mention} {rely}')
        if channel.id!=utils.config['log_channel_id']:
            await log(f'[{guild.name}][{channel.name}]{sender.name}\n{msg}')
    if msg.startswith(prefix_char):
        await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    embed=discord.Embed(
        description=logic.command_response('ping'), 
        color=utils.random_bright_color()
    )
    await ctx.send(embed=embed)
 
@bot.command()
async def clear(ctx,amount=100):
    guild=ctx.guild
    channel=ctx.channel
    sender=ctx.author
    if ctx.me.permissions_in(channel).manage_messages:
        if sender.permissions_in(channel).manage_messages:
            await channel.purge(limit = amount)
            embed = discord.Embed(
                description = logic.command_response('clear'), 
                color = helper.random_bright_color()
            )
            await ctx.send(embed = embed)
        else:
            await ctx.send(sender.mention + ' Sorry, you don\'t have permission to manage messages.')
    else:
        await ctx.send(sender.mention + ' Sorry, I don\'t have permission to manage messages.')
        
        
@bot.command()
async def knc(ctx):
    channel = ctx.channel
    sender = ctx.author
    if channel.is_nsfw():
        image_urls = konachan.explicit(1)
        for image_url in image_urls:
            embed = discord.Embed(
                title = 'Click to get source. (konachan)',
                description = logic.command_response('knc'),
                color = helper.random_bright_color(),
                url = image_url
            )  
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)
    else:
        image_urls = konachan.safe(1)
        for image_url in image_urls:
            embed = discord.Embed(
                title = 'Click to get source. (konachan)',
                description = logic.command_response('knc'),
                color = helper.random_bright_color(),
                url = image_url
            )  
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)
 

@bot.command()
async def ydr(ctx):
    channel = ctx.channel
    sender = ctx.author
    if channel.is_nsfw():
        image_urls = yandere.explicit(1)
        for image_url in image_urls:
            embed = discord.Embed(
                title = 'Click to get source. (yandere)',
                description = logic.command_response('ydr'),
                color = helper.random_bright_color(),
                url = image_url
            )
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)
    else:
        image_urls = yandere.safe(1)
        for image_url in image_urls:
            embed = discord.Embed(
                title = 'Click to get source. (yandere)',
                description = logic.command_response('ydr'),
                color = helper.random_bright_color(),
                url = image_url
            )
            embed.set_image(url = image_url)
            await ctx.send(embed = embed)

            
@bot.command()
async def anwp(ctx):
    packs = nomi_water_pack.asia_pack(1)
    for pack in packs:
        embed = discord.Embed(
            title = 'Click to get source. (Asian Nomi Water Pack)',
            description = logic.command_response('anwp'),
            color = helper.random_bright_color(),
            url = pack
        )
        embed.set_image(url = pack)
        await ctx.send(embed = embed)
                

@bot.command()
async def unwp(ctx):
    packs = nomi_water_pack.us_uk_pack(1)
    for pack in packs:
        embed = discord.Embed(
             title = 'Click to get source. (US-UK Nomi Water Pack)',
             description = logic.command_response('unwp'),
             color = helper.random_bright_color(),
             url = pack
        )
        embed.set_image(url = pack)
        await ctx.send(embed = embed)     
        
        
@bot.command()
async def htgasm(ctx):
    channel = ctx.channel
    sender = ctx.author
    if channel.is_nsfw():
        h = hentaigasm.hentai()
        name = h['name']
        stream_url = h['stream_url']
        image_url = h['image_url']
        embed = discord.Embed(
            title = name,
            description = logic.command_response('htgasm'),
            color = helper.random_bright_color(),
            url = stream_url
        )
        embed.set_image(url = image_url)
        await ctx.send(embed = embed)
    else:
        await ctx.send(sender.mention + ' Sorry, this is not nsfw channel.')
            

@bot.command()
async def wtch8x(ctx):
    channel = ctx.channel
    sender = ctx.author
    if channel.is_nsfw():
        j = watch8x.jav()
        code = j['code']
        stream_url = j['stream_url']
        image_url = j['image_url']
        embed = discord.Embed(
            title = code,
            description = logic.command_response('wtch8x'),
            color = helper.random_bright_color(),
            url = stream_url
        )
        embed.set_image(url = image_url)
        await ctx.send(embed = embed)
    else:
        await ctx.send(sender.mention + ' Sorry, this is not nsfw channel.')
                  
            
@bot.command()
async def join(ctx, *, voice_channel: discord.VoiceChannel):
    voice_client = ctx.voice_client
    sender = ctx.author
    if voice_client == None:
        await voice_channel.connect()
        embed = discord.Embed(
            description = logic.command_response('join'),
            color = helper.random_bright_color()
        )
        await ctx.send(embed = embed)
    else:
        flag = True
        if ctx.me.voice:
            if ctx.me.voice.channel == voice_channel:
                flag = False
                await ctx.send(sender.mention + ' Sorry, I\'m already in there.')
        if flag:
            await voice_client.move_to(voice_channel)
            embed = discord.Embed(
                description = logic.command_response('join'),
                color = helper.random_bright_color()
            )
            await ctx.send(embed = embed)

                
@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    channel = ctx.channel
    sender = ctx.author
    if sender.permissions_in(channel).administrator:
        if voice_client == None:
            await ctx.send(sender.mention + ' Sorry, there is no voice channel in using.')
        else:
            await voice_client.disconnect()
            embed = discord.Embed(
                description = logic.command_response('leave'),
                color = helper.random_bright_color()
            )
            await ctx.send(embed = embed)
    else:
        await ctx.send(sender.mention + ' Sorry, you aren\'t administrator.')

        
@bot.command()
async def play(ctx, *, url):
    voice_client = ctx.voice_client
    channel = ctx.channel
    sender = ctx.author
    flag = True
    if voice_client == None:
        if sender.voice:
            voice_client = await sender.voice.channel.connect()
        else:
            flag = False
            await ctx.send(sender.mention + ' Sorry, you need to connect to a voice channel.')
    else:
        if voice_client.is_playing(): 
            if sender.permissions_in(channel).administrator:
                voice_client.stop()
            else:
                flag = False
                await ctx.send(sender.mention + ' Sorry, you aren\'t administrator to stop current music. So just wait until it finishes.')
        if sender.voice and ctx.me.voice:
            if not sender.voice.channel == ctx.me.voice.channel:
                flag = False
                await ctx.send(sender.mention + ' Sorry, you are not even in the same voice channel as mine.')
    if flag:
        stream_url = url
        if url in ['1','2','3','4','5']:
            if len(utils.config['youtube_results']) > 0:
                stream_url = utils.config['youtube_results'][int(url) - 1]
                utils.config['youtube_results'] = []
        data = await stream.source_from_url(stream_url, loop = bot.loop)
        source = data['audio_source']
        voice_client.play(source)
        utils.config['last_play_url'] = stream_url
        embed = discord.Embed(
            title = 'Click to go to source player.',
            description = logic.command_response('play').format(data['title']),
            color = helper.random_bright_color(),
            url = stream_url
        )
        embed.set_image(url = data['thumbnail'])
        await ctx.send(embed = embed)

        
@bot.command()
async def replay(ctx):
    voice_client = ctx.voice_client
    channel = ctx.channel
    sender = ctx.author
    flag = True
    if voice_client == None:
        if sender.voice:
            voice_client = await sender.voice.channel.connect()
        else:
            flag = False
            await ctx.send(sender.mention + ' Sorry, you need to connect to a voice channel.')
    else:
        if voice_client.is_playing(): 
            if sender.permissions_in(channel).administrator:
                voice_client.stop()
            else:
                flag = False
                await ctx.send(sender.mention + ' Sorry, you aren\'t administrator to stop current music. So just wait until it finishes.')
        if sender.voice and ctx.me.voice:
            if not sender.voice.channel == ctx.me.voice.channel:
                flag = False
                await ctx.send(sender.mention + ' Sorry, you are not even in the same voice channel as mine.')
    if flag:
        if 'last_play_url' in utils.config:
            url = utils.config['last_play_url']
            data = await stream.source_from_url(url, loop = bot.loop)
            source = data['audio_source']
            voice_client.play(source)
            embed = discord.Embed(
                title = 'Click to go to source player.',
                description = logic.command_response('replay').format(data['title']),
                color = helper.random_bright_color(),
                url = url
            )
            embed.set_image(url = data['thumbnail'])
            await ctx.send(embed = embed)    
        else:
            await ctx.send(sender.mention + ' Sorry, there is nothing to replay.')
        
        
@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    channel = ctx.channel
    sender = ctx.author
    if sender.permissions_in(channel).administrator:
        if voice_client == None:
            await ctx.send(sender.mention + ' Well, I\'m not in any voice channel.')
        else:
            if voice_client.is_playing() or voice_client.is_paused():
                voice_client.stop()
                embed = discord.Embed(
                    description = logic.command_response('stop'),
                    color = helper.random_bright_color()
                )
                await ctx.send(embed = embed)
            else:
                await ctx.send(sender.mention + ' Sorry, I\'m not playing anything.')
    else:
        await ctx.send(sender.mention + ' Sorry, you aren\'t administrator to stop current music. So just wait until it finishes.')
  

@bot.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    channel = ctx.channel
    sender = ctx.author
    if sender.permissions_in(channel).administrator:
        if voice_client == None:
            await ctx.send(sender.mention + ' Sorry, I\'m not even in any voice channel.')
        else:
            if voice_client.is_paused():
                await ctx.send(sender.mention + ' Sorry, the music is already paused.')
            else:
                voice_client.pause()
                embed = discord.Embed(
                    description = logic.command_response('pause'),
                    color = helper.random_bright_color()
                )
                await ctx.send(embed = embed)
    else:
        await ctx.send(sender.mention + ' Sorry, you aren\'t administrator to pause current music.')
  

@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    channel = ctx.channel
    sender = ctx.author
    if sender.permissions_in(channel).administrator:
        if voice_client == None:
            await ctx.send(sender.mention + ' Sorry, I\'m not even in any voice channel.')
        else:
            if voice_client.is_paused():
                voice_client.resume()
                embed = discord.Embed(
                    description = logic.command_response('resume'),
                    color = helper.random_bright_color()
                )
                await ctx.send(embed = embed)
            else:
                await ctx.send(sender.mention + ' Sorry, the music is not paused.')
    else:
        await ctx.send(sender.mention + ' Sorry, you aren\'t administrator to resume current music, even pause it.')
  

@bot.command()
async def ytsearch(ctx, *word):
    query = '%20'.join(word)
    utils.config['youtube_results'] = youtube.search(query)
    embed = discord.Embed(
        description = 'Type "{}play <number>" to play audio.\n{}'.format(prefix_char, logic.command_response('ytsearch')),
        color = helper.random_bright_color()
    )
    for count in range(1,6):
        url = utils.config['youtube_results'][count - 1]
        data = await stream.info_from_url(url, loop = bot.loop)
        embed.add_field(
            name = 'Number {}'.format(count), 
            value = '[{}] {}'.format(helper.to_time_format(data['duration']), data['title']), 
            inline = False
        )
    await ctx.send(embed = embed)
    
    
@bot.command()
async def help(ctx): 
    invite_url = utils.config['invite_url']
    embed = discord.Embed(
        title = 'Help for noob',
        color = helper.random_bright_color()
    )  
    value = (
        '```'
        'You can use this link below to add me to your servers:\n\n'
        '{}\n\n'
        'Just copy it, lazy man.\n\n'
        'Only works if you are administrator of server or at least you have permission to manage server.'
        '```'
        ).format(invite_url)
    embed.add_field(
        name = 'Invitation', 
        value = value, 
        inline = False
    )
    value = (
        '```'
         'The main prefix character to start a command is "{}".\n'
         'Well, somehow you typed "{}help", I think you knew.\n\n'
         'Type "{}commands" to see all offical commands.\n'
         'Don\'t ask me about the unofficial.'
         '```'
        ).replace('{}', prefix_char)
    embed.add_field(
        name = 'Commands', 
        value = value, 
        inline = False
    )
    value = (
        '```'
        'Type a message with mention only me, I will automatic response to you.\n\n'
        'You can mention me everywhere in your message, but please don\'t mention me more than one time, just one.\n\n'
        'If anyone else is mentioned too, I won\'t response.\n\n'
        'Well, I\'m not an AI and sometimes I\'m not enough smart to rely to you.\n'
        'So don\'t talk to me too much.\n\n'
        'If you want to have direct messages with me and no one can read our conversation, well, I don\'t like private conversations, so, nerver.'
        '```'
        )
    embed.add_field(
        name = 'Chatting', 
        value = value, 
        inline = False
    )
    await ctx.send(embed = embed)
    
    
@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title = 'All commands for noob',
        color = helper.random_bright_color()
    )
    value = (
        '```'
        '{}help: show help message.\n'
        '{}commands: show this message, of course...\n'
        '{}ping: say "Pong!". (maybe)\n'
        '{}clear [number]: clear number-1 messages.'
        '```'
        ).replace('{}', prefix_char)
    embed.add_field(
        name = 'Misc (text channels)', 
        value = value, 
        inline = False
    )
    value = (
        '```'
        '{}knc: 1 image from konachan.\n'
        '{}ydr: 1 image from yandere.\n'
        '{}anwp: 1 image from asian nomi water pack.\n'
        '{}unwp: 1 image from us-uk nomi water pack.'
        '```'
    ).replace('{}', prefix_char)
    embed.add_field(
        name = 'Picture (text channels)', 
        value = value, 
        inline = False
    )
    value = (
        '```'
        '{}knc: 1 image from konachan.\n'
        '{}ydr: 1 image from yandere.\n'
        '{}htgasm: 1 hentai from hentaigasm.\n'
        '{}wtch8x: 1 jav from watch8x.'
        '```'
        ).replace('{}', prefix_char)
    embed.add_field(
        name = 'Nsfw (nsfw text channels)',
        value = value, 
        inline = False
    )
    value = (
        '```'
        '{}join <name>: join voice channel having name.\n'
        '{}leave: leave voice channel.\n'
        '{}play <url>: play audio from url.\n'
        '{}replay: play again the last audio.\n'
        '{}stop: stop current sound.\n'
        '{}pause: pause current sound.\n'
        '{}resume: resume current sound.\n'
        '{}ytsearch: search audios on Youtube and play them.'
        '```'
        ).replace('{}', prefix_char)
    embed.add_field(
        name = 'Music (voice channels)', 
        value = value, 
        inline = False
    )
    embed.set_footer(text = '[] is optional, <> is non-optional')
    await ctx.send(embed = embed)


bot.run(token)
