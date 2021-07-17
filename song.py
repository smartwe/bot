from pytube import YouTube
import os
import glob

#유튜브 전용 인스턴스 생성
url = "https://www.youtube.com/watch?v=9L_WDQuG9Ds"
yt = YouTube(url)
print(yt.title)


print(yt.streams.filter(only_audio=True, file_extension='mp4').all())

# 특정영상 다운로드
yt.streams.filter(only_audio=True, file_extension='mp4').first().download("song")

print('success')

files = glob.glob("*.mp4")
for x in files:
    if not os.path.isdir(x):
        filename = os.path.splitext(x)
        try:
            os.rename(x,filename[0] + '.mp3')
        except:
            pass