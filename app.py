# 멀티페이지 웹 앱 기술 참조: https://dash.plotly.com/urls
from dash import Dash, html, dcc, Input, Output, callback
import dash
import dash_bootstrap_components as dbc # 부트 스트랩 디자인 사용
import time

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.title = '파이썬 웹 스크래핑과 반응형 대시보드 앱 만들기'
app.layout = html.Div([
	html.H1('파이썬 웹 스크레핑과 반응형 대시보드 앱 만들기'),
    # html.Div(
    #     [
    #         html.Div(
    #             dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"]
    #             )
    #         )
    #         for page in dash.page_registry.values()
    #     ]
    # ),
    # 부트스트랩 버튼 클래스 이름 정보 https://getbootstrap.com/docs/4.0/components/buttons/
    # 플로틀리 dash.register_page 정보: https://github.com/plotly/dash-multi-page-app-plugin
    dbc.Nav(
        [
        dbc.NavLink(
            [
                html.Div(page["title"], className='ms-2 btn '+page["css_key"]),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
        ]
    ),
	dash.page_container,
    html.Div([
        dcc.Loading(id="loading-1", type="default", children=html.Div(id="loading-output")),
    ],style={'position':'fixed','left':'50%','top':'50%','width':'100%','height':'100%'}),
])

# 아래 콜백 함수에서 항상 Output 이 먼저 와야 한다.
@callback(
    Output('loading-output', 'children'),
    Input('loading-1', 'value'),
)
# update_output 는 콜백으로 자동실행된다.
def update_output(value):
    print('로딩중...')
    # time.sleep(1)
    return ''

if __name__ == '__main__': #파이썬 파일이 메인 프로그램으로 사용될 때와 모듈로 사용될 때를 구분하기 위한 용도
    app.run_server(debug=False, host='0.0.0.0', port=8888)
