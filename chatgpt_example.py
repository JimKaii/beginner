from openai import OpenAI
client = OpenAI()

def chat_with_chatgpt(user_message, system_prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content":system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

if __name__ == '__main__':
    chat_with_chatgpt(
        user_message="我要珍珠奶茶微糖微冰",
        system_prompt="你好，你是一位飲料店的店員，有人向你點餐"

    )