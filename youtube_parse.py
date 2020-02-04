# -*- coding: utf-8 -*-
''' 
Getting information about the file, downloading 
the audio and video file from the link.
Ffmpeg installation required. 
'brew install ffmpeg' or 'apt-get install ffmpeg'
or https://www.ffmpeg.org/download.html
'''

import youtube_dl

from get_proxies import get_proxy


def get_info(**kwarg):
    global count
    count += 1
    proxy = get_proxy()
    print(proxy, count)
    ydl_opts = {
    'ignoreerrors': True,
    'nocheckcertificate': True,
    'proxy': proxy,
    'socket_timeout': 30,
    }
    info = []
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(kwarg['url'], download=False)
            formats = meta.get('formats', [meta])
            title = meta.get('summaru', [meta])
    except:
        return False

    if kwarg['params'] == 'check_info':
        for f in formats[::-1]:
            if f['ext'] == 'mp4' and f['fps'] != None and \
                str(f['height']) + 'p' + str(f['fps']) not in info:
                info.append(str(f['height']) + 'p' + str(f['fps']))
        return info

    if kwarg['params'] == 'check_filesize':
        for f in formats[::-1]:
            if f['height'] == kwarg['height'] and \
            f['fps'] == kwarg['fps'] and f['filesize'] <= 524288000:
                return True


def get_audio(url):
    global count
    count += 1
    proxy = get_proxy()
    print(proxy, count)
    ydl_opts = {
    'nocheckcertificate': True,
    'outtmpl': 'data/%(title)s.%(ext)s',
    'noprogress': True,
    'format': '140',
    'proxy': proxy,
    'socket_timeout': 10,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        count = 0
    except:
        if count == 35:
            count = 0
            raise 
        get_audio(url)


def get_video(url, height, fps):
    global count
    count += 1
    proxy = get_proxy()
    print(proxy, count)
    ydl_opts = {
    'ignoreerrors': True,
    'nocheckcertificate': True,
    'noprogress': True,
    'outtmpl': 'data/%(title)s.%(ext)s',
    'max_filesize': 524288000,
    'socket_timeout': 10,
    'proxy': proxy,
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'}]
    }
    if fps == 60:
        ydl_opts['format'] = f'bestvideo[ext=mp4] \
        [height={height}][fps=60]+bestaudio'
        
    elif fps == 50:
        ydl_opts['format'] = f'bestvideo[ext=mp4] \
        [height={height}][fps=50]+bestaudio'
        
    else:
        ydl_opts['format'] = f'bestvideo[height={height}] \
        +bestaudio/bestvideo[ext=mp4]+bestaudio/best'
        
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        count = 0
    except:
        if count == 35:
            count = 0
            raise 
        get_video(url, height, fps)
    

count = 0


if __name__ == '__main__':
    pass