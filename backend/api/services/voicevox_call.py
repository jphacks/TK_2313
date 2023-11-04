import os
import requests
import json
from typing import List
from dotenv import load_dotenv

load_dotenv(".env.default")

HOST = os.environ.get('VOICEVOX_ENGINE_HOST')
PORT = int(os.environ.get('VOICEVOX_ENGINE_PORT'))



class Character:
    def __init__(self,name:str,uuid:str,styles:dict[str,int]):
        self.name:str = name
        self.uuid:str = uuid
        self.styles:dict[str,int] = styles

    def get_params(self,text:str,style_id:str):
        return {
            'text': text,
            'style': style_id
        }

    def get_query(self,text:str,style_id:str):
        return requests.post(
            f'http://{HOST}:{PORT}/characters',
            headers={"Content-Type": "application/json"},
            data=json.dumps(self.get_params(text,style_id))
        )
        
    def make_voice(self,text:str,style:str|int):
        if type(style) == str:
            style = self.get_style_id(style)
        query = self.get_query(text,style)
        synthesis = requests.post(
            f'http://{HOST}:{PORT}/synthesis',
            headers={"Content-Type": "application/json"},
            data=json.dumps(query.json())
        )
        return synthesis.content


    def get_styles_name(self):
        return list(self.styles.keys())
    
    def get_style_id(self,style_name:str):
        if style_name not in self.styles:
            raise Exception(f'{style_name} is not in {self.name}')
        return self.styles[style_name]

    def __str__(self) -> str:
        return f'{self.name}:{" ".join(self.styles.keys())}'
    
def make_speaker_list():
    with open('api/services/speakers.json','r') as f:
        speaker_list = json.load(f)
    for speaker in speaker_list:
        speaker['uuid'] = speaker['speaker_uuid']
        speaker['style'] = dict()
        for style in speaker['styles']:
            speaker['style'][style['name']] = style['id']
        #print(speaker["styles"])
        
    return {speaker['name']:Character(speaker['name'],speaker['uuid'],speaker['style']) for speaker in speaker_list}
    
speakers=make_speaker_list()




def vvox_test(text):
    speaker=speakers['櫻歌ミコ']
    return speaker.make_voice(text,'ノーマル')


if __name__ == "__main__":
    for s in speakers:
        print(s)   
    vvox_test('こんにちは')