import base64
import os
import requests

API_KEY = os.environ.get("OPENAI_API_KEY")

def encode_image(image_paths):
    if len(image_paths) == 0:
        return []
    base64_images = []
    for image_path in image_paths:
        with open(image_path, "rb") as image_file:
            base64_images.append(base64.b64encode(image_file.read()).decode('utf-8'))
    return base64_images
  

def vision_payload(base64_images, html_code, css_code, js_code, feature):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"```html {html_code}``` \n```css {css_code}``` \n```js {js_code}```\nPlease refer to the style of this html, css, js webpage source code and change the structure and overall style. If there is an input photo, please write a responsive website code that is compatible with both mobile and web with the same structure as the photo, and without it. And please create it by reflecting the request: {feature}."
                    }
                ]
            },
            {
                "role": "user",
                "content": []  # 사용자 메시지로서 content를 빈 배열로 초기화
            }
        ],
        "max_tokens": 16384
    }

    # base64 이미지를 처리하여 payload에 추가
    if len(base64_images) == 0:
        return payload
    else:
        for base64_image in base64_images:
            payload["messages"][1]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "low"
                }
            })

    return payload

def execute_vision(payload):
    global API_KEY
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response