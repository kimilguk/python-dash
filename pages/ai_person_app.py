#-*- coding:utf-8 -*-
import urllib3
import json
import base64

# AI API 결과를 가져와 DataFrame 데이터로 반환하는 함수로 기존 터미널 전용코드를 감싸준다.
def get_api(query):
    # openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    openApiURL = "http://aiopen.etri.re.kr:8000/HumanParsing"
    accessKey = "cc902c9e-dd9b-4afa-bf83-3ffc585f81a2"
    imageFilePath = query
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
    # 데이터프레임 사용에 필요한 판다스 모듈 임포트
    import pandas as pd

    #####################################################################
    # dsah_table 모듈사용 시(아래) 
    # 데이터 프레임 생성
    df_person = pd.DataFrame(data_list) # 딕셔너리 데이터를 판다스 DataFrame으로 변환
    df_person = df_person.transpose() # 딕셔너리 데이터의 행열 변환
    # print(df_person.columns) # 컬럼출력
    df_person = df_person[['hair color','coat color','pants color']]
    df_person.columns = ['머리색상', '상의색상', '바지색상'] # 열 이름 변경
    df_person = df_person.reset_index().rename(columns={'index':'사람객체명'}) # 인덱스 명 출력
    print(df_person.head()) # 많은 데이터 중 상위 몇개만 표시
    #######################################################################

    #######################################################################
    # 데이터프레임.to_html()을 사용하여 웹용으로 변경 사용 시(아래)
    person_list = [] # 개체(json=dictionary) 배열변수 추가
    for i in data_list: # 하나씩 가져다가 리스트로 출력하는 코드입니다.
        person_list.extend([{
        'person':i,
        'hair color':'<div style="height:15px;width:15px;background-color:rgb'+data_list.get(i).get('hair color')+';display: inline-block;"></div>'+data_list.get(i).get('hair color'),
        'coat color':'<div style="height:15px;width:15px;background-color:rgb'+data_list.get(i).get('coat color')+';display: inline-block;"></div>'+data_list.get(i).get('coat color'),
        'pants color':'<div style="height:15px;width:15px;background-color:rgb'+data_list.get(i).get('pants color')+';display: inline-block;"></div>'+data_list.get(i).get('pants color')
        }])
        #print(i,' = hair color:',data_list.get(i).get('hair color'),' coat color:',data_list.get(i).get('coat color'),' pants color:',data_list.get(i).get('pants color'))
    # print(person_list)
    df_person_html = pd.DataFrame(person_list) # 딕셔너리 데이터를 판다스 DataFrame으로 변환
    # print(df_person.columns)
    df_person_html.columns = ['사람객체명', '머리색상', '상의색상', '바지색상'] # 열 이름 변경
    print(df_person_html.head()) # 많은 데이터 중 상위 몇개만 표시
    html_table = df_person_html.to_html(index=False, escape=False) # 데이터프레임을 문자열로 변경
    #####################################################################
    # 위 소스 까지가 기존 터미널 출력 소스이고 함수로 묶어주면 아래 리턴값이 발생한다.
    return df_person, html_table
# 위 소스는 루트에서 ai_person_app.py 로 생성한 수업소스를 그대로 가져오고, 
# 웹에서 사용하는 코드는 아래 부터 소스를 추가해 나가는 방식으로 수업이 진행된다.

#####################################################################
query = "assets/senior-3336451_640.jpg"
[df_person, html_table] = get_api(query)
# 대시보드 앱 시작(아래)
# 단일 파일로 실행 할 때 아래 멀티 dash페이지등록 부분 8줄코드 주석처리 후 제일 하단 app.run_server 코드는 주석해제
import dash
dash.register_page(
    __name__,
    title='사람속성 검출 AI를 사용한 웹 앱',
    path='/ai_person_app',
    description='사람속성 검출 AI를 사용한 웹 앱',
    css_key='btn-primary'
)

from dash import Dash, dcc, Input, Output, callback, callback_context, dash_table, State, html
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
from dash.dash_table.Format import Format, Group # , type:'numeric', format:Format(group=True, groups=[4])
from dash.exceptions import PreventUpdate

app = Dash('ai_person_app',external_stylesheets=[dbc.themes.BOOTSTRAP]) # __name__ 사용하지 않는 대신에 하단에 @callback 처럼 사용
app.title = '사람속성 검출 AI를 사용한 웹 앱'
# img_names = ['senior-3336451_640.jpg', 'people-7358064_640.jpg']
layout = dbc.Container([ # 멀티 파일로 실행 할 때
# app.layout = dbc.Container([ # 단일 파일로 실행 할 때
    html.H2(children='사람속성 검출 AI를 사용한 웹 앱'),
    html.Div(children=[
        # html.Img(src=app.get_asset_url('senior-3336451_640.jpg'), width="300"),
        # dcc.RadioItems(img_names, img_names[0], id="img-picker", ),
        dcc.RadioItems([
            {
                "label": html.Div(
                    [
                        html.Img(src="/assets/senior-3336451_640.jpg", height=200),
                        html.Div("샘플이미지1", style={'font-size': 15,'padding-left': 10}),
                    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'left'}
                ),
                "value": "senior-3336451_640.jpg",
            },
            {
                "label": html.Div(
                    [
                        html.Img(src="/assets/people-7358064_640.jpg", height=200),
                        html.Div("샘플이미지2", style={'font-size': 15, 'padding-left': 10}),
                    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'left','padding-left': 10}
                ),
                "value": "people-7358064_640.jpg",
            }
        ],"senior-3336451_640.jpg",id="img-picker", inline=True)
    ]),
    html.Div([
        html.Span('', id='errors6'),
    ], style={'display':'inline-block','color':'red'}),
    dbc.Button("검출시작", color="primary", className="me-1", id="btn_search6",
               style={'display':'inline-block','width':'100px','vertical-align':'inherit'}),
    dash_table.DataTable( # 스타일 참조: https://dash.plotly.com/datatable/style
        columns=[
        {'id': i, "name": i, 'presentation': 'markdown'} for i in df_person.columns], # , 'presentation': 'markdown'
        id='tbl6',
        data=df_person.to_dict("records"),
        style_header={'textAlign': 'center'},
        style_cell={'textAlign': 'left'},
    ),
    html.Div(children=[
            dcc.Markdown(html_table, dangerously_allow_html=True, id="html_table")
        ]),
    html.Div([
        dcc.Loading(id="loading-6", type="circle", children=html.Div(id="loading-output-6")),
    ],style={'position':'fixed','left':'50%','top':'50%','z-index':'9999'}),
])
@callback (
    [Output('tbl6','data'),Output('errors6','children'),Output('html_table','children'),Output("loading-output-6","children")],
    [Input('img-picker','value'),Input("btn_search6", "n_clicks")],
    [State('tbl6', 'data')], # 기존 값 가져오기
#     prevent_initial_call=True, # 페이지 로드 시 콜백이 실행되지 않도록 
)
def update_table(value, n_clicks, data):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0] # 클릭,상태변경 이벤트 확인용 변수
    if 'img-picker' in changed_id:
        raise PreventUpdate
    if 'btn_search6' in changed_id:
        try:
            print('이벤트-콜백함수시작 try', value)
            value = "assets/"+value
            [df_person, html_table] = get_api(value)
            data=df_person.to_dict("records")
        except:
            print('이벤트-콜백함수시작 except', value)
            value = "assets/senior-3336451_640.jpg"
            [df_person, html_table] = get_api(value)
            data=df_person.to_dict("records")
        return data, value, html_table, ''

# if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
#     app.run_server(debug=False, host='0.0.0.0', port=8888) # 단일 파일로 실행 할 때
# Dash Core Components 기술참조 : https://dash.plotly.com/dash-core-components/radioitems
# 데이터과학 기술참조: http://bigdata.dongguk.ac.kr/lectures/datascience/_book/index.html
# 사용된 픽사베이 무료 이미지 2개(아래)
# https://pixabay.com/ko/photos/%EC%83%81%EC%9C%84-%EC%97%B0%EC%84%B8%EA%B0%80-%EB%93%9C%EC%8B%A0-%EC%82%AC%EB%9E%8C%EB%93%A4-3336451/
# https://pixabay.com/ko/photos/%EC%82%AC%EB%9E%8C%EB%93%A4-%EA%B1%B7%EB%8A%94-%EC%82%B0%EB%B3%B4-%EC%96%B4%EB%A6%B0%EC%9D%B4%EB%93%A4-7358064/
# 