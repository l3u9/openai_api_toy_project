import base64
import os
import requests
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
def encode_image(image_paths):
    if len(image_paths) == 0:
        return []
    base64_images = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            base64_images.append(base64.b64encode(image_file.read()).decode('utf-8'))
    return base64_images
        #   "model": "gpt-4o-mini",

def vision_payload(base64_images):
    payload = {
        "model": "gpt-4o-mini",  # 가능한 모델로 설정
        "messages": [
            {
                "role": "system",
                "content": (
                    "당신은 웹 개발자입니다. 주어진 이미지를 바탕으로 원 페이지 "
                    "React 기반의 웹 프론트엔드 컴포넌트 소스코드를 작성하고, 사진과 똑같게 "
                    "CSS 코드를 자세하게 작성해주세요. 백엔드가 필요하다면 백엔드 코드를 "
                    "함께 작성해주세요."
                )
            },
            {
                "role": "user",
                "content": []  # 사용자 메시지를 담을 부분
            }
        ],
        "max_tokens": 16384
    }

    # base64 이미지를 처리하여 payload에 추가
    for base64_image in base64_images:
        # 확장자와 형식을 추론할 수 있도록 data URL의 포맷을 유연하게 설정
        image_format = "jpeg"  # 기본값
        if base64_image.startswith("/9j/"):  # JPEG의 특정 시그니처
            image_format = "jpeg"
        elif base64_image.startswith("iVBORw0KGgo"):  # PNG 시그니처
            image_format = "png"
        elif base64_image.startswith("R0lGOD"):  # GIF 시그니처
            image_format = "gif"

        payload["messages"][1]["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{image_format};base64,{base64_image}",
                "detail": "low"
            }

        })
    return payload

# def execute_vision(payload):
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     try:
#         response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#         response.raise_for_status()  # 응답 상태 코드 확인
#         return response  # 응답 데이터를 JSON 형식으로 반환
#     except requests.exceptions.HTTPError as err:
#         print(f"HTTP error occurred: {err}")
#         return f"HTTP error occurred: {err}"
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return f"An error occurred: {str(e)}"

def execute_vision(payload):
    try:
        response = client.chat.completions.create(
            model=payload["model"],
            messages=payload["messages"],
            max_tokens=payload["max_tokens"]
        )
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"