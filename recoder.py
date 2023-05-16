import cv2
import numpy as np
import pyaudio
import wave

# 屏幕分辨率
screen_size = (1920, 1080) # 假设屏幕分辨率为 1920x1080

# 录音设置
audio_format = pyaudio.paInt16
audio_channels = 2
audio_rate = 44100
audio_chunk_size = 1024
audio_seconds = 10

# 录制的视频文件名和音频文件名
video_filename = '~/output.avi'
audio_filename = '~/output.wav'

# 打开视频文件
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_filename, fourcc, 30.0, screen_size)

# 打开音频流
audio_stream = pyaudio.PyAudio().open(
    format=audio_format,
    channels=audio_channels,
    rate=audio_rate,
    input=True,
    frames_per_buffer=audio_chunk_size
)

# 开始录制
for i in range(int(audio_rate / audio_chunk_size * audio_seconds)):
    # 截取屏幕截图
    screen = np.array(ImageGrab.grab(bbox=(0, 0, *screen_size)))

    # 写入视频文件
    video_writer.write(screen)

    # 读取音频数据并写入音频文件
    audio_data = audio_stream.read(audio_chunk_size)
    with wave.open(audio_filename, 'ab') as audio_file:
        audio_file.writeframes(audio_data)

# 停止录制
video_writer.release()
audio_stream.stop_stream()
audio_stream.close()