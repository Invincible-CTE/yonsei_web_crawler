from datetime import date

"""web crawling 하면서 필요한 메소드 만든 모듈"""


def dot_date_to_datetime(dot_date):
    """2019.10.04 처럼 .으로 구분된 날짜를 datetime.date로 변환함"""
    _year, _mon, _day = map(int, dot_date.strip().split("."))
    return date(_year, _mon, _day)


def reduce_spaces(_input):
    """\r, \t, \n 를 제거 하고 &amp를 &로 바꿈"""
    _input = str(_input)
    if '[공지]' in _input:
        _input = _input.replace('[공지]', '')
    return _input.replace('\r', '').replace('\n', '').replace('\t', '').replace('&amp;', '&').lstrip()


# "1(목)~7(수)" -> [1,2,3,4,5,6,7]
def tilde_txt_to_dates(txt_date):
    start, end = txt_date.split("~")

    if '.' not in start and '.' not in end:
        start = small_bracket_to_int(start)
        end = small_bracket_to_int(end)
        return [x for x in range(start, end + 1)]
    elif '.' in start:
        # ex) 10.29(화)~1(금)
        mon, day = start.split(".")
        mon = small_bracket_to_int(mon)
        day = small_bracket_to_int(day)
        end = small_bracket_to_int(end)
        return [0, mon, day, end]
    else:  # case of '.' in end
        # ex) 29(화)~11.01(금)
        mon, day = end.split(".")
        mon = small_bracket_to_int(mon)
        day = small_bracket_to_int(day)
        start = small_bracket_to_int(start)
        return [-1, start, mon, day]


# "15(목)" -> 15
def small_bracket_to_int(txt_date):
    return int(txt_date.split("(")[0])


# "15(목)" -> 3 (weekday)
def txt_to_date(date_text):
    """1(목)같은 스트링 데이터가 들어오면 3 리턴
    월:0, 화:1, 수:2, 목:3, 금:4, 토:5, 일:6
    다른 경우에는 ValueError"""
    if "월" in date_text:
        return 0
    elif "화" in date_text:
        return 1
    elif "수" in date_text:
        return 2
    elif "목" in date_text:
        return 3
    elif "금" in date_text:
        return 4
    elif "토" in date_text:
        return 5
    elif "일" in date_text:
        return 6
    else:  # case of error
        raise ValueError


def tr_to_txt(tr_str):
    """description
    tr태그의 정보만을 추출하여 str 타입의 데이터를 리턴하는 함수"""
    return str(tr_str.text).replace("\t", "").replace("\r", "").replace("\n", "")
