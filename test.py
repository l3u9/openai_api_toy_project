import requests

base_url = "https://s2yunseul.github.io/yunseul/%EA%B3%A4%ED%83%80%EB%B2%85%EC%8A%A4/"

html = requests.get(base_url+"index.html").text

css = requests.get(base_url+"style.css").text

js = requests.get(base_url+"script.js").text


f = open("html_code.txt", "w")
f.write(html)

f = open("css_code.txt", "w")
f.write(css)

f = open("js_code.txt", "w")
f.write(js)