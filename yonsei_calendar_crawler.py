from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
import html_parser as hp


class YonseiCalendarCrawler:
    """연세 학사 일정 가져오는 클래스"""
    def __init__(self):
        """ 월 값들 가져오는 부분 """
        # 월 태그들을 일단 raw하게 넣음
        self.schedule_list = []
        target_url = r'https://www.yonsei.ac.kr/wj/support/calendar.jsp'
        html = urlopen(target_url)
        bs_object = BeautifulSoup(html, "html.parser")
        calendar = bs_object.body.find("table", {"class": "tblH ty2 jw_vertical"})
        month_names = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        current_year = date.today().year  # 현재 년도 가져옴
        month_list = calendar.find_all("span")

        # 월 값들을 str 타입으로 넣음 ex) 08 AUG
        for i in range(len(month_list)):
            month_list[i] = str(month_list[i]).split(">")[1][:6]

        """ 월별 일정 가져오는 부분"""
        desc = calendar.find_all("td", {"class": "des"})  # 내용 string data
        month = int(month_list[0][:2]) - 1  # start_month is first_month -1
        last_date = 32  # 마지막 날짜 값을 받아서

        schedule = list()  # [datetime.date: 내용] 형식의 리스트 타입 데이터
        # 날짜 데이터와 내용 데이터 뽑아내는 부분
        for i in range(0, len(desc), 2):
            date_info = str(desc[i]).replace("\t", "").replace("\r", "").replace("\n", "").split(" ")[1][12:]
            detail = str(desc[i + 1]).split(">")[2].split("<")[0]

            if "~" in date_info:
                if hp.tilde_txt_to_dates(date_info)[0] == -1:
                    start, mon, day = hp.tilde_txt_to_dates(date_info)[1:]
                    for k in range((date(current_year, month, start) - date(current_year, mon, day)).days + 1):
                        schedule.append([date(current_year, month, start) + timedelta(days=k), detail])
                elif hp.tilde_txt_to_dates(date_info)[0] == 0:
                    # 위에서 데이터 추가했으니 중복이 되므로 pass
                    pass
                else:
                    date_info = hp.tilde_txt_to_dates(date_info)  # a~b int list type

                    if date_info[0] < last_date:  # 다음 달로 넘어간 경우
                        month = month_names[month % 12]
                        current_year = current_year + 1 if month == 1 else current_year

                    # 리스트의 각 데이터들 하나씩 추가
                    for j in range(len(date_info)):
                        schedule.append([date(current_year, month, date_info[j]), detail.replace(u'\xa0', u' ')])
                        if j == len(date_info) - 1:
                            last_date = date_info[0]

            else:
                date_info = hp.small_bracket_to_int(date_info)
                if date_info < last_date:  # 다음 달로 넘어간 경우
                    month = month_names[month % 12]
                    current_year = current_year + 1 if month == 1 else current_year
                schedule.append([date(current_year, month, date_info), detail.replace(u'\xa0', u' ')])
                last_date = date_info

        self.schedule_list = schedule

    # 오늘의 일정 가져오기
    def get_today_schedule(self):
        sc = self.schedule_list
        rt = []
        for i in sc:
            if date.today() == i[0]:
                rt.append(i[1])

        return rt

    def get_all(self):
        return self.schedule_list

    def get_latest(self, cnt):
        try:
            return self.schedule_list[:cnt]
        except IndexError:
            return self.schedule_list
