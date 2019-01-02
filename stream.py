import asyncio, discord, youtube_dl


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
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


async def info_from_url(url, loop = None):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
    if 'entries' in data:
        data = data['entries'][0]
    return data

async def source_from_url(url, *, loop = None, stream = False):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))
    if 'entries' in data:
        data = data['entries'][0]
    file_name = data['url'] if stream else ytdl.prepare_filename(data)
    data['audio_source'] = discord.FFmpegPCMAudio(file_name, options = '-vn')
    return data
