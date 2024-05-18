import dash # 멀티 파일로 실행 할 때 위 아래 줄 주석 해제
dash.register_page(
    __name__,
    title='환율 데이터를 가져오는 웹 앱',
    path='/exchange_rate_app',
    description='환율 데이터를 가져오는 웹 앱',
    css_key='btn-info'
)
# 단일 파일로 실행하지 않고, 멀티 파일로 저장할 경우 제일 하단 서버실행은 주석처리한다.
# 환율 데이터를 가져오는 웹 앱
import pandas as pd
import datetime
import time
# import matplotlib.pyplot as plt
# import matplotlib
from io import BytesIO

# -----------------------------------------------------------------------------
# 날짜별 환율 데이터를 반환하는 함수
# - 입력 인수: currency_code(통화코드), last_page_num(페이지 수)
# - 반환: 환율 데이터 프레임 dataframe
# -----------------------------------------------------------------------------
def get_exchange_rate_data(currency_code, last_page_num):
    base_url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn"
    df = pd.DataFrame()
    
    for page_num in range(1, last_page_num+1):
        url = f"{base_url}?marketindexCd={currency_code}&page={page_num}"
        dfs = pd.read_html(url, header=1)
        
        # 통화 코드가 잘못 지정됐거나 마지막 페이지의 경우 for 문을 빠져나옴
        if dfs[0].empty:
            if (page_num==1):
                print(f"통화 코드({currency_code})가 잘못 지정됐습니다.")
            else:
                print(f"{page_num}가 마지막 페이지입니다.")
            break
            
        # page별로 가져온 DataFrame 데이터 연결
        df = pd.concat([df, dfs[0]], ignore_index=True)
        time.sleep(0.1) # 0.1초간 멈춤
        
    return df
# -----------------------------------------------------------------------------
currency_name_symbols = {"미국 달러":"USD", "유럽연합 유로":"EUR", "일본 엔(100)":"JPY", "중국 위안":"CNY"}
currency_name = list(currency_name_symbols.keys())[0] #dict 데이터 반환 dict_keys(['미국 달러', '유럽연합 유로', '일본 엔(100)', '중국 위안'])
print(currency_name)
currency_symbol = currency_name_symbols[currency_name] # 환율 심볼 선택
currency_code = f"FX_{currency_symbol}KRW"
print(currency_code)
last_page_num = 20 # 네이버 금융에서 가져올 최대 페이지 번호 지정
# 지정한 환율 코드를 이용해 환율 데이터 가져오기
df_exchange_rate = get_exchange_rate_data(currency_code, last_page_num)
# 원하는 열만 선택
df_exchange_rate = df_exchange_rate[['날짜', '매매기준율','사실 때', '파실 때', '보내실 때', '받으실 때']]
# 최신 데이터와 과거 데이터의 순서를 바꿔 df_exchange_rate2에 할당
df_exchange_rate2 = df_exchange_rate[::-1].reset_index(drop=True)
# df_exchange_rate2의 index를 날짜 열의 데이터로 변경
df_exchange_rate2 = df_exchange_rate2.set_index('날짜')
# df_exchange_rate2의 index를 datetime 형식으로 변환
print('여기1',df_exchange_rate2.index)
#df_exchange_rate2.index = df_exchange_rate2.index.replace('.', '-')
print('여기2',df_exchange_rate2)
df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index,format='%Y-%m-%d')
# 1) 환율 데이터 표시
# display(df_exchange_rate.tail())  # 환율 데이터 표시(앞의 일부만 표시)
# display(df_exchange_rate2.head())  # 환율 데이터 표시(앞의 일부만 표시)

# # # 2) 차트 그리기
# # matplotlib을 이용한 그래프에 한글을 표시하기 위한 설정
# matplotlib.rcParams['font.family'] = 'NanumGothic'
# matplotlib.rcParams['axes.unicode_minus'] = False

# # # 선 그래프 그리기 (df_exchange_rate2 이용)
# ax = df_exchange_rate2['매매기준율'].plot(grid=True, figsize=(15, 5))
# ax.set_title("환율(매매기준율) 그래프", fontsize=30) # 그래프 제목을 지정
# ax.set_xlabel("기간", fontsize=20)                   # x축 라벨을 지정
# ax.set_ylabel(f"원화/{currency_name}", fontsize=20)  # y축 라벨을 지정
# plt.xticks(fontsize=15)             # X축 눈금값의 폰트 크기 지정
# plt.yticks(fontsize=15)             # Y축 눈금값의 폰트 크기 지정
# plt.show()
# # display(type(ax.get_figure()))
# # fig = ax.get_figure()               # fig 객체 가져오기 dsah 에서 에러나서 하단의 fig로 교체

#----------------------------------------------------
# 대시보드 앱 시작(아래) 
#----------------------------------------------------
from datetime import date # 날짜 계산 기술 참조 https://jsikim1.tistory.com/143
from dateutil.relativedelta import relativedelta
from dash import Dash, Input, Output, html, dcc, callback_context, callback #dcc(dash_core_components)
import plotly.express as px
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
from dash.dash_table.Format import Format, Group # , type:'numeric', format:Format(group=True, groups=[4])

# fig = px.line(df_exchange_rate2['매매기준율'], title="환율(매매기준율) 그래프", labels={"variable": "분류"}) # 단일 값 출력
# fig.update_layout(yaxis_title=f"원화/{currency_name}"
#                   , title_font_size=30, xaxis_title_font_size=20, yaxis_title_font_size=20)

app = Dash('exchange_rate_app',external_stylesheets=[dbc.themes.BOOTSTRAP]) # __name__ 사용하지 않는 대신에 하단에 @callback 처럼 사용 dbc.themes.BOOTSTRAP
#Dash클래스에 프로그램 이름 내장변수로 app 객체 생성.파이썬 파일이 메인 프로그램으로 사용될 때는 __main__ 이 기본값
app.title = "환율 정보를 가져오는 웹 앱"
# app layout: html과 dcc 모듈을 이용
layout = html.Div(children=[ # 멀티 파일에서 사용
# app.layout = html.Div(children=[ # 단일 파일에서 사용
    # Dash HTML Components module로 HTML 작성 
    html.H2(children='환율 정보를 가져오는 웹 앱'),
    html.Div([
        html.Span('환율 데이터 선택하기:', style={'vertical-align':'middle'}),
#         dbc.Dropdown(
#             id="my-dropdown",
#             options=currency_name_symbols,
#             value=currency_name,
#             searchable=False,
#             style={'display':'inline-block','width':200, 'vertical-align':'middle'}
#         ),
        dbc.Select(
            id="my-dropdown",
            options=currency_name_symbols,
            value=currency_name,
            style={'display':'inline-block','width':200, 'vertical-align':'middle'}
        )
    ], style={'display':'inline-block'}),
    html.Div([
# 부트 스트랩 디자인 버튼 기술참조: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button/
        dbc.Button("데이터 다운로드", color="primary", className="me-1", id="btn-download1"),
#         html.Button("다운로드", id="btn-download"),
        dcc.Download(id="download-data1"),
    ], style={'display':'inline-block'}),
    html.Br(),
    # dash.core.components(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링
    html.Div([
        dcc.Graph(
            id='update_graph4',
#             figure=fig
        )
    ]),
])

# 엑셀 다운로드 기술참조: https://dash.plotly.com/dash-core-components/download
@callback(
    Output("download-data1", "data"),
    [Input("btn-download1", "n_clicks"),Input('my-dropdown', 'value')],# 반드시 value 로 해야 한다.
    prevent_initial_call=True, # 페이지 로드 시 콜백이 실행되지 않도록 
)
def func(n_clicks, my_dropdown_value):
    global currency_name_symbols, last_page_num
#     global df_exchange_rate2 # 빈 테이터 프레임 만들고, 전역변수로 할당 = pd.DataFrame()
    if my_dropdown_value is not None:
        currency_symbol = currency_name_symbols[my_dropdown_value] # 환율 심볼 선택
        currency_code = f"FX_{currency_symbol}KRW"
        print(currency_code)
        print(last_page_num)
        # 지정한 환율 코드를 이용해 환율 데이터 가져오기
        df_exchange_rate = get_exchange_rate_data(currency_code, last_page_num)
        # 원하는 열만 선택
        df_exchange_rate = df_exchange_rate[['날짜', '매매기준율','사실 때', '파실 때', '보내실 때', '받으실 때']]
        # 최신 데이터와 과거 데이터의 순서를 바꿔 df_exchange_rate2에 할당
        df_exchange_rate2 = df_exchange_rate[::-1].reset_index(drop=True)
        # df_exchange_rate2의 index를 날짜 열의 데이터로 변경
        df_exchange_rate2 = df_exchange_rate2.set_index('날짜')
        # df_exchange_rate2의 index를 datetime 형식으로 변환
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index,format='%Y-%m-%d')
    changed_id = [p['prop_id'] for p in callback_context.triggered][0] # 클릭,상태변경 이벤트 확인용 변수
    if 'btn-download' in changed_id:
        return dcc.send_data_frame(df_exchange_rate2.to_excel, "mydf.xlsx", sheet_name=f"Sheet_원화_vs_{my_dropdown_value}")    
#     return dict(content="헬로 world!", filename="hello.txt")
#     return dcc.send_data_frame(df.to_csv, "mydf.csv")
#     return dcc.send_file("./dash_docs/assets/images/gallery/dash-community-components.png")

# 그래프 1개 출력(아래)
@callback(
    Output(component_id='update_graph4', component_property='figure'),
    Input('my-dropdown', 'value')
    )
def update_output(my_dropdown_value):
    global currency_name_symbols, last_page_num
    if my_dropdown_value is not None:
        # 여기에 figure 객체 생성
        currency_name_symbols = {"미국 달러":"USD", "유럽연합 유로":"EUR", "일본 엔(100)":"JPY", "중국 위안":"CNY"}
        currency_symbol = currency_name_symbols[my_dropdown_value] # 환율 심볼 선택
        currency_code = f"FX_{currency_symbol}KRW"
        print(currency_code)
        print(last_page_num)
        # 지정한 환율 코드를 이용해 환율 데이터 가져오기
        df_exchange_rate = get_exchange_rate_data(currency_code, last_page_num)
        # 원하는 열만 선택
        df_exchange_rate = df_exchange_rate[['날짜', '매매기준율','사실 때', '파실 때', '보내실 때', '받으실 때']]
        # 최신 데이터와 과거 데이터의 순서를 바꿔 df_exchange_rate2에 할당
        df_exchange_rate2 = df_exchange_rate[::-1].reset_index(drop=True)
        # df_exchange_rate2의 index를 날짜 열의 데이터로 변경
        df_exchange_rate2 = df_exchange_rate2.set_index('날짜')
        # df_exchange_rate2의 index를 datetime 형식으로 변환
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index,format='%Y-%m-%d')
        fig = px.line(df_exchange_rate2['매매기준율'], title="환율(매매기준율) 그래프", labels={"variable": "분류"}) # 단일 값 출력
        fig.update_layout(yaxis_title=f"원화/{my_dropdown_value}"
                  , title_font_size=30, xaxis_title_font_size=20, yaxis_title_font_size=20)
        return fig

# if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
#     app.run_server(debug=False, host='0.0.0.0', port=8888)
