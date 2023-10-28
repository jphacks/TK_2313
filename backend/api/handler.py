import os
import openai
from dotenv import load_dotenv
from services import whisper_call, ChatGPT_call, voicevox_call
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File

load_dotenv()
openai.organization = os.environ.get('OPENAI_ORG_KEY')
openai.api_key = os.environ.get('OPENAI_API_KEY')


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


# イベントによって呼び出される関数

# def handle_event_driven(event, context):
#     #TODO

def handle_voice_driven(voice_input: bytes):
    transcript = whisper_call.whisper_transcription(voice_input)
    replay = ChatGPT_call.GPT_call(transcript)
    audio_bytes = voicevox_call.vvox_test(replay)
    # return mp3 as bytes
    return audio_bytes, replay
