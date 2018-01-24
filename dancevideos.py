import subprocess
from os import mkdir

fred_astaire = [
    'https://www.youtube.com/watch?v=mxPgplMujzQ',
    'https://www.youtube.com/watch?v=CnrbdNjf-aw',
    'https://www.youtube.com/watch?v=yTH9VwACh7o',
    'https://www.youtube.com/watch?v=yuJxYmJlEHY',
    'https://www.youtube.com/watch?v=GKPMk5_gStk',
]

dancemovies = [
    'https://www.youtube.com/watch?v=j8XGmZ8HDIU',
    'https://www.youtube.com/watch?v=fy0rYUvn7To',
    'https://www.youtube.com/watch?v=pW1hazYKd5o',
    'https://www.youtube.com/watch?v=qdbrIrFxas0',
    'https://www.youtube.com/watch?v=BiAwpYIkRmU',
]

soul_train = [
    'https://www.youtube.com/watch?v=qXbP4JBf8To',
    'https://www.youtube.com/watch?v=qglBm-N-Lnw',
    'https://www.youtube.com/watch?v=lODBVM802H8',
    'https://www.youtube.com/watch?v=0g7KawdsVSQ',
]

air_guitar = [

]

bollywood = [
    'https://www.youtube.com/watch?v=U_0HSjUpciQ',

]

choreographies = [
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
]

music_videos = [
    'https://www.youtube.com/watch?v=Vnoz5uBEWOA',
    'https://www.youtube.com/watch?v=JqYhuwu614Y',
    'https://www.youtube.com/watch?v=wCDIYvFmgW8',
    'https://www.youtube.com/watch?v=9bZkp7q19f0',
]

internet_shit = [
    'https://www.youtube.com/watch?v=gtakKnP5GcM',
    'https://www.youtube.com/watch?v=ABz2m0olmPg',
    'https://www.youtube.com/watch?v=yMHygHL-obQ',
    'https://www.youtube.com/watch?v=otCpCn0l4Wo',
    'https://www.youtube.com/watch?v=VLW1ieY4Izw',
    'https://www.youtube.com/watch?v=y90yaLFoYoA',
    'https://www.youtube.com/watch?v=A1PAO3jgmXY',
    'https://www.youtube.com/watch?v=bPn6Dw4f26Q',
]


def download_video(video_link, output_dir='data/videos/'):
    vlc_download_cmd = ('/Applications/VLC.app/Contents/MacOS/VLC -I rc '
                        '--play-and-exit -vvv "{link}" --sout="#transcode'
                        '{{vcodec=mp4v,acodec=mp4a,samplerate=44100}}'
                        ':std{{access=file,mux=mp4,dst={output_name}.m4v}}"')

    link = video_link
    output_name = output_dir + video_link.split('=')[-1]

    subprocess.check_output(
        vlc_download_cmd.format(
            link=link, output_name=output_name),
        shell=True,
        timeout=120
    )


all_vids = {'fred_astaire': fred_astaire,
            'dancemovies': dancemovies,
            'soul_train': soul_train,
            'bollywood': bollywood,
            'choreographies': choreographies,
            'music_videos': music_videos,
            'internet_shit': internet_shit}

for key in all_vids:
    mkdir('data/videos/%s' % key)

for name, videos in all_vids.items():
    for video in videos:
        print('Downloading %s' % video)
        download_video(video, 'data/videos/%s/' % name)
