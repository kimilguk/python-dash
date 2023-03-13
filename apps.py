# 멀티페이지 웹 앱 기술 참조: https://dash.plotly.com/urls
from dash import Dash, html, dcc, Input, Output, callback, State
import dash
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
import time
BS = "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.13.1/build/styles/tomorrow-night-eighties.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, BS], use_pages=True)
app.title = '파이썬 웹 스크래핑과 반응형 대시보드 앱 만들기'
app.layout = html.Div(children=[
    html.H1(html.A('파이썬 웹 스크레핑과 반응형 대시보드 앱 만들기', href="/",style={'color': 'blue', 'text-decoration': 'none'})),
    html.H2("원격URL로 가져오는 앱은 PythonAnywhere 클라우드에서 당분간 403 권한 없음 때문에 작동하지 않습니다."),
    # 부트스트랩 버튼 클래스 이름 정보 https://getbootstrap.com/docs/4.0/components/buttons/
    # 플로틀리 dash.register_page 정보: https://github.com/plotly/dash-multi-page-app-plugin
    dbc.Col(
        dbc.Button("포트폴리오 리스트", id="open-offcanvas", n_clicks=0),
        width=12,
        style={'textAlign': 'center'}
    ),
    dbc.Offcanvas(
        dbc.Nav(
            [
            dbc.NavLink(
                [
                    html.Div(page["title"], className='ms-2 btn '+page["css_key"]),
                ],
                href=page["path"],
            )
            for page in dash.page_registry.values()
            ]
        ),
        id="offcanvas",
        title="포트폴리오 리스트",
        is_open=False,
    ),
    dbc.Tabs(
    [
        dbc.Tab(dash.page_container, label="실행결과"),
        dbc.Tab([
            dcc.Location(id='url', refresh=False),
            html.Code(id='source_code', className='hljs')
        ], label="소스코드"),
    ]),
    html.Div([
        dcc.Loading(id="loading", type="default", children=html.Div(id="loading-output")),
    ],style={'position':'fixed','left':'50%','top':'50%','width':'100%','height':'100%'}),
])
# 현재 페이지의 파이썬 소스 확인
@app.callback(
    Output('source_code', 'children'),
    Input('url', 'pathname')
)
def display_source(pathname):
    for page in dash.page_registry.values():
        print(pathname)
        if pathname == page["path"]:
            if pathname == '/':
                pathname = '/dsah_app'
            with open(f'./pages{pathname}.py') as file_data:
                # 기본적으로 사용하는 함수를  with문 안에 사용하면 되며
                # with문을 나올 때 close를 자동으로 불러줍니다.
                source = file_data.read()
                source_code = html.Pre(source)
                return source_code # display_source() 함수 종료

# 포트폴리오 메뉴
@app.callback(
    [Output("offcanvas", "is_open"), Output("offcanvas", "placement")],
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open, 'end'
    return is_open, 'end'

# 아래 콜백 함수에서 항상 Output 이 먼저 와야 한다.
@callback(
    Output('loading-output', 'children'),
    Input('url', 'pathname'),
)
# update_output 는 콜백으로 자동실행된다.
def update_output(pathname):
    print('로딩중...')
    # time.sleep(1)
    return ''

if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
    app.run_server(debug=False, host='0.0.0.0', port=8888)
