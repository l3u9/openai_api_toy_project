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
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


# OpenAI API Key
api_key = os.environ.get("OPENAI_API_KEY")
print(api_key)

# base_url = "https://s2yunseul.github.io/yunseul/%EC%8B%9D%EB%8B%B9/"

# html = ""
# css = ""

# js = ""

# html = requests.get(base_url+"index.html").text

# css = requests.get(base_url+"style.css").text

# js = requests.get(base_url+"script.js").text


# feature = "Please make this a site to recruit participants for the AI ​​competition."
# Path to your image
# image_paths = ["./images/site1.png", "./images/site2.png", "./images/site3.png"]
# image_paths = ["./images/sample.png"]
# image_paths = ["./images/ai1.png", "./images/ai2.png", "./images/ai3.png", "./images/ai4.png", "./images/ai5.png", "./images/ai6.png"]


# # Getting the base64 string
# base64_images = encode_image(image_paths)
# print(len(base64_images))

# payload = vision_payload(base64_images)


# # print("Payload: ", payload)

# output = execute_vision(payload)
# print("output:" , output)

# code = output.choices[0].message.content
# print("type: ", type(code))
# # print("payload: ", json.dumps(payload, indent=2))
# f = open("output.txt", "w")
# f.write(code)

code = ""

# 1. Create chat prompt template for 코드 수정
code_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 웹 개발자입니다. 참고 소스코드가 존재하면 클라이언트 요구사항에 맞게 소스코드를 수정하고, 필요시 추가 소스코드도 제공해주세요. 설명 없이 수정된 최종 소스코드만 출력해주세요."),
    # ("ai", "네, 주어진 소스코드를 분석하여 요구사항에 맞게 수정하고, 필요한 추가 코드도 제공하겠습니다."),
    # ("system", "참고 소스코드는 ```{code}``` 입니다. 이 소스코드를 바탕으로 클라이언트의 디자인 요구사항에 맞는 CSS 스타일을 Chakra UI와 Tailwind CSS를 사용하여 수정하고, 추가 스타일링이 필요한 경우 함께 적용해주세요."),
    # ("ai", "참고 소스코드를 확인했습니다. Chakra UI와 Tailwind CSS를 사용하여 디자인 요구사항에 맞는 스타일로 수정하겠습니다."),
    ("system", "전체 페이지는 원 페이지 랜딩 웹사이트 형식으로 구성해주시고, 필요한 모든 스타일링을 적용해주세요."),
    ("ai", "원 페이지 랜딩 페이지로 구성하겠습니다."),
    # ("system", "주제 타이틀과 맞게 Tailwind CSS와 Chakra UI를 사용하여 페이지 전체에 적절한 CSS 스타일을 적용해주세요. 최대한 클라이언트의 요구에 맞는 분위기를 반영해주세요. 설명 없이 최종 CSS 코드만 출력해주세요."),
    # ("ai", "요구사항에 맞게 Tailwind CSS와 Chakra UI를 사용하여 스타일을 수정하고 적용하겠습니다."),
    ("system", "Chakra UI와 Tailwind 외부 라이브러리를 사용하여 페이지를 꾸미고 반응형 디자인을 구현해주세요. Tailwind의 유틸리티 클래스와 Chakra UI 컴포넌트를 조합하여 고퀄리티로 페이지를 디자인해주세요."),
    ("ai", "Chakra UI와 Tailwind를 사용하여 스타일을 구현하겠습니다."),
    ("system", "화면이 심심하지 않게 빈공간이 없게 스타일링해주고 디자인 섹션을 조화롭게 구성해줘."),
    ("ai", "빈 공간을 최소화하고 디자인 섹션을 조화롭게 구성하겠습니다."),
    ("system", "클라이언트가 홍보용 이미지와 참고 사진을 추가할 수 있도록 해주세요"),
    ("ai", "홍보용 이미지와 참고 사진을 추가할 수 있도록 구현하겠습니다."),
    ("system", "React, Node.js 기반의 프로젝트로 구성해주세요. 각 파일을 명시적으로 출력하고, 프로젝트의 전체 구조를 보여주세요. 설명 없이 파일 이름과 내용을 출력해주세요."),
    ("ai", "Node.js와 React18, ES6 프로젝트에 맞는 컴포넌트와 서버 코드를 작성하겠습니다."),
    ("system", "최종적으로 웹 프로젝트를 구동하기 위한 모든 소스코드와 파일들을 출력해주세요. React18 기반의 프론트엔드 코드와 Node.js 기반의 백엔드 코드를 포함한 전체 프로젝트 소스코드를 파일 이름과 함께 출력해주고 프로젝트 환경 구성 과정도 단계별로 설명해주세요."),
    ("human", "제 요구사항은 ```{client}``` 입니다."),
    ("ai", "요구사항에 맞게 수정된 최종 프로젝트 소스코드는 다음과 같습니다."),
])


# backend_code = ChatPromptTemplate.from_messages([
#     ("system", "주어진 코드들과 클라이언트의 요구사항을 바탕으로 백엔드 코드를 작성해주세요."),
#     ("ai", "백엔드 코드를 요구사항에 맞게 작성하겠습니다."),
#     ("system", "참고할 코드는 ```{code}``` 및 ```{code2}```입니다. 이 코드들을 참고하여 클라이언트의 요구사항에 맞는 백엔드 코드를 완성해주세요."),
#     ("ai", "참고 코드를 확인하였으며, 클라이언트 요구사항을 반영한 백엔드 코드를 작성하겠습니다."),
#     ("system", "특히 클라이언트의 특정 요구사항 ```{client}```에 맞춰 백엔드 로직을 구현해주세요."),
#     ("human", "제 요구사항은 ```{client}``` 입니다."),
#     ("ai", "요구사항에 맞게 최종적으로 수정된 백엔드 코드는 다음과 같습니다."),
# ])

# # 2. Create chat prompt template for 프로젝트 실행 설명
# execution_prompt = ChatPromptTemplate.from_messages([
#     ("system", "front: ```{front}```, backend: ```{backend}``` 이 내용의 React 프로젝트를 로컬 환경에서 구동하는 방법에 대해 자세히 설명해주세요. 설치해야 할 패키지와 실행 명령어, 필요 조건들을 포함해주세요."),
#     ("ai", "React 프로젝트를 로컬 환경에서 실행하는 방법을 설명해드리겠습니다."),
#     ("system", "필요한 패키지 설치 명령어, 환경 설정 파일, 그리고 프로젝트를 시작하는 방법을 단계별로 설명해주세요."),
#     ("ai", "프로젝트를 실행하기 위한 필수 패키지, 환경 설정 파일, 그리고 구동 명령어를 포함한 단계별 실행 절차를 제공하겠습니다."),
# ])

# 3. Initialize model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
# model = ChatOpenAI(model="o1-mini", temperature=0.7)


# 4. Create parser
parser = StrOutputParser()

# 5. Create chains
code_chain = code_prompt | model | parser
# execution_chain = execution_prompt | model | parser
# backend_code_chain = backend_code | model | parser

# 6. Read client requirement from file
with open("client.txt", "r", encoding="utf-8") as f:
    client = f.read()

# Suppose 'output' contains the code you want to pass to 'code' field
# You should define or fetch 'output' before using it here

# 7. Run code_chain to get the modified code
modified_code_result = code_chain.invoke({
    # "code": code,
    "client": client
})

# backend_code_result = backend_code_chain.invoke({
#     "code": code,
#     "code2": modified_code_result,
#     "client": client
# })

# # 8. Run execution_chain to get the instructions for running the project
# execution_instructions_result = execution_chain.invoke({
#     "front": modified_code_result,
#     "backend": backend_code_result
# })

# 9. Write the results to separate files or print them
with open("modified_code.md", "w", encoding="utf-8") as f:
    f.write(modified_code_result)

# with open("backend_code.md", "w", encoding="utf-8") as f:
#     f.write(backend_code_result)

# with open("execution_instructions.md", "w", encoding="utf-8") as f:
#     f.write(execution_instructions_result)

