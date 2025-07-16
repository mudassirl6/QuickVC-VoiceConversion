from pydub import AudioSegment

# Load .m4a file
audio = AudioSegment.from_file("/home/user/Downloads/fine-lookinx27-pie-322685.mp3", format="mp3")

# Export as .wav
audio.export("./test_data/accent.wav", format="wav")
