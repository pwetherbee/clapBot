import os
from pytube import YouTube

path = "tempAudioFiles/"
cmdFormat = "clapadd <url>* <start> <stop> <name>* --- *url and name are required, start and stop time are in seconds and are optional\nfor example:\nclapadd https://www.youtube.com/watch?v=POFHXEOdZXU 100 120 synthcrazy\nclapadd https://youtu.be/xIarrG9ZO4I salt"


def getCmdFormat():
    return cmdFormat


def convertAndDownloadURL(url, start, stop, fileName, folderPath=path):
    print(url)
    url = str(url)
    yt = YouTube(url)
    if (
        yt.length > 60 * 40
    ):  # if video is over 20 mins, dont allow any download whatsoever
        e = "Youtube clip is too long!"
        print(e)
        return e
    if not start:
        start = 0
    if not stop:
        stop = yt.length
    try:  # try to convert to numbers
        start = float(start)
        stop = float(stop)
    except ValueError:
        e = "Invalid start or stop values!"
        raise ValueError(e)
    if start >= stop:
        print(start, stop)
        raise ValueError("Start time is greater than end time!")
    diff = stop - start
    streams = yt.streams.filter(only_audio=True).first()
    dl = streams.download(
        output_path=folderPath, filename="temp.m4a", skip_existing=False
    )
    print("\n Path to downloaded audio file: \n", dl)
    ffmpegCommands = f'ffmpeg -ss {start} -i "{dl}" -t {diff} -c:a copy -acodec libmp3lame -ab 256k "{folderPath}{fileName}.mp3" -y'
    # if start and stop not specified, just download the entire clip

    os.system(ffmpegCommands)
    return


def parseYTDLRequestInput(args):
    url = start = stop = filename = None
    if len(args) < 2:  # invalid number of arguments
        raise ValueError("Too few parameters!")
    elif (
        len(args) == 2
    ):  # assume it is in the format *url *filename and the user wants to download the entire clip
        url = args[0]
        filename = args[1]
    elif len(args) == 3:  # assume it is in the format *url *start *filename *start
        url = args[0]
        start = args[1]
        filename = args[2]
    elif len(args) == 4:  # assume it is in the format *url *start *stop *filename
        url = args[0]
        start = args[1]
        stop = args[2]
        filename = args[3]
    else:
        raise ValueError("Too many parameters!")
    return [url, start, stop, filename]
