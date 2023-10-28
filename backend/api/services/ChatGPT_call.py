import os
from mychatgpt import Chat, Message, Role,Model
from dotenv import load_dotenv

load_dotenv(".env")

# OpenAIのAPIトークン
API_TOKEN = os.environ.get('OPENAI_API_KEY')

# チャットログのインスタンスの作成
chat = Chat(API_TOKEN, model=Model.gpt35)


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
    chat.add("これからねこになりきって会話してください", role=Role.system, output=True)  # ログへ追加(返答を得ない)
    chat.add(Message(Role.assistant, "かしこまりましたにゃん！"), output=True)
    chat.add(text, output=True)
    reply: Message = chat.completion(output=True)
    return reply.content
