from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from langchain_core.output_parsers import StrOutputParser
import requests
import os
from utils import *
import json

# OpenAI API Key
api_key = os.environ.get("OPENAI_API_KEY")


base_url = "https://s2yunseul.github.io/yunseul/%EC%8B%9D%EB%8B%B9/"

html = requests.get(base_url+"index.html").text

css = requests.get(base_url+"style.css").text

js = requests.get(base_url+"script.js").text

feature = "Please make this a site to recruit participants for the AI ​​competition."
# Path to your image
# image_paths = ["./images/site1.png", "./images/site2.png", "./images/site3.png"]
# image_paths = ["./images/sample.png"]
image_paths = []

# Getting the base64 string
base64_images = encode_image(image_paths)
print(len(base64_images))

payload = vision_payload(base64_images, html, css, js, feature)


# print("Payload: ", payload)

output = execute_vision(payload)
# print("payload: ", json.dumps(payload, indent=2))
f = open("output.txt", "w")
f.write(output.text)





# # 1. Create prompt template
# system_template = "Translate the following into {language}:"
# prompt_template = ChatPromptTemplate.from_messages([
#     ('system', system_template),
#     ('user', '{text}')
# ])

# # 2. Create model
# model = ChatOpenAI(model="gpt-4o-mini")

# # 3. Create parser
# parser = StrOutputParser()

# # 4. Create chain
# chain = LLMChain(
#     llm=model,
#     prompt=prompt_template,
#     output_parser=parser
#     )

# output = chain.run(language="French", text="Hello, how are you?")  # Translate the following into French: Hello, how are you?
# print(output)