import os
import requests
import json
import pyaudio

def vvox_test(text):
    host = os.environ.get('VOICEVOX_ENGINE_HOST')
    port = int(os.environ.get('VOICEVOX_ENGINE_PORT'))
    
    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ('text', text),
        ('speaker', 3),
    )
    
    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    
    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers = {"Content-Type": "application/json"},
        params = params,
        data = json.dumps(query.json())
    )
    
    # 再生処理
    voice = synthesis.content
    pya = pyaudio.PyAudio()
    
    # サンプリングレートが24000以外だとずんだもんが高音になったり低音になったりする
    stream = pya.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=24000,
                      output=True)
    
    stream.write(voice)
    stream.stop_stream()
    stream.close()
    pya.terminate()