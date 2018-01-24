from __future__ import unicode_literals
import youtube_dl
import os

videos = [
    # fred_astaire
    'https://www.youtube.com/watch?v=mxPgplMujzQ',
    'https://www.youtube.com/watch?v=CnrbdNjf-aw',
    'https://www.youtube.com/watch?v=yTH9VwACh7o',
    'https://www.youtube.com/watch?v=yuJxYmJlEHY',
    'https://www.youtube.com/watch?v=GKPMk5_gStk',
    # dancemovies
    'https://www.youtube.com/watch?v=j8XGmZ8HDIU',
    'https://www.youtube.com/watch?v=fy0rYUvn7To',
    'https://www.youtube.com/watch?v=pW1hazYKd5o',
    'https://www.youtube.com/watch?v=qdbrIrFxas0',
    'https://www.youtube.com/watch?v=BiAwpYIkRmU',
    # soul_train
    'https://www.youtube.com/watch?v=qXbP4JBf8To',
    'https://www.youtube.com/watch?v=qglBm-N-Lnw',
    'https://www.youtube.com/watch?v=lODBVM802H8',
    'https://www.youtube.com/watch?v=0g7KawdsVSQ',
    # air_guitar
    'https://www.youtube.com/watch?v=U_0HSjUpciQ',
    # choreographies
    'https://www.youtube.com/watch?v=X5qpDrmyO0E',
    'https://www.youtube.com/watch?v=Kl5B6MBAntI',
    'https://www.youtube.com/watch?v=7v5s0wDbEik',
    'https://www.youtube.com/watch?v=9TZYvud_ngY',
    'https://www.youtube.com/watch?v=2LwQXowfyVw',
    'https://www.youtube.com/watch?v=eFWieJL6Xys',
    'https://www.youtube.com/watch?v=QO2KwVh4yNk',
    'https://www.youtube.com/watch?v=qL7Y7Y_enAg',
    'https://www.youtube.com/watch?v=I7FgZcvx1XI',
    'https://www.youtube.com/watch?v=_cZSslxIrdc',
    'https://www.youtube.com/watch?v=iW2yUrXXRTI',
    'https://www.youtube.com/watch?v=sUKrTQRNZuw',
    'https://www.youtube.com/watch?v=cqdXgQ5bxxs',
    'https://www.youtube.com/watch?v=h-bsd6FSZDY',
    # music_videos
    'https://www.youtube.com/watch?v=Vnoz5uBEWOA',
    'https://www.youtube.com/watch?v=JqYhuwu614Y',
    'https://www.youtube.com/watch?v=wCDIYvFmgW8',
    'https://www.youtube.com/watch?v=9bZkp7q19f0',
    # internet_shit
    'https://www.youtube.com/watch?v=gtakKnP5GcM',
    'https://www.youtube.com/watch?v=ABz2m0olmPg',
    'https://www.youtube.com/watch?v=yMHygHL-obQ',
    'https://www.youtube.com/watch?v=otCpCn0l4Wo',
    'https://www.youtube.com/watch?v=VLW1ieY4Izw',
    'https://www.youtube.com/watch?v=y90yaLFoYoA',
    'https://www.youtube.com/watch?v=A1PAO3jgmXY',
    'https://www.youtube.com/watch?v=bPn6Dw4f26Q',
]

class ScraberLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def scraber_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def mkdir(path):
    sub_path = os.path.dirname(path)
    if not os.path.exists(path):
        os.mkdir(path)

path=os.path.dirname(os.path.abspath(__file__))
data_path="%s/data" % (path, )
mkdir(data_path)
video_path="%s/video/" % (data_path, )
mkdir(video_path)
audio_path="%s/audio/" % (data_path, )
mkdir(audio_path)

video_path_opts='{}%(title)s.%(ext)s'.format(video_path)

ydl_opts_video = {
    'f': 'bestvideo[height<=?1080]+bestaudio/best',
    'recode-video': 'mp4',
    'logger': ScraberLogger(),
    'progress_hooks': [scraber_hook],
    'outtmpl': video_path_opts
}

with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
    ydl.download(videos)

audio_path_opts='{}%(title)s.%(ext)s'.format(audio_path)
ydl_opts_audio = {
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
    'logger': ScraberLogger(),
    'progress_hooks': [scraber_hook],
    'outtmpl': audio_path_opts
}
with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
    ydl.download(videos)

