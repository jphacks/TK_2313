import os
from mychatgpt import Chat, Message, Role, Model, GPTFunction, GPTFunctionParam, GPTFunctionProperties
from dotenv import load_dotenv
import json
import time
import hashlib
import hmac
import base64
import requests

load_dotenv(verbose=True)

# OpenAIのAPIトークン
API_TOKEN = os.environ.get('OPENAI_API_KEY')
API_BASE_URL = "https://api.switch-bot.com"
ACCESS_TOKEN = os.environ.get('SWITCH_BOT_ACCESS_TOKEN')
SECRET = os.environ.get('SWITCH_BOT_SECRET')
DEVICE_ID = os.environ.get('SWITCH_BOT_DEVICE_ID')


def generate_sign(token: str, secret: str, nonce: str) -> tuple[str, str]:
    """SWITCH BOT APIの認証キーを生成する"""

    t = int(round(time.time() * 1000))
    string_to_sign = "{}{}{}".format(token, t, nonce)
    string_to_sign_b = bytes(string_to_sign, "utf-8")
    secret_b = bytes(secret, "utf-8")
    sign = base64.b64encode(
        hmac.new(secret_b, msg=string_to_sign_b,
                 digestmod=hashlib.sha256).digest()
    )

    return (str(t), str(sign, "utf-8"))


def get_device_list() -> str:
    """SWITCH BOTのデバイスリストを取得する"""

    nonce = "zzz"
    t, sign = generate_sign(ACCESS_TOKEN, SECRET, nonce)
    headers = {
        "Authorization": ACCESS_TOKEN,
        "t": t,
        "sign": sign,
        "nonce": nonce,
    }
    url = f"{API_BASE_URL}/v1.1/devices"
    r = requests.get(url, headers=headers)

    return json.dumps(r.json(), indent=2, ensure_ascii=False)


def post_command(
    device_id: str,
    command: str,
    parameter: str = "default",
    command_type: str = "command",
) -> requests.Response:
    """指定したデバイスにコマンドを送信する"""

    nonce = "zzz"
    t, sign = generate_sign(ACCESS_TOKEN, SECRET, nonce)
    headers = {
        "Content-Type": "application/json; charset: utf8",
        "Authorization": ACCESS_TOKEN,
        "t": t,
        "sign": sign,
        "nonce": nonce,
    }
    url = f"{API_BASE_URL}/v1.1/devices/{device_id}/commands"
    data = json.dumps(
        {"command": command, "parameter": parameter, "commandType": command_type}
    )
    try:
        print(f"Post command: {data}")
        r = requests.post(url, data=data, headers=headers)
        print(f"Responce: {r.text}")
    except requests.exceptions.RequestException as e:
        print(e)

    return r


def turn_on_light(
    device_id: str,
    color: tuple[int, int, int] = (0, 0, 0),
    brightness: int = 100,
):
    """指定したパラメーターでカラーライトをオンにする"""

    (r, g, b) = color

    post_command(device_id, "setBrightness", str(brightness))
    post_command(device_id, "setColor", f"{r}:{g}:{b}")
    post_command(device_id, "turnOn")


def set_color(color: tuple[int, int, int]):
    (r, g, b) = color
    post_command(DEVICE_ID, "setColor", f"{r}:{g}:{b}")
    return f"色を{r}:{g}:{b}に変更しました"


def set_brightness(brightness: int):
    post_command(DEVICE_ID, "setBrightness", str(brightness))
    return f"明るさを{brightness}に変更しました"


def turn_on():
    post_command(DEVICE_ID, "turnOn")
    return "ライトをオンにしました"


def turn_off():
    post_command(DEVICE_ID, "set_color", "0:0:0")
    return "ライトをオフにしました"


# ライトのプロパティの作成
light1_power = GPTFunctionProperties("light1_power", "bool", "ライトの電源が入っているか")
light1_red = GPTFunctionProperties("light1_red", "integer", "ライトの赤")
light1_green = GPTFunctionProperties("light1_green", "integer", "ライトの緑")
light1_blue = GPTFunctionProperties("light1_blue", "integer", "ライトの青")
light1_brightness = GPTFunctionProperties(
    "light1_brightness", "integer", "ライトの明るさ")

set_light1_color = GPTFunction("set_light1_color", "ライトの色を変更します", GPTFunctionParam([light1_red, light1_green, light1_blue], [
                               light1_red, light1_green, light1_blue]), lambda _red, _green, _blue: set_color((_red, _green, _blue)))
set_light1_brightness = GPTFunction("set_light1_brightness", "ライトの明るさを変更します", GPTFunctionParam(
    [light1_brightness], [light1_brightness]), lambda _brightness: set_brightness(_brightness))
turn_on_light1 = GPTFunction(
    "turn_on_light1", "ライトをオンにします", GPTFunctionParam([], []), lambda: turn_on())
turn_off_light1 = GPTFunction(
    "turn_off_light1", "ライトをオフにします", GPTFunctionParam([], []), lambda: turn_off())

# チャットログのインスタンスの作成
chat = Chat(API_TOKEN, model=Model.gpt4,
            functions=[set_light1_color, set_light1_brightness, turn_on_light1, turn_off_light1])

with open("./prompt/hard_takanawa.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

chat.add(prompt, role=Role.system, output=True)  # ログへ追加(返答を得ない)


#
# print("user : こんにちは！")
# reply: Message = chat.send("こんにちは!")  # Userとして送信し返答を得る
# print(reply)  # 返答の表示(Messageはprintできる)
#
# chat.send("よろしくお願いします！", output=True)  # output=Trueで質問と返答まで表示する
#
# chat.reset()  # チャットログのリセット
#
# # ロールについて(system(強い権限),user(ユーザー),assistant(AIアシスタント))
#
# chat.add("これからねこになりきって会話してください", role=Role.system, output=True)  # ログへ追加(返答を得ない)
# chat.add(Message(Role.assistant, "かしこまりましたにゃん！"),
#          output=True)  # Messageのインスタンスでもよい,AI側の返答を書いておくことも可能(返答の方向性を指定できる)
# chat.add("こんにちは！お元気ですか？", output=True)  # roleを指定しないとUserになる
# reply: Message = chat.completion(output=True)  # 追加したログに対して返信を求める
#
# # 表示方法2
# print(f"{reply.role.name}:{reply.content}({reply.token})")

def GPT_call(text):
    chat.add(text, output=True)
    reply: Message = chat.completion(output=True)
    return reply.content
