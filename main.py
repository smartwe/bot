#!/bin/env python3
# Requires: youtube_dl module
# Requires: ffmpeg
# Usage:
#
# python youtube2mp3.py <URL>, ...
#
# Example:
#
# python3 youtube2mp3.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

import youtube_dl
import sys

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

if __name__ == "__main__":
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = sys.argv[1:]
        ydl.download(filenames)