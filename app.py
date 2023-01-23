import re
from collections import Counter
from bs4 import BeautifulSoup
import urllib.request as req
import streamlit as st

st.title("BREAKOUT SON 금칙어 검사")


# 블로그 에디터 창에서 안보이지만 따라오는 단어들
remove_list = ['대표사진 삭제', '사진 설명을 입력하세요.', '출처 입력', '사진 삭제','이미지 썸네일 삭제',\
               '동영상 정보 상세 보기','동영상 설명을 입력하세요.']
ban_list = ['야하', '야합', '야해', '야한', '고자', '게이', '자살', '어도', '세요', '매장', '일수',\
            '총','개','년','시간','음부','보지','자지','참','면','이해','살인','죽음','강간',\
            '다음', '포', '창', '탄','필', '하시', '교수', '교사','나가요','구타','폭행','애자'\
            '술', '면수', '가장', '식인','자인', '교통','장면','고살','도적','도둑','강도',\
            '포커', '자자', '브라', '씹', '에로', '로비', '도할','일수','최고','최저', '100%',\
            '고검', '담배','조폭', '중독', '폭력', '염장', '이반', '장도','판매','효과','치료',\
            '해도','도사', '완전', '성인', '특별', '정사','거지','의사','무료','추천','보장',\
            '상담','가입', '네이버', '최저', '엄청', '1등','최고', '아다','노출','성교','시다',\
            '기가', '가오', '가조', '어보', '에다', '까다', '다니', '빠','섹스','칼',\
            '사장', '서울','서제', '요사', '요서', '이기', '이나', '이부','할인','고가',\
            '이슬', '인지', '장님', '장해', '중요', '지지','쪽','하지','저가','체험','A+',\
            '한사', '도자', '진몰','신경', '가보', '가이', '매주', '서적','분들',\
            '기장', '이감', '창이', '해주', '포토', '가기', '가동', '간이','니거']

# 줄바꿈 있는 본문을 한번에 입력하기
# str = pyautogui.prompt()     # 파이참에서 쓸때
user_input = st.text_input('본문 또는 URL 입력') # 스트림릿에서 쓸때

if 'blog.naver.com' in user_input:
    url = user_input

    if not 'm.blog.naver.com' in url:
        url = url.replace('blog.naver.com', 'm.blog.naver.com')

    code = req.urlopen(url)
    soup = BeautifulSoup(code, 'html.parser')

    title = soup.select_one('#SE-b28e8031-860b-4891-9f6b-228ccf1c844f')
    str = soup.select_one('div.se-main-container')
    str = str.text

else:
    str = user_input


if str != '':
    
    # 따라온 단어들 삭제
    for i in remove_list:
        str = str.replace(i, '')
    
    # 공백과 줄바꿈 삭제
    str_re = re.sub('\n| ', '', str)
    str_without_line = str.replace('\n','').strip() #줄바꿈만 정리한 것
    
    print (str_re)
    print ('============= 글자 수 =================')
    print ('공백제외:', len(str_re), '|', '공백포함:', len(str),'자 입니다\n')
    
    # 금칙어 찾기
    user_ban_list = []
    for i in ban_list:
        user_ban = re.findall(i, str_re)
        user_ban_list += user_ban
    ban_cnt = dict(Counter(user_ban_list))
    
    # 금칙어 사용 횟수 카운팅
    print ('============ 금칙어 리스트 =================================')
    num = 0
    for k, v in ban_cnt.items():
        print (k, ':', v,'회', ',', end=' ')
        num += 1
        if num % 6 == 0 :
            print ('')
    
    st.write('#### 공백 제외', len(str_re),'자, 공백 포함', len(str),'자 입니다')
    st.info(str_re)
    st.write('### 금칙어 사용 현황')
    st.write(ban_cnt)
    st.write('Tip. 금칙어는 뷰탭 누락의 원인입니다.
             이게 왜.. 라고 생각드시겠지만 불가피한 경우를 제외하고 최대한 줄여보세요')
