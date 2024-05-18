import dash # 멀티 파일로 실행 할 때 위 아래 줄 주석 해제
dash.register_page(
    __name__,
    title='구글 뉴스 기사를 검색하는 웹 앱',
    path='/s_search_app',
    description='구글 뉴스 기사를 검색하는 웹 앱',
    css_key='btn-primary'
)
# 단일 파일로 실행하지 않고, 멀티 파일로 저장할 경우 제일 하단 서버실행은 주석처리한다.
# %%writefile C:\myPyScraping\code\ch09\gnews_search_app.py
# 구글 뉴스에서 기사를 검색하는 웹 앱

from datetime import datetime, timedelta
import pandas as pd
import feedparser
# from IPython.display import HTML

# RSS 피드 제공 일시를 한국 날짜와 시간으로 변경하는 함수
def get_local_datetime(rss_datetime):    
    # 전체 값 중에서 날짜와 시간만 문자열로 추출 
    date_time_str = ' '.join(rss_datetime.split()[1:5])
    # 문자열의 각 자리에 의미를 부여해 datetime 객체로 변경 
    date_time_GMT = datetime.strptime(date_time_str, '%d %b %Y %H:%M:%S') 
    # GMT에 9시간을 더해 한국 시간대로 변경
    date_time_KST = date_time_GMT + timedelta(hours=9) 
    return date_time_KST # 변경된 시간대의 날짜와 시각 반환 
#---------------------------------------------------------

# 구글 뉴스 RSS 피드에서 검색 결과를 가져와 DataFrame 데이터로 반환하는 함수 
def get_gnews(query):
#     pd.reset_option('^display.', silent=True) # 판다스 출력 옵션 초기화
    # RSS 서비스 주소
    rss_url = f'https://news.google.com/rss/search?q={query}&&hl=ko&gl=KR&ceid=KR:ko' 
    rss_news = feedparser.parse(rss_url) # RSS 형식의 데이터를 파싱
    title = rss_news['feed']['title']
    updated = rss_news['feed']['updated']
    updated_KST = get_local_datetime(updated) # 한국 날짜와 시각으로 변경   
    df_gnews = pd.DataFrame(rss_news.entries) # 구글 뉴스 아이템을 판다스 DataFrame으로 변환
    # 위 rss_nes.entries 에서 타임스페이스 김일국 로 검색시 엔트리 값이 나오지 않는다.
    selected_columns = ['title', 'published', 'link'] # 관심있는 열만 선택
    df_gnews2 = df_gnews[selected_columns].copy()     # 선택한 열만 다른 DataFrame으로 복사
    # published 열의 작성 일시를 한국 시간대로 변경
    df_gnews2['published'] = df_gnews2['published'].apply(get_local_datetime)
    df_gnews2.columns = ['제목', '제공 일시', '링크'] # 열 이름 변경
    return title, updated_KST, df_gnews2
#---------------------------------------------------------

# 구글 뉴스 검색 결과를 Table로 정리한 HTML 코드를 반환하는 함수
def create_gnews_html_code(title, updated_KST, df):
    # DataFrame 데이터를 HTML 코드로 변환 (justify='center' 옵션을 이용해 열 제목을 중간에 배치)
    html_table = df.to_html(justify='center', escape=False, render_links=True) 
    # HTML 기본 구조를 갖는 HTML 코드
    html_code = '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>구글 뉴스 검색</title>
      </head>
      <body>
        <h1>{0}</h1>
        <h3> *검색 날짜 및 시각: {1}</h3>
        {2}
      </body>
    </html>    
    '''.format(title, updated_KST, html_table)
    return html_code
# -----------------------------------
# 구글 뉴스 검색 결과 가져오기
query = "인공지능%20머신러닝"
[title_gnews, updated_KST_gnews, df_gnews] = get_gnews(query)
# display(df_gnews.head()) # [Google](https://www.google.com)

# 링크 액션 작동하게 처리
df_gnews['링크']=df_gnews['링크'].map('[링크]({})'.format) #html.A(html.P('Link'),href="yahoo.com")
# 긴 제목 기사 줄여서 표시하기: 위 처럼 1줄로 되지 않아서 아래로 처리
for i in df_gnews.columns[0:1]:
    df_gnews[i] = df_gnews[i].str[:60]+'...'

print(df_gnews.head()) # ![Plotly](
# 웹 앱에 표시할 HTML 테이블 생성 (DataFrame 데이터 중 처음 일부만 HTML 테이블로 생성)
html_table = df_gnews.head().to_html(justify='center', escape=False, render_links=True)
# HTML 파일 다운로드를 위한 HTML code 생성
gnews_html_code = create_gnews_html_code(title_gnews, updated_KST_gnews, df_gnews)
# HTML(html_table)
# HTML(gnews_html_code)

# 대시보드 앱 시작(아래)
from dash import Dash, dcc, Input, Output, callback, callback_context, dash_table, State, html
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
from dash.dash_table.Format import Format, Group # , type:'numeric', format:Format(group=True, groups=[4])
from dash.exceptions import PreventUpdate

app = Dash('s_search_app',external_stylesheets=[dbc.themes.BOOTSTRAP]) # __name__ 사용하지 않는 대신에 하단에 @callback 처럼 사용
app.title = '구글 뉴스 기사를 검색하는 웹 앱'
layout = dbc.Container([ # 멀티 파일로 실행 할 때
# app.layout = dbc.Container([ # 단일 파일로 실행 할 때
    html.H2(children='구글 뉴스 기사를 검색하는 웹 앱'),
    html.Div([
        html.Span('검색어를 입력하세요!'),
    ], style={'display':'inline-block'}),
    dbc.Input(
        id="input_search",
        type='search',
        value='인공지능 머신러닝',
        placeholder="검색어를 입력하세요",
        style={'display':'inline-block',"width":"30%"}),
     html.Div([
        html.Span('', id='errors'),
    ], style={'display':'inline-block','color':'red'}),
    dbc.Button("검색", color="primary", className="me-1", id="btn_search",
               style={'display':'inline-block','width':'100px','vertical-align':'inherit'}),
    dash_table.DataTable(
        columns=[
#             {"name": i, "id": i} for i in df_gnews.columns],
        {'id': i, 'name': i, 'presentation': 'markdown'} if i == '링크' else {'id': i, 'name': i} for i in df_gnews.columns],
        id='tbl',
        data=df_gnews.to_dict("records"),
        style_header={'textAlign': 'center'},
        style_cell={'textAlign': 'left'},
    ),
    html.Div([
        dcc.Loading(id="loading-1", type="circle", children=html.Div(id="loading-output-1")),
    ],style={'position':'fixed','left':'50%','top':'50%','z-index':'9999'}),
])

@callback (
    [Output('tbl', 'data'),Output('errors', 'children'),Output("loading-output-1", "children")],
    [Input('input_search', 'value'), Input("btn_search", "n_clicks")],
    [State('tbl', 'data'), State('tbl', 'columns')], # 기존 값 가져오기
#     prevent_initial_call=True, # 페이지 로드 시 콜백이 실행되지 않도록 
)
def update_table(value, n_clicks, data, columns):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0] # 클릭,상태변경 이벤트 확인용 변수
    if 'input_search' in changed_id:
        raise PreventUpdate
    if 'btn_search' in changed_id:
        new_value = value.replace(" ", "%20" )
        print(new_value)
        try:
            value=''
            [title_gnews, updated_KST_gnews, df_gnews] = get_gnews(new_value)
            # 링크 액션 작동하게 처리
            df_gnews['링크']=df_gnews['링크'].map('[링크]({})'.format) #html.A(html.P('Link'),href="yahoo.com")
            # 긴 제목 기사 줄여서 표시하기: 위 처럼 1줄로 되지 않아서 아래로 처리
            for i in df_gnews.columns[0:1]:
                df_gnews[i] = df_gnews[i].str[:60]+'...'
            data=df_gnews.to_dict("records")
        except:
            value='검색결과를 파싱하지 못했습니다. 다른 검색어를 입력해 주세요.'
            data=data
        return data, value, ''

# if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
#     app.run_server(debug=False, host='0.0.0.0', port=8888) # 단일 파일로 실행 할 때
