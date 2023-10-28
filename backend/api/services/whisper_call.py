import openai

def whisper_transcription(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']