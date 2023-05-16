import wave
import threading
from os import remove, mkdir, listdir
from os.path import exists, splitext, basename, join
from datetime import datetime
from time import sleep
from shutil import rmtree
import pyaudio
from PIL import ImageGrab
from numpy import array
import cv2
from moviepy.editor import *

CHUNK_sIZE = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16
RATE = 48000
allowRecording = True


def record_audio():
    p = pyaudio.PyAudio()
    # event.wait()
    sleep(3)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=0,  # 立体混音，具体选哪个根据需要选择
                    frames_per_buffer=CHUNK_sIZE)
    wf = wave.open(audio_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    while allowRecording:
        # 从录音设备读取数据，直接写入wav文件
        data = stream.read(CHUNK_sIZE)
        wf.writeframes(data)
    wf.close()
    stream.stop_stream()
    stream.close()
    p.terminate()


def record_screen():
    # 录制屏幕
    im = ImageGrab.grab()
    video = cv2.VideoWriter(screen_video_filename,
                            cv2.VideoWriter_fourcc(*'XVID'),
                            25, im.size)  # 帧速和视频宽度、高度
    while allowRecording:
        im = ImageGrab.grab()
        im = cv2.cvtColor(array(im), cv2.COLOR_RGB2BGR)
        video.write(im)
    video.release()


now = str(datetime.now())[:19].replace(':', '_')
audio_filename = "%s.mp3" % now
webcam_video_filename = "t%s.avi" % now
screen_video_filename = "tt%s.avi" % now
video_filename = "%s.avi" % now

# 创建两个线程，分别录音和录屏
t1 = threading.Thread(target=record_audio)
t2 = threading.Thread(target=record_screen)

event = threading.Event()
event.clear()
for t in (t1, t2):
    t.start()
# 等待摄像头准保好，提示用户三秒钟以后开始录制
# event.wait()
print('3秒后开始录制，按q键结束录制')
while True:
    if input() == 'q':
        break
allowRecording = False
for i in (t1, t2):
    t.join()

# 把录制的视频和音频合成视频文件
audio = AudioFileClip(audio_filename)
video1 = VideoFileClip(screen_video_filename)
ratio1 = audio.duration / video1.duration
video1 = (video1.fl_time(lambda t: t / ratio1, apply_to=['video']) \
          .set_end(audio.duration))

video = CompositeVideoClip([video1]).set_audio(audio)
video.write_videofile(video_filename, codec='libx264', fps=25)

remove(audio_filename)
remove(screen_video_filename)