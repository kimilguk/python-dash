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
import requests
# import matplotlib.pyplot as plt
# import matplotlib
from io import BytesIO

# -----------------------------------------------------------------------------
# 날짜별 환율 데이터를 반환하는 함수
# - 입력 인수: currency_code(통화코드), last_page_num(조회할 기간 단위 수)
# - 반환: 환율 데이터 프레임 dataframe
# -----------------------------------------------------------------------------
def get_exchange_rate_data(currency_code, last_page_num):
    """Frankfurter API에서 최근 영업일 환율 데이터를 가져옵니다.

    기존 Naver Finance HTML 페이지는 더 이상 안정적으로 제공되지 않으므로,
    ECB 기준 환율을 제공하는 공개 Frankfurter API를 사용합니다.
    """
    base_currency = currency_code.removeprefix('FX_').removesuffix('KRW')
    end_date = datetime.date.today()
    # 기존 20페이지(페이지당 약 10일)와 비슷한 기간을 조회합니다.
    start_date = end_date - datetime.timedelta(days=last_page_num * 10)
    url = (
        f"https://api.frankfurter.dev/v1/{start_date.isoformat()}.."
        f"{end_date.isoformat()}?base={base_currency}&symbols=KRW"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    payload = response.json()
    rows = [
        {
            '날짜': rate_date,
            '매매기준율': values['KRW'],
            # Frankfurter는 기준환율만 제공하므로 현찰/송금 환율은 제공하지 않습니다.
            '사실 때': pd.NA,
            '파실 때': pd.NA,
            '보내실 때': pd.NA,
            '받으실 때': pd.NA,
        }
        for rate_date, values in payload.get('rates', {}).items()
        if 'KRW' in values
    ]

    if not rows:
        raise ValueError(f"{currency_code}에 대한 환율 데이터가 없습니다.")

    return pd.DataFrame(rows).sort_values('날짜').reset_index(drop=True)
# -----------------------------------------------------------------------------
currency_name_symbols = {"미국 달러":"USD", "유럽연합 유로":"EUR", "일본 엔(100)":"JPY", "중국 위안":"CNY"}
currency_name = list(currency_name_symbols.keys())[0] #dict 데이터 반환 dict_keys(['미국 달러', '유럽연합 유로', '일본 엔(100)', '중국 위안'])
print(currency_name)
currency_symbol = currency_name_symbols[currency_name] # 환율 심볼 선택
currency_code = f"FX_{currency_symbol}KRW"
print(currency_code)
last_page_num = 20 # 최근 영업일 데이터 조회 기간 단위 지정
# 지정한 환율 코드를 이용해 환율 데이터 가져오기
df_exchange_rate = get_exchange_rate_data(currency_code, last_page_num)
# 최신 데이터와 과거 데이터의 순서를 바꿔 df_exchange_rate2에 할당
df_exchange_rate2 = df_exchange_rate[::-1].reset_index(drop=True)
# df_exchange_rate2의 index를 날짜 열의 데이터로 변경
df_exchange_rate2 = df_exchange_rate2.set_index('날짜')
# df_exchange_rate2의 index를 datetime 형식으로 변환
df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index, format='mixed')

#----------------------------------------------------
# 대시보드 앱 시작(아래) 
#----------------------------------------------------
from datetime import date
from dateutil.relativedelta import relativedelta
from dash import Dash, Input, Output, html, dcc, callback_context, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Group

app = Dash('exchange_rate_app', external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "환율 정보를 가져오는 웹 앱"
layout = html.Div(children=[
    html.H2(children='환율 정보를 가져오는 웹 앱'),
    html.Div([
        html.Span('환율 데이터 선택하기:', style={'vertical-align':'middle'}),
        dbc.Select(
            id="my-dropdown",
            options=currency_name_symbols,
            value=currency_name,
            style={'display':'inline-block','width':200,'vertical-align':'middle'}
        )
    ], style={'display':'inline-block'}),
    html.Div([
        dbc.Button("데이터 다운로드", color="primary", className="me-1", id="btn-download1"),
        dcc.Download(id="download-data1"),
    ], style={'display':'inline-block'}),
    html.Br(),
    html.Div([dcc.Graph(id='update_graph4')]),
])

# 엑셀 다운로드
@callback(
    Output("download-data1", "data"),
    [Input("btn-download1", "n_clicks"), Input('my-dropdown', 'value')],
    prevent_initial_call=True,
)
def func(n_clicks, my_dropdown_value):
    if my_dropdown_value is not None:
        currency_symbol = currency_name_symbols[my_dropdown_value]
        currency_code = f"FX_{currency_symbol}KRW"
        df_exchange_rate = get_exchange_rate_data(currency_code, last_page_num)
        df_exchange_rate2 = df_exchange_rate[::-1].reset_index(drop=True).set_index('날짜')
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index, format='mixed')

    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-download' in changed_id:
        return dcc.send_data_frame(
            df_exchange_rate2.to_excel,
            "mydf.xlsx",
            sheet_name=f"Sheet_원화_vs_{my_dropdown_value}"
        )

# 그래프 1개 출력
@callback(
    Output(component_id='update_graph4', component_property='figure'),
    Input('my-dropdown', 'value')
)
def update_output(my_dropdown_value):
    if my_dropdown_value is not None:
        currency_symbol = currency_name_symbols[my_dropdown_value]
        currency_code = f"FX_{currency_symbol}KRW"
        df_exchange_rate = get_exchange_rate_data(currency_code, last_page_num)
        df_exchange_rate2 = df_exchange_rate[::-1].reset_index(drop=True).set_index('날짜')
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index, format='mixed')
        fig = px.line(
            df_exchange_rate2['매매기준율'],
            title="환율(매매기준율) 그래프",
            labels={"variable": "분류"}
        )
        fig.update_layout(
            yaxis_title=f"원화/{my_dropdown_value}",
            title_font_size=30,
            xaxis_title_font_size=20,
            yaxis_title_font_size=20
        )
        return fig

# if __name__ == '__main__':
#     app.run_server(debug=False, host='0.0.0.0', port=8888)
