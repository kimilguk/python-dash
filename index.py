# -*- coding: utf-8 -*-
# 위 코드는 이문서가 파이썬에서 컴파일(번역)될 때 ascii 아스키(영어전용) 코드가 아닌 utf-8(한글지원) 코드라는 것을 명시한다.
# (파이썬 버전 3 이상 에서는 기본이 utf-8 이라서 필요없다.)
# 우선 파이썬과 주피터 노트북의 버전을 확인 한다. python --version, jupyter --version
# 주피터 노트북의 IDE에서 인터랙티브한 실행 환경을 제공하는 ipython 버전을 확인 한다. pip3 show ipython
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
# CDN(Contents Delivery Network)으로 외부 CSS 불러오기
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 6],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='헬로 Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
    #app.run_server(debug=True)
    #실행 명령: python app.py