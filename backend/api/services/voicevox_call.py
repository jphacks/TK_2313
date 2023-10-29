import os
import requests
import json


def vvox_test(text):
    host = os.environ.get('VOICEVOX_ENGINE_HOST')
    port = int(os.environ.get('VOICEVOX_ENGINE_PORT'))

    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ('text', text),
        # ('speaker', 8),
        ('speaker', 43)
    )

    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )

    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers={"Content-Type": "application/json"},
        params=params,
        data=json.dumps(query.json())
    )

    return synthesis.content
