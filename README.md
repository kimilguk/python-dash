### 2026-08-30(일) 작업 : 파이썬 버전올리면서 작업한 내역(아래) 
#### koyeb 플랫폼에 배포하면서, 추가하고, 수정한 내용정리
- 파이썬 버전 지정파일 추가 : runtime.txt python-3.13.15 (이전에는 3.8.16였음.)
- 웹에서 소스코드 버튼을 사용할 때 'cp949' codec can't decode byte...에러 처리(아래)
- with open(f'{THIS_FOLDER}/pages{pathname}.py',encoding='cp949') //,encoding='UTF-8'에서 cp949로 변경
- 외부패키지 버전 지정파일 추가 : requirements.txt (아래 내용)

```
dash==2.15.0
yfinance==0.2.38
dash_bootstrap_components==1.5.0
feedparser==6.0.11
matplotlib>=3.3.2
IPython==7.19.0
```

- 파이썬 버전이 올라가면서 아래 내용 2가지 수정됨.
- exchange_rate_app.py(환율 데이터를 가져오는 웹 앱)
- land_info_app.py(부동산 정보를 가져오는 웹 앱)
- 위 2개의 파일에서 df.dtypes를 object에서 datetime형식으로 바꾸는 함수의 날짜 format 을 지정하는 방식 변경됨(아래 2개)

```
# exchange_rate_app.py(환율 데이터를 가져오는 웹 앱)
# koyeb에서 에러나서 format변경
# df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index,format='%Y-%m-%d')
df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index,,format='mixed')
# infer_datetime_format 함수가 deprecated 되어서 더이상 사용되지 않을 예정이라서 format속성으로 대체한다.(아래)
df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index,format='mixed')
- 위 처리 관련정보 : https://pandas.pydata.org/pdeps/0004-consistent-to-datetime-parsing.html
```

```
# land_info_app.py(부동산 정보를 가져오는 웹 앱)
# koyeb에서 에러나서 format변경
# df_rates_for_chart.index = pd.to_datetime(df_rates_for_chart.index,format='%Y-%m')
df_rates_for_chart.index = pd.to_datetime(df_rates_for_chart.index,format='mixed')

```
- koyeb 배포에서는 노트북 폴더 내용은 지우고, 앱 내묭만 배포한다.

### 구름ide용으로 pages폴더내의 ~_app.py파일의 name 대신 사용한 부분 변경(아래)
- app = Dash('name',...) 부분을 app = Dash('파일명',...)으로

### 파이썬 웹 스크레핑과 반응형 대시보드 앱 만들기
#### 2023-03-15(수) 작업 : 파이썬 스케줄로 카카오 톡 메세지 보내기
#### 2023-03-14(화) 작업 : 파이썬 코드로 카카오 톡 메세지 보내기
#### 2023-03-13(월) 작업 : 클라우드 서버에 배포 app.py 을 apps.py 으로 변경
#### 클라우드 배포용으로 웹에서 사용하진 않기 때문에 설치하지 않고 pages 내용도 변경 matplotlib, iPython 부분 주석처리함
#### 2023-03-12(일) 작업 : 포트폴리오 리스트 메뉴 제작
#### 2023-03-08(수) 작업 : 대시보드 메인페이지 구성 및 로딩 이미지 추가
#### 2023-03-07(화) 작업 : 1번 인터렉트브 액션으로 멀티 html 객체 업데이트 및 멀티파일로 여러 앱 메뉴로 불러오기 처리
#### 2023-03-06(월) 작업 : 매트랩(고정)과 플로틀리(인터렉티브) 차이 확인 및 매트랩 그래프에서 한글 사용 추가 처리
#### 2023-03-05(일) 작업 : 주식 정보를 가져오는 웹 앱에서 엑셀 다운로드 버튼 추가 및 Dash용 부트스트랩 디자인 적용
#### 2023-03-04(토) 작업 : 주식 정보를 가져오는 웹 앱
#### 2023-03-03(금) 작업 : 대시보드 인터렉티브 콜백 기능 처리
#### 2023-03-02(목) 작업 : dash_table 모듈 작업 클릭 했을 때 선택한 데이터 변화 처리OK
#### 2023-03-01(수) 작업 : dcc(dash_core_components) 모듈 작업
#### 2023-02-28(화) 작업 : 대시보드 작업 시작
#### 2023-02-27(월) 작업 : 스크래핑한 내용 html로 저장 및 디자인 후 출력
#### 2023-02-26(일) 작업 : RSS 작업
#### 2023-02-25(토) 작업 : 최초 커밋

```
┌───────────────────────────────────────────────┐
                                       _       
     __ _  ___   ___  _ __ _ __ ___   (_) ___  
    / _` |/ _ \ / _ \| '__| '_ ` _ \  | |/ _ \ 
   | (_| | (_) | (_) | |  | | | | | |_| | (_) |
    \__, |\___/ \___/|_|  |_| |_| |_(_)_|\___/ 
    |___/                                      
			     🌩 𝘼𝙣𝙮𝙤𝙣𝙚 𝙘𝙖𝙣 𝙙𝙚𝙫𝙚𝙡𝙤𝙥!
└───────────────────────────────────────────────┘
```

# goormIDE
Welcome to goormIDE!

goormIDE is a powerful cloud IDE service to maximize productivity for developers and teams.  
**DEVELOP WITH EXCELLENCE**  

`Happy coding! The goormIDE team`


## 🔧 Tip & Guide

* Command feature
	* You can simply run your script using the shortcut icons on the top right.
	* Check out `PROJECT > Common/Build/Run/Test/Find Command` in the top menu.
	
* Get URL and Port
	* Click `PROJECT > URL/PORT` in top menu bar.
	* You can get default URL/Port and add URL/Port in the top menu.

* Useful shortcut
	
| Shortcuts name     | Command (Mac) | Command (Window) |
| ------------------ | :-----------: | :--------------: |
| Copy in Terminal   | ⌘ + C         | Ctrl + Shift + C |
| Paste in Terminal  | ⌘ + V         | Ctrl + Shift + V |
| Search File        | ⌥ + ⇧ + F     | Alt + Shift + F  |
| Terminal Toggle    | ⌥ + ⇧ + B     | Alt + Shift + B  |
| New Terminal       | ⌥ + ⇧ + T     | Alt + Shift + T  |
| Code Formatting    | ⌥ + ⇧ + P     | Alt + Shift + P  |
| Show All Shortcuts | ⌘ + H         | Ctrl + H         |

## 💬 Support & Documentation

Visit [https://ide.goorm.io](https://ide.goorm.io) to support and learn more about using goormIDE.  
To watch some usage guides, visit [https://help.goorm.io/en/goormide](https://help.goorm.io/en/goormide)
