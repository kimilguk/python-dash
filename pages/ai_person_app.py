#-*- coding:utf-8 -*-
import dash # 멀티 파일로 실행 할 때 위 아래 줄 주석 해제
dash.register_page(
    __name__,
    title='사람속성 검출 AI를 사용한 웹 앱',
    path='/ai_person_app',
    description='사람속성 검출 AI를 사용한 웹 앱',
    css_key='btn-primary'
)

import urllib3
import json
import base64

# openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
openApiURL = "http://aiopen.etri.re.kr:8000/HumanParsing"
accessKey = "cc902c9e-dd9b-4afa-bf83-3ffc585f81a2"
imageFilePath = "senior-3336451_640.jpg"
type = "jpg"
#위 입력예시) ---------
# https://pixabay.com/ko/photos/%EC%83%81%EC%9C%84-%EC%97%B0%EC%84%B8%EA%B0%80-%EB%93%9C%EC%8B%A0-%EC%82%AC%EB%9E%8C%EB%93%A4-3336451/
# imageFilePath = "./boardwalk.jpg"
# type = "jpg"
#-------------

file = open(imageFilePath, "rb")
imageContents = base64.b64encode(file.read()).decode("utf8")
file.close()

requestJson = {
    "argument": {
        "type": type,
        "file": imageContents
    }
}

http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8", "Authorization":accessKey},
    body=json.dumps(requestJson)
)

print("[responseCode] " + str(response.status))
print("[responBody]")
print(response.data) # print를 통해 결과가 json 형태로 나오는걸 보실수 있습니다.
#여기까지가 공통 샘플 소스이다. 이후 아래 소스는 API1, API2 기능별로 선택해서 사용-

# API1. 여기서부터는 샘플 소스 이후 사람속성 검출 API 시각화 소스
# 참고, 자바스크립트의 json과 파이썬의 딕셔너리는 같은 데이터 형이다.(아래)
data = json.loads(response.data) # string 형태의 json이라서 json.loads를 통해 읽어서 딕셔너리로 반환한다.
data_list = data.get("return_object") #딕셔너리에서 특정 값을 가져와서 딕셔너리로 반환한다.
print('사진에 있는 사람의 수와 복장 특징 목록')
for i in data_list: # 하나씩 가져다가 리스트로 출력하는 코드입니다.
    print(i,' = hair color:',data_list.get(i).get('hair color'),' coat color:',data_list.get(i).get('coat color'),' pants color:',data_list.get(i).get('pants color'))

# 대시보드 앱 시작(아래)
from dash import Dash, dcc, Input, Output, callback, callback_context, dash_table, State, html
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
from dash.dash_table.Format import Format, Group # , type:'numeric', format:Format(group=True, groups=[4])
from dash.exceptions import PreventUpdate

app = Dash('s_search_app',external_stylesheets=[dbc.themes.BOOTSTRAP]) # __name__ 사용하지 않는 대신에 하단에 @callback 처럼 사용
app.title = '사람속성 검출 AI를 사용한 웹 앱'
layout = dbc.Container([ # 멀티 파일로 실행 할 때
# app.layout = dbc.Container([ # 단일 파일로 실행 할 때
    html.H2(children='사람속성 검출 AI를 사용한 웹 앱'),
    html.Div(children=data_list),
    html.Div([
        dcc.Loading(id="loading-1", type="circle", children=html.Div(id="loading-output-1")),
    ],style={'position':'fixed','left':'50%','top':'50%','z-index':'9999'}),
])