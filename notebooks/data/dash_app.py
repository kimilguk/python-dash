from dash import Dash, html, dcc #dcc(dash_core_components)
import plotly.express as px
import pandas as pd

df = px.data.iris() # 판다스에 내장된 iris함수로 data 불러오기: 분꽃 종류별 데이터
#display(df) #sepal(꽃받침)과 petal(꽃잎)의 가로,세로 크기로 setosa, versicolor, virginica 3가지 종류로 구분
# plotly를 이용한 산점도(스캐터) 그래프 객체 생성
fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")

app = Dash(__name__) #Dash클래스에 프로그램 이름 내장변수로 app 객체 생성
# app layout: html과 dcc 모듈을 이용
app.layout = html.Div(children=[
    # Dash HTML Components module로 HTML 작성 
    html.H1(children='첫번째 Dash 연습'),
    html.Div(children='''
        대시를 이용하여 웹어플리케이션 작성 연습...
    '''),
    # dash.core.components(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링
    dcc.Graph(
        id='graph1',
        figure=fig
    )
])

if __name__ == '__main__': #스크립트 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
    app.run_server(debug=False, host='0.0.0.0', port=8888)
