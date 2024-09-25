from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="o1-preview",
    messages=[
        {
            "role": "user", 
            "content": "멋진 랜딩페이지 제작"
        }
    ]
)


f = open("landing_page.txt", "w")
f.write(response.choices[0].message.content)

print(response.choices[0].message.content)