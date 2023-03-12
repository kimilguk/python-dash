import dash # 멀티 파일로 실행 할 때 위 아래 줄 주석 해제
dash.register_page(
    __name__,
    title='주식 데이터를 가져오는 웹 앱',
    path='/stock_info_app',
    description='주식 데이터를 가져오는 웹 앱',
    css_key='btn-danger'
)
# 단일 파일로 실행하지 않고, 멀티 파일로 저장할 경우 제일 하단 서버실행은 주석처리한다.
# 주식 데이터를 가져오는 웹 앱
# %matplotlib inline
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

#----------------------------------------
# 한국 주식 종목 코드를 가져오는 함수
#----------------------------------------
def get_stock_info(maket_type=None):
    # 한국거래소(KRX)에서 전체 상장법인 목록 가져오기
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"
    if maket_type == 'kospi':
        marketType = "stockMkt"  # 주식 종목이 코스피인 경우
    elif maket_type == 'kosdaq':
        marketType = "kosdaqMkt" # 주식 종목이 코스닥인 경우
    elif maket_type == None:
        marketType = ""
    url = "{0}?method={1}&marketType={2}".format(base_url, method, marketType)

    df = pd.read_html(url, header=0)[0]
    
    # 종목코드 열을 6자리 숫자로 표시된 문자열로 변환
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")
    
    # 회사명과 종목코드 열 데이터만 남김
    df = df[['회사명','종목코드']]
    
    return df
#----------------------------------------------------
# yfinance에 이용할 Ticker 심볼을 반환하는 함수
#----------------------------------------------------
def get_ticker_symbol(company_name, maket_type):
    df = get_stock_info(maket_type)
    code = df[df['회사명']==company_name]['종목코드'].values
    code = code[0]
    
    if maket_type == 'kospi':
        ticker_symbol = code +".KS" # 코스피 주식의 심볼
    elif maket_type == 'kosdaq':
        ticker_symbol = code +".KQ" # 코스닥 주식의 심볼
    
    return ticker_symbol
#---------------------------------------------------------
ticker_symbol = get_ticker_symbol("삼성전자", "kospi") # 삼성전자, 주식 종류는 코스피로 지정
start_date = "2022-01-01"
end_date = "2022-01-31"
# ticker_data = yf.Ticker(ticker_symbol)
# df = ticker_data.history(start='2022-06-13', end='2022-06-18') # 시작일과 종료일 지정
df = yf.download(ticker_symbol, start=start_date, end=end_date)
print(df.head())
from matplotlib import font_manager as fm
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)
font_name = fm.FontProperties(fname=font_path).get_name() # 한글이 깨져 보일 때는. 아래 작업 후 반드시 주피터 노트북을 재 실핸 한다.
# print(matplotlib.get_cachedir()) # 폰트 캐시 위치, 만약 한글이 깨져 보이면 이 폴더 내를 지운다.rm -rf ~/.cache/matplotlib/*

# matplotlib을 이용한 그래프 그리기
matplotlib.rcParams['font.family'] = font_name # 'NanumGothic' 기본은 sans-serif로 전역 설정됨
matplotlib.rcParams['axes.unicode_minus'] = False # 마이너스(-) 폰트 깨짐 방지
# Axes : 보통 plot으로 생각하는 하나의 그래프. 각각의 Axes는 개별적으로 제목 및 x/y 레이블을 가질 수 있다.
# Axis : 번역하면 '축'인데, 그려지는 축을 말하는 것이 아니라 정확히는 x, y 의 제한 범위를 말한다
# pyplog로 간단하게 그래프 그리기
print(df.columns) #현재 컬럼명 확인
selected_columns = ['Open', 'Close'] # 관심있는 열만 선택
df2 = df[selected_columns].copy()     # 선택한 열만 다른 DataFrame으로 복사
df2.reset_index(inplace=True) # 기존 Data 인덱스가 컬럼으로 변경된다.
print(df2.columns) #현재 컬럼명 확인
df2.columns = ['등록일', '주가(시작가)', '주가(종가)'] # 컬럼명 한글로 변경
# ax = df['Close'].plot(grid=True, figsize=(15, 5)) #여기서는 Axes 출력
ax = df2.plot(x='등록일', y=['주가(시작가)', '주가(종가)'],grid=True, figsize=(15, 5)) 
ax.set_title("주가(종가) 그래프", fontsize=30) # 그래프 제목을 지정 , fontproperties=font_prop
ax.set_xlabel("기간", fontsize=20)             # x축 라벨을 지정 , fontproperties=font_prop
ax.set_ylabel("주가(원)", fontsize=20)         # y축 라벨을 지정 , fontproperties=font_prop
plt.xticks(fontsize=15)                        # X축 눈금값의 폰트 크기 지정
plt.yticks(fontsize=15)                        # Y축 눈금값의 폰트 크기 지정    
# display(type(ax.get_figure()))
# display(df['Close'].index)
plt.show()

# 2개의 선 그래프 출력: 플로틀리 모듈을 사용하면, matplotlab 모듈보다 인터렉티브(대화형) 하게 그래프를 조작할 수 있다.
import plotly.offline as pyo
import plotly.graph_objs as go
trace1 = go.Scatter(x=df['Open'].index, y=df['Open'], name = '시작가')
trace2 = go.Scatter(x=df['Close'].index, y=df['Close'], name = '종가')
# pyo.iplot([trace1,trace2])
layouts = go.Layout(
    title="주가(종가) 그래프",
    xaxis=dict(
        title="기간"
    ),
    yaxis=dict(
        title="주가(원)"
    ) 
)
pyo.iplot({'data': [trace1,trace2], 'layout': layouts})

#----------------------------------------------------
# 대시보드 앱 시작(아래) 
#----------------------------------------------------
from datetime import date # 날짜 계산 기술 참조 https://jsikim1.tistory.com/143
from dateutil.relativedelta import relativedelta
from dash import Dash, Input, Output, html, dcc, callback_context, callback #dcc(dash_core_components)
import plotly.express as px
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
from dash.dash_table.Format import Format, Group # , type:'numeric', format:Format(group=True, groups=[4])

# fig = px.line(df['Close'], title="주가(종가) 그래프")
# BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
# BS = app.get_asset_url('bootstrap.min.css') # 노트북에서는 상대경로는 않된다. 대신 py파일이 있는 폴더에서 assets 이란 폴더를 생성한 후 css를 넣는다.
# app.get_asset_url() 관련정보 https://dash.plotly.com/dash-enterprise/static-assets
# 실행 결과 assets 폴더에 저장된 CSS는 위 함수 없이도 앱에서 자동으로 읽어 들인다.
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP]) # __name__ 사용하지 않는 대신에 하단에 @callback 처럼 사용 dbc.themes.BOOTSTRAP
#Dash클래스에 프로그램 이름 내장변수로 app 객체 생성.파이썬 파일이 메인 프로그램으로 사용될 때는 __main__ 이 기본값
app.title = "주식 정보를 가져오는 웹 앱"
# app layout: html과 dcc 모듈을 이용
layout = html.Div(children=[ # 다중 파일 살행 시
# app.layout = html.Div(children=[ # 단일 파일 실행 시
    # Dash HTML Components module로 HTML 작성 
    html.H2(children='주식 정보를 가져오는 웹 앱'),
    html.Div([
        '검색시작일:',
        dcc.DatePickerSingle(
            id='start-date-picker',
            min_date_allowed=date(2000, 1, 1),
            max_date_allowed=date(2050, 12, 31),
            initial_visible_month=date.today() - relativedelta(months=1),
            display_format='YYYY-MM-DD',
            date=str(date.today() - relativedelta(months=1))
        ),
    ], style={'display':'inline-block'}),
    html.Div([
        '검색종료일:',
        dcc.DatePickerSingle(
            id='end-date-picker',
            min_date_allowed=date(2000, 1, 1),
            max_date_allowed=date(2050, 12, 31),
            initial_visible_month=date.today(),
            display_format='YYYY-MM-DD',
            date=str(date.today())
        ),
# 부트 스트랩 디자인 버튼 기술참조: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        dbc.Button("데이터 다운로드", color="primary", className="me-1", id="btn-download"),
#         html.Button("다운로드", id="btn-download"),
        dcc.Download(id="download-data"),
    ], style={'display':'inline-block'}),
    html.Div(id='output-container-date-picker-single'),
    html.Br(),
    # dash.core.components(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링
    html.Div([
        dcc.Graph(
            id='update_graph2',
#             figure=fig
        )
    ]),
    html.Br(),
    html.Div([
        '검색시작일:',
        dcc.DatePickerSingle(
            id='start-date-picker2',
            min_date_allowed=date(2000, 1, 1),
            max_date_allowed=date(2050, 12, 31),
            initial_visible_month=date.today() - relativedelta(months=1),
            display_format='YYYY-MM-DD',
            date=str(date.today() - relativedelta(months=1))
        ),
    ], style={'display':'inline-block'}),
    html.Div([
        '검색종료일:',
        dcc.DatePickerSingle(
            id='end-date-picker2',
            min_date_allowed=date(2000, 1, 1),
            max_date_allowed=date(2050, 12, 31),
            initial_visible_month=date.today(),
            display_format='YYYY-MM-DD',
            date=str(date.today())
        ),
    ], style={'display':'inline-block'}),
    html.Div([
        dcc.Graph(
            id='update_graph3',
#             figure=fig
        )
    ])
])

# 엑셀 다운로드 기술참조: https://dash.plotly.com/dash-core-components/download
@callback(
    Output("download-data", "data"),
    [Input("btn-download", "n_clicks"),Input('start-date-picker', 'date'),Input('end-date-picker', 'date')],
    prevent_initial_call=True, # 페이지 로드 시 콜백이 실행되지 않도록 
)
def func(n_clicks, start_date_value, end_date_value):
    if start_date_value is not None:
        start_date_object = date.fromisoformat(start_date_value)
        end_date_object = date.fromisoformat(end_date_value)
        start_date = start_date_object.strftime('%Y-%m-%d')
        end_date = end_date_object.strftime('%Y-%m-%d')
        df = yf.download(ticker_symbol, start=start_date, end=end_date)
    changed_id = [p['prop_id'] for p in callback_context.triggered][0] # 클릭,상태변경 이벤트 확인용 변수
    if 'btn-download' in changed_id:
        return dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")    
#     return dict(content="헬로 world!", filename="hello.txt")
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")
#     return dcc.send_file("./dash_docs/assets/images/gallery/dash-community-components.png")

# 그래프 1개 출력(아래)
@callback(
    Output(component_id='update_graph2', component_property='figure'),
    [Input('start-date-picker', 'date'),Input('end-date-picker', 'date')]
     )
def update_output(start_date_value, end_date_value):
    if start_date_value is not None:
        start_date_object = date.fromisoformat(start_date_value)
        end_date_object = date.fromisoformat(end_date_value)
        start_date = start_date_object.strftime('%Y-%m-%d')
        end_date = end_date_object.strftime('%Y-%m-%d')
        # 여기에 figure 객체 생성
        df = yf.download(ticker_symbol, start=start_date, end=end_date)
        selected_columns = ['Open', 'Close'] # 관심있는 열만 선택
        df2 = df[selected_columns].copy()     # 선택한 열만 다른 DataFrame으로 복사
        df2.columns = ['주가(시작가)', '주가(종가)'] # 컬럼명 한글로 변경
        fig = px.line(df2, title="주가(종가) 그래프", labels={"variable": "분류"})
#         fig = px.line(df['Close'], title="주가(종가) 그래프") # 단일 값 출력
        fig.update_layout(xaxis_title="기간", yaxis_title="주가(원)",title_text="주가(종가)그래프"+start_date+" ~ "+end_date, title_font_size=20)
        return (fig)
# 그래프 2개 출력(아래)
@callback(
    Output(component_id='update_graph3', component_property='figure'),
#     Output('output-container-date-picker-single', 'children'),
    [Input('start-date-picker2', 'date'),Input('end-date-picker2', 'date')]
     )
def update_output(start_date_value, end_date_value):
    if start_date_value is not None:
        start_date_object = date.fromisoformat(start_date_value)
        end_date_object = date.fromisoformat(end_date_value)
        start_date = start_date_object.strftime('%Y-%m-%d')
        end_date = end_date_object.strftime('%Y-%m-%d')
        # 여기에 figure 객체 생성
        df = yf.download(ticker_symbol, start=start_date, end=end_date)
        trace1 = go.Scatter(x=df['Open'].index, y=df['Open'], name = '시작가')
        trace2 = go.Scatter(x=df['Close'].index, y=df['Close'], name = '종가')
        fig = go.Figure(data=[trace1,trace2])
        fig.update_layout(xaxis_title="기간", yaxis_title="주가(원)",title_text="주가(시작가,종가)그래프"+start_date+" ~ "+end_date, title_font_size=20)
        return fig
#         date_string = start_date_object.strftime('%Y-%m-%d') +" | "+ end_date_object.strftime('%Y-%m-%d')
#         return date_string

# if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
#     app.run_server(debug=False, host='0.0.0.0', port=8888)
