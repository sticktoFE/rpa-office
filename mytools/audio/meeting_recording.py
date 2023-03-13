import pyaudio
import wave
from datetime import datetime
import pyaudio
import wave
import time


def recording(t):
    # 1、录音会议声音，按10分钟一次转成文字
    time.sleep(5)
    duration = 10
    # 初始化录音设备
    p = pyaudio.PyAudio()
    # 打开音频流
    # 设置参数
    CHUNK = 1024
    FORMAT = pyaudio.paInt24
    CHANNELS = 2
    RATE = 48000
    WAVE_OUTPUT_FILENAME = "output"
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("* recording")
    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * duration * 60)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    # 停止录音
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 将音频数据保存为WAV文件
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    wav_file_name = f"{WAVE_OUTPUT_FILENAME}_{t}.wav"
    wf = wave.open(wav_file_name, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


if __name__ == "__main__":
    i = 1
    while True:
        recording(i)
        i = i + 1
