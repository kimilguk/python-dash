import dash # 멀티 파일로 실행 할 때 위 아래 줄 주석 해제
dash.register_page(
    __name__,
    title='콜백 Dash 연습 웹 앱',
    path='/',
    description='콜백 Dash 연습 웹 앱',
    css_key='btn-success'
)
from dash import Dash, Input, Output, html, dcc, callback #dcc(dash_core_components)
import plotly.express as px
import pandas as pd

df = px.data.iris() # 판다스에 내장된 iris함수로 data 불러오기: 분꽃 종류별 데이터
print(df) #sepal(꽃받침)과 petal(꽃잎)의 길이,너비 크기로 setosa, versicolor, virginica 3가지 종류로 구분
# plotly를 이용한 산점도(스캐터) 그래프 객체 생성
# fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")
col_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
app = Dash(__name__) #Dash클래스에 프로그램 이름 내장변수로 app 객체 생성.파이썬 파일이 메인 프로그램으로 사용될 때는 __main__ 이 기본값
# app layout: html과 dcc 모듈을 이용
app.title = "콜백 Dash 연습"
layout = html.Div(children=[ # 다중 파일 실행 시
# app.layout = html.Div(children=[ # 단일 파일 실행 시
    # Dash HTML Components module로 HTML 작성 
    html.H2(children='콜백 Dash 연습'),
    html.Div([
        'X-변수:',
        dcc.Dropdown(id="xvar_name",
                    options=col_names,
                    value=col_names[0],
                    placeholder="X축을 컬럼을 선택하세요"),
    ], style={'width':'30%', 'display':'inline-block'}),
    html.Div([
        'Y-변수:',
        dcc.Dropdown(id="yvar_name",
                    options=col_names,
                    value=col_names[1],
                    placeholder="Y축을 컬럼을 선택하세요"),
    ], style={'width':'30%', 'display':'inline-block'}),
    html.Br(),
    # dash.core.components(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링
    html.Div([
        dcc.Graph(
            id='update_graph1'
        )
    ])
])

@callback(
    Output(component_id='update_graph1', component_property='figure'),
    Input(component_id='xvar_name', component_property='value'),
    Input('yvar_name', 'value')
)
def update_graphs(xvar, yvar):
    # 여기에 figure 객체 생성
    fig = px.scatter(df, x=xvar, y=yvar, color="species", width=1000, height=700)
    fig.update_layout(title_text="스캐터 Plot of"+xvar+" vs "+yvar, title_font_size=30)
    return fig

# if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
#     app.run_server(debug=False, host='0.0.0.0', port=8888)
