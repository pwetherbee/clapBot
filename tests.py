import json
import os
from pytube import YouTube

path = 'tempAudioFiles/'

#create youtube object from url
#yt = YouTube("https://www.youtube.com/watch?v=seFHSuL0nsw")
#streams = yt.streams.filter(only_audio = True).first()
#dl = streams.download(output_path = path, filename='test.m4a')


#print(dl)
#download, cut and convert file to mp3 and place it in the correct folder
#os.system(f'ffmpeg -ss 10 -i "{dl}" -t 5 -c:a copy -acodec libmp3lame -ab 256k output.mp3')

def convertAndDownloadURL(url, start, stop, fileName, folderPath = path):
    yt = YouTube(url)
    if yt.length > 60*20: #if video is over 20 mins, dont allow any download whatsoever
        e='Youtube clip is too long!'
        print(e)
        return e 
    if not start: start = 0
    if not stop: stop = yt.length
    if start >= stop:
        e='Start time is greater than end time!'
        print(e)
        return e 
    diff = stop - start
    streams = yt.streams.filter(only_audio=True).first()
    dl = streams.download(output_path = folderPath, filename='temp.m4a', skip_existing=False)
    print('\n Path to downloaded audio file: \n', dl)
    ffmpegCommands = f'ffmpeg -ss {start} -i "{dl}" -t {diff} -c:a copy -acodec libmp3lame -ab 256k {folderPath}{fileName}.mp3'
    #if start and stop not specified, just download the entire clip
    
    os.system(ffmpegCommands)
    return 

#convertAndDownloadURL("https://www.youtube.com/watch?v=seFHSuL0nsw", 10, 30, 'claps')

cmd=input("Type out your requested mp3 in the format *url *start *stop *(the name you would like to use- NO spaces!)") 
    
print(cmd.split())

def parseYTDLRequestInput(args):
    parsed = args.split(' ')
    for arg in parsed:
        print(arg)

def checkUrl(url):
    if url.startswith("https://www.youtube.com/watch?v=") or url.startswith("https://youtu.be/"):
        return True
    return False

parseYTDLRequestInput(cmd)