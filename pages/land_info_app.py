import dash # 멀티 파일로 실행 할 때 위 아래 줄 주석 해제
dash.register_page(
    __name__,
    title='부동산 정보를 가져오는 웹 앱',
    path='/land_info_app',
    description='부동산 정보를 가져오는 웹 앱',
    css_key='btn-warning'
)
# 단일 파일로 실행하지 않고, 멀티 파일로 저장할 경우 제일 하단 서버실행은 주석처리한다.
# %%writefile C:\myPyScraping\code\ch09\land_info_app.py
# 부동산 데이터를 가져오는 웹 앱
import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib

# 원본 DataFrame의 제목 열에 있는 문자열을 분리해
# 전국, 서울, 수도권의 매매가 변화율 열이 있는 DataFrame 반환하는 함수
#----------------------------------------------------------------------------------
def split_title_to_rates(df_org):
    df_new = df_org.copy()
    df_temp = df_new['제목'].str.replace('%', '') # 제목 문자열에서 % 제거
    df_temp = df_temp.str.replace('보합', '0')    # 제목 문자열에서 보합을 0으로 바꿈
    df_temp = df_temp.str.replace('보합세', '0')  # 제목 문자열에서 보합세를 0으로 바꿈
    regions = ['전국', '서울', '수도권']
    for region in regions:
        df_temp = df_temp.str.replace(region, '') # 문자열에서 전국, 서울, 수도권 제거
    df_temp = df_temp.str.split(']', expand=True) # ]를 기준으로 열 분리
    df_temp = df_temp[1].str.split(',', expand=True) # ,를 기준으로 열 분리
    df_temp = df_temp.astype(float)
    df_new[regions] = df_temp # 전국, 서울, 수도권 순서대로 DataFrame 데이터에 할당
    return df_new[['등록일'] + regions + ['번호']] # DataFrame에서 필요한 열만 반환
#----------------------------------------------------------------------------------
base_url = "https://land.naver.com/news/trendReport.naver"
df_rates = pd.DataFrame() # 전체 데이터가 담길 DataFrame 데이터
last_page_num = 2 # 가져올 데이터의 마지막 페이지
for page_num in range(1, last_page_num+1):
    url = f"{base_url}?page={page_num}"
    dfs = pd.read_html(url)
    df_page = dfs[0] # 리스트의 첫 번째 항목에 동향 보고서 제목 데이터가 있음
    df_rate = split_title_to_rates(df_page)
    # 세로 방향으로 연결 (기존 index를 무시)
    df_rates = pd.concat([df_rates, df_rate], ignore_index=True)
# 최신 데이터와 과거 데이터의 순서를 바꿈. index도 초기화함
df_rates_for_chart = df_rates[::-1].reset_index(drop=True)
print(df_rates_for_chart.head())
selected_regions = ['전국','서울','수도권']
# # 차트 그리기
# # matplotlib을 이용한 그래프에 한글을 표시하기 위한 설정
# matplotlib.rcParams['font.family'] = 'NanumGothic'
# matplotlib.rcParams['axes.unicode_minus'] = False
# # 선 그래프 그리기 -o 사용
# ax = df_rates_for_chart.plot(x='등록일', y=selected_regions, figsize=(15, 6),
#                              style = '-o', grid=True) # 그래프 그리기
# ax.set_title("아파트 매매가 변화율", fontsize=30) # 그래프 제목을 지정
# ax.set_xlabel("날짜", fontsize=20)                # x축 라벨을 지정
# ax.set_ylabel("변화율(%)", fontsize=20)           # y축 라벨을 지정
# plt.xticks(fontsize=15)             # X축 눈금값의 폰트 크기 지정
# plt.yticks(fontsize=15)             # Y축 눈금값의 폰트 크기 지정
# plt.show()

# display(type(ax.get_figure()))
# fig = ax.get_figure()               # fig 객체 가져오기 dsah 에서 에러나서 하단의 fig로 교체

#----------------------------------------------------
# 대시보드 앱 시작(아래) 
#----------------------------------------------------
from datetime import date # 날짜 계산 기술 참조 https://jsikim1.tistory.com/143
from dateutil.relativedelta import relativedelta
from dash import Dash, Input, Output, html, dcc, callback, callback_context #dcc(dash_core_components)
import plotly.express as px
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
from dash.dash_table.Format import Format, Group # , type:'numeric', format:Format(group=True, groups=[4])

# 인덱스를 주면 x 축 값이 생성 된다.
df_rates_for_chart = df_rates_for_chart.set_index('등록일')
# koyeb에서 에러나서 format변경
# df_rates_for_chart.index = pd.to_datetime(df_rates_for_chart.index,format='%Y-%m')
df_rates_for_chart.index = pd.to_datetime(df_rates_for_chart.index,format='mixed')
# fig = px.line(df_rates_for_chart[selected_regions], title="아파트의 매매가 변화율", labels={"variable": "분류"}) # 단일 값 출력
# fig.update_layout(xaxis_title="날짜", yaxis_title="변화율(%)"
#                   , title_font_size=30, xaxis_title_font_size=20, yaxis_title_font_size=20)

app = Dash('land_info_app',external_stylesheets=[dbc.themes.BOOTSTRAP]) # __name__ 사용하지 않는 대신에 하단에 @callback 처럼 사용 dbc.themes.BOOTSTRAP
app.title = "부동산 정보를 가져오는 웹 앱"
# app.layout = html.Div([ # 단일 파일로 실행할 때
layout = html.Div([ # 멀티 파일로 실행할 때
    html.H2(children='부동산 정보를 가져오는 웹 앱'),
    html.Div([
        dcc.Checklist(
            options=selected_regions,
            value=selected_regions,
            id='demo-check'
        ),
    ]),
    html.Br(),
    # dash.core.components(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링
    html.Div([
        dcc.Graph(
            id='update_graph',
#             figure=fig
        )
    ]),
    html.Div(id='dd-output-container'),
    html.Div([
        dcc.Loading(id="loading-2", type="default", children=html.Div(id="loading-output-2")),
    ],style={'position':'fixed','left':'50%','top':'50%','z-index':'9999'}),
])
# 아래 콜백 함수에서 항상 Output 이 먼저 와야 한다.
@callback(
    [Output(component_id='update_graph', component_property='figure'),Output('dd-output-container', 'children'),Output('loading-output-2', 'children')],
    Input('demo-check', 'value'),
)
# update_output 는 콜백으로 자동실행된다.
def update_output(value):
    if value is not None:
        fig = px.line(df_rates_for_chart[value], title="아파트의 매매가 변화율", labels={"variable": "분류"}) # 단일 값 출력
        fig.update_layout(xaxis_title="날짜", yaxis_title="변화율(%)"
                  , title_font_size=30, xaxis_title_font_size=20, yaxis_title_font_size=20)
        return fig, f'You have selected {value}', ''

# if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
#     app.run_server(debug=False, host='0.0.0.0', port=8888) # 단일 파일로 실행 할 때