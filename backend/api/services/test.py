import os
import openai
from dotenv import load_dotenv
import whisper_call
import ChatGPT_call
import voicevox_call

def f():
    load_dotenv()
    openai.organization = os.environ.get('OPENAI_ORG_KEY')
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    fname = "output.m4a"
    audio_file = open(fname, "rb")
    transcript = whisper_call.whisper_transcription(audio_file)
    response_message = ChatGPT_call.GPT_call(transcript)
    print(response_message)
    voicevox_call.vvox_test(response_message)