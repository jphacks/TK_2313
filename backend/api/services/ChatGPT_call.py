import openai

def GPT_call(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": text},
        ],
    )
    response_message = response.choices[0]["message"]["content"].strip()
    return response_message