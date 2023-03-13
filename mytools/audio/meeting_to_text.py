from pydub import AudioSegment


def toMP3(file_name):
    # 将 WAV 文件转换为 MP3 文件
    sound = AudioSegment.from_wav(f"{file_name}.wav")
    mp3_file_name = f"{file_name}.mp3"
    sound.export(mp3_file_name, format="mp3")
    print(f"生成 MP3 文件 {mp3_file_name} 完成！")
    text = toText(mp3_file_name)
    out_docx(text, f"{file_name}.docx")


def toText(mp3_file_name):
    # 2、调用开发api转文字
    import openai

    # 设置 OpenAI API 密钥
    openai.api_key = "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"
    # 将 MP3 文件转换为文本
    print("开始将 mp3 文件转换为文本...")
    audio_file = open(mp3_file_name, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    transcription = transcript["text"]
    print(f"文本转换结果：{transcription}")
    return transcription


def toSimpe(transcription):
    import opencc

    # 创建 OpenCC 对象，使用 s2twp.json 配置文件将简体中文转换为台湾繁体中文
    # 繁体中文转换为大陆简体中文，可以使用 t2s.json 配置文件
    converter = opencc.OpenCC("t2s")
    # 将繁体中文字符串转换为简体中文字符串
    simplified_text = converter.convert(transcription)
    print(simplified_text)


def out_docx(simplified_text, outfile="output.docx"):
    # 导出为docx
    from docx import Document

    document = Document()
    document.add_paragraph(simplified_text)

    document.save(outfile)


if __name__ == "__main__":
    WAVE_OUTPUT_FILENAME = "output"
    i = 1
    while True:
        wav_file_name = f"{WAVE_OUTPUT_FILENAME}_{i}"
        toMP3(wav_file_name)
        i = i + 1
