#-*- coding:utf-8 -*-
import urllib3
import json
import base64

# openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
openApiURL = "http://aiopen.etri.re.kr:8000/HumanParsing"
accessKey = "cc902c9e-dd9b-4afa-bf83-3ffc585f81a2"
imageFilePath = "assets/senior-3336451_640.jpg"
type = "jpg"
#위 입력예시) ---------
# https://pixabay.com/ko/photos/%EC%83%81%EC%9C%84-%EC%97%B0%EC%84%B8%EA%B0%80-%EB%93%9C%EC%8B%A0-%EC%82%AC%EB%9E%8C%EB%93%A4-3336451/
# imageFilePath = "./boardwalk.jpg"
# type = "jpg"
#-------------

file = open(imageFilePath, "rb")
imageContents = base64.b64encode(file.read()).decode("utf8")
file.close()

requestJson = {
    "argument": {
        "type": type,
        "file": imageContents
    }
}

http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8", "Authorization":accessKey},
    body=json.dumps(requestJson)
)

print("[responseCode] " + str(response.status))
print("[responBody]")
print(response.data) # print를 통해 결과가 json 형태로 나오는걸 보실수 있습니다.
#여기까지가 공통 샘플 소스이다. 이후 아래 소스는 API1, API2 기능별로 선택해서 사용-

# API1. 여기서부터는 샘플 소스 이후 사람속성 검출 API 시각화 소스
# 참고, 자바스크립트의 json과 파이썬의 딕셔너리는 같은 데이터 형이다.(아래)
data = json.loads(response.data) # string 형태의 json이라서 json.loads를 통해 읽어서 딕셔너리로 반환한다.
data_list = data.get("return_object") #딕셔너리에서 특정 값을 가져와서 딕셔너리로 반환한다.
print(data_list)
print('사진에 있는 사람의 수와 복장 특징 목록')

# 데이터프레임 사용에 필요한 판다스 모듈 임포트
import pandas as pd
#####################################################################
# dsah_table 모듈사용 시(아래) 
# 데이터 프레임 생성
df_person = pd.DataFrame(data_list) # 딕셔너리 데이터를 판다스 DataFrame으로 변환
df_person = df_person.transpose() # 딕셔너리 데이터의 행열 변환
# print(df_person.columns) # 컬럼출력
df_person = df_person[['hair color','coat color','pants color']]
df_person.columns = ['머리색상', '상의색상', '바지색상'] # 열 이름 변경
df_person = df_person.reset_index().rename(columns={'index':'사람객체명'}) # 인덱스 명 출력
print(df_person.head()) # 많은 데이터 중 상위 몇개만 표시
#######################################################################

#######################################################################
# 데이터프레임.to_html()을 사용하여 웹용으로 변경 사용 시(아래)
person_list = [] # 개체(json=dictionary) 배열변수 추가
for i in data_list: # 하나씩 가져다가 리스트로 출력하는 코드입니다.
    person_list.extend([{'person':i,'hair color':data_list.get(i).get('hair color'),'coat color':data_list.get(i).get('coat color'),'pants color':data_list.get(i).get('pants color')}])
    #print(i,' = hair color:',data_list.get(i).get('hair color'),' coat color:',data_list.get(i).get('coat color'),' pants color:',data_list.get(i).get('pants color'))
# print(person_list)
df_person_html = pd.DataFrame(person_list) # 딕셔너리 데이터를 판다스 DataFrame으로 변환
# print(df_person.columns)
df_person_html.columns = ['사람객체명', '머리색상', '상의색상', '바지색상'] # 열 이름 변경
print(df_person_html.head()) # 많은 데이터 중 상위 몇개만 표시