#상대경로-아래는 절대경로
#%%writefile /workspace/python-dash/notebooks/calc_area2.py
#%%writefile C:\myPyScraping\code\ch03\calc_area.py 윈도우 경로
# File name: calc_area.py
PI = 3.14
def rectangle(l, w): # 직사각형(가로: l, 세로: w)의 넓이를 반환
    return l * w

def circle(r): # 원(반지름: r)의 넓이를 반환
    return PI * r ** 2
