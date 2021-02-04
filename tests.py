import json
import os
from pytube import YouTube

path = "tempAudioFiles/"

# create youtube object from url
# yt = YouTube("https://www.youtube.com/watch?v=seFHSuL0nsw")
# streams = yt.streams.filter(only_audio = True).first()
# dl = streams.download(output_path = path, filename='test.m4a')


# print(dl)
# download, cut and convert file to mp3 and place it in the correct folder
# os.system(f'ffmpeg -ss 10 -i "{dl}" -t 5 -c:a copy -acodec libmp3lame -ab 256k output.mp3')


cmdFormat = "clapadd <url*> <start> <stop> <name*> --- *required"


def convertAndDownloadURL(url, start, stop, fileName, folderPath=path):
    print(url)
    url = str(url)
    yt = YouTube(url)
    if (
        yt.length > 60 * 20
    ):  # if video is over 20 mins, dont allow any download whatsoever
        e = "Youtube clip is too long!"
        print(e)
        return e
    if not start:
        start = 0
    if not stop:
        stop = yt.length
    try:  # try to convert to numbers
        start = int(start)
        stop = int(stop)
    except ValueError:
        print("Invalid start or stop values!")
    if start >= stop:
        print(start, stop)
        e = "Start time is greater than end time!"
        print(e)
        return e
    diff = stop - start
    streams = yt.streams.filter(only_audio=True).first()
    dl = streams.download(
        output_path=folderPath, filename="temp.m4a", skip_existing=False
    )
    print("\n Path to downloaded audio file: \n", dl)
    ffmpegCommands = f'ffmpeg -ss {start} -i "{dl}" -t {diff} -c:a copy -acodec libmp3lame -ab 256k "{folderPath}{fileName}.mp3"'
    # if start and stop not specified, just download the entire clip

    os.system(ffmpegCommands)
    return


# convertAndDownloadURL("https://www.youtube.com/watch?v=seFHSuL0nsw", 10, 30, 'claps')

# cmd = input(
#    "Type out your requested mp3 in the format *url *start(optional) *stop(optional) *(the name you would like to use- NO spaces!)"
# )

# cmd = cmd.split()


def parseYTDLRequestInput(args):
    url = start = stop = filename = None
    if len(args) < 2:  # invalid number of arguments
        raise ValueError(
            "Too few parameters! Type out your requested mp3 in the format *url *start *stop *(the name you would like to use- NO spaces!)"
        )
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
        raise ValueError(
            "Too few parameters! Type out your requested mp3 in the format *url *start *stop *(the name you would like to use- NO spaces!)"
        )
    # return {"url": url, "start": start, "stop": stop, "filename": filename}
    return [url, start, stop, filename]


def checkUrl(url):
    return True
    # if url.startswith("https://www.youtube.com/watch?v=") or url.startswith(
    # "https://youtu.be/"
    # ):
    #    return True
    # return False


j = 0
while j < 10:
    j += 1
    try:
        cmd = input(
            "Type out your requested mp3 in the format *url *start(optional) *stop(optional) *(the name you would like to use- NO spaces!)"
        )
        cmd = cmd.split()
        outputs = parseYTDLRequestInput(cmd)
        print(outputs)
        break
    except ValueError as e:
        print(e)

# outputs[0] = "https://youtu.be/7ODcC5z6Ca0"

convertAndDownloadURL(*outputs)

print('this file should trigger github')