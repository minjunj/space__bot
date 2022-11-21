import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#space_token = "eyJhbGciOiJSUzUxMiJ9.eyJzdWIiOiI0YnU1TmU0OHNFb2wiLCJhdWQiOiJjaXJjbGV0LXdlYi11aSIsIm9yZ0RvbWFpbiI6ImdzYWluZm90ZWFtIiwibmFtZSI6Im1pbmp1bl9KbyIsImlzcyI6Imh0dHBzOlwvXC9nc2FpbmZvdGVhbS5qZXRicmFpbnMuc3BhY2UiLCJwZXJtX3Rva2VuIjoidVZKVlUyRU0yZUsiLCJwcmluY2lwYWxfdHlwZSI6IlVTRVIiLCJpYXQiOjE2Njc5MDcxODR9.MPRqv5i8AyGkQvnAOt9S4sJcXWEeRafaH6HLE_O6qQXk8A3uCcuJF4Zy2wNbtHGJjYPYShaKSE1ZdpdZbz7uUqvvNx7-uBoy_DeJhZIbZQ-lchho0_TsiAPLcyzIblGtDbTUgPX36rJIXjaIXu8RINcbNErKqC4Tpijqiwd-ifs"
space_token = os.environ.get("SPACE_TOKEN")

url_full = "https://gsainfoteam.jetbrains.space/api/http/projects/id:3HmDlS2elYQJ/planning/issues?sorting=UPDATED&descending=false&$fields=data(title,description)"
url_To_slack = "https://hooks.slack.com/services/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" #웹훅 그 url로 가져오세요
def url_parser(url_full):#주소 박으면 분류해줌
    payload = {}
    #value = []
    url = url_full.split('?')#url 필요한 부분한 ?로 끊어서 가져오기
    #https://gsainfoteam.jetbrains.space/api/http/projects/id:3HmDlS2elYQJ/planning/issues
    main_url = url[0] #콜할 때 쓰는 http주소입니다.
    url_tail = url[1]
    #sorting=UPDATED&descending=false&$fields=data(title, description)
    url_tail_filter = url_tail.split('&') #&단위로 끊어서 배열만들기

    for i in url_tail_filter:#for문 돌려서 patload꼴에 받는 딕셔너리 제작
        key = i.split("=")
        #value.append(key[1])
        #print("a의 값 :" + str(a))
        payload[key[0]] = key[1]

    auth = {'Authorization': f'Bearer {space_token}'}
    source = requests.get(main_url,params=payload, headers=auth).json()
    src = source["data"]
    # print(src)
    return src

def print_issues(src):
    result = []  # 결과를 줄 리스트인데 안에 딕셔너리 있음
    dic = {}  # result에 들어갈 딕셔너리
    count = 1
    for i in src: #데이터 필터
        i_title = i['title']
        dic["title"] = str(count) + ". " + i_title
        try:
            i_des = i['description']
            dic["value"] = "-" + i_des + "    "
        except:
            i_des = "None"
            dic["value"] = "-" + i_des + "    "
        #dic["short"] = True 한행에 여러개 보여줄 때
        result.append(dic)
        dic = {}
        count += 1
    return result

result = print_issues(url_parser(url_full))

JSON = {
      "attachments": [
          {
              "fallback": "Get all issues",
              "color": "#2eb886",
              "fields": result,
              "ts": 123456789
          }
      ]
    }

def shot_message_slack(url_To_slack, result):
    source = requests.post(url_To_slack, json=JSON)



# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("!issues")
def message_hello(message, say):

    shot_message_slack(url_To_slack, result)


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()




