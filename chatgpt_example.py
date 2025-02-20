from openai import OpenAI
client = OpenAI()

def chat_with_gpt(user_message, system_prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return completion.choices[0].message.content

if __name__ == '__main__':
    chat_with_gpt(
        user_message="我要珍珠奶茶微糖微冰",
        system_prompt="你好，你是一位飲料店的店員，有人向你點餐"

    )