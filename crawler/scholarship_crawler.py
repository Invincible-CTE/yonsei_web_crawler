from urllib.request import urlopen
from bs4 import BeautifulSoup
import html_parser as hp


class ScholarshipCrawler:

    def __init__(self, limit=300):
        self.art_list = []  # 공지사항 리스트
        self.offset = 0  # 공지사항이 몇 번째 아이템인지
        self.limit = 10000 if limit == 0 else limit # 대략 1년에 150개

        base_url = r'https://wsw.yonsei.ac.kr/wsw/notice/scholarship-board.do'  # 목표 주소
        list_url = r'?mode=list&&articleLimit=10&article.offset='  # 리스트가 포함되어 있는 주소
        _step = 10  # 한 페이지에 몇 개씩 늘어나는지

        while True:
            try:
                html = urlopen(base_url + list_url + str(self.offset))
                bs_object = BeautifulSoup(html, "html.parser")
                page_arts = []
                page_arts = page_arts + bs_object.body.find("table", {"class": "board-table"}).tbody.find_all('tr')

                if len(page_arts) <= 10 or self.offset > self.limit:
                    raise IndexError  # 마지막 페이지 처리
                for i in range(len(page_arts)):
                    title_str = hp.reduce_spaces(page_arts[0].find_all('td')[1].get_text())
                    tmp = []
                    if hp.reduce_spaces(page_arts[0].find_all('td')[0].get_text()).rstrip() == '공지':
                        if self.offset < 10:
                            tmp = [True,  # 공지
                                   title_str.split("]")[0].lstrip()[1:].split("학생복지처")[
                                       0].rstrip() if '[' in title_str else "기타",  # 종류
                                   title_str.split("]")[1].lstrip().split("학생복지처")[0].rstrip() if '[' in title_str else
                                   title_str.split("학생복지처")[0].rstrip(),  # title
                                   True if hp.reduce_spaces(page_arts[0].find_all('td')[0].get_text()) == '첨부파일' else False,
                                   # 첨부파일
                                   hp.reduce_spaces(page_arts[0].find_all('td')[3].get_text()),  # 글쓴이
                                   hp.dot_date_to_datetime(
                                       "20" + hp.reduce_spaces(page_arts[0].find_all('td')[4].get_text()))]  # 날짜
                            page_arts.append(tmp)
                        else:
                            pass
                        page_arts.pop(0)
                    else:  # 일반글
                        tmp = [False,  # 공지
                               title_str.split("]")[0].lstrip()[1:].split("학생복지처")[0].rstrip() if '[' in title_str else "기타",
                               # 종류
                               title_str.split("]")[1].lstrip().split("학생복지처")[0].rstrip() if '[' in title_str else
                               title_str.split("학생복지처")[0].rstrip(),  # title
                               True if hp.reduce_spaces(page_arts[0].find_all('td')[0].get_text()) == '첨부파일' else False,  # 첨부파일
                               hp.reduce_spaces(page_arts[0].find_all('td')[3].get_text()),  # 글쓴이
                               hp.dot_date_to_datetime(
                                   "20" + hp.reduce_spaces(page_arts[0].find_all('td')[4].get_text()))]  # 날짜
                        page_arts.append(tmp)
                        page_arts.pop(0)
            except IndexError:
                break
            self.art_list += page_arts
            self.offset += _step

    def get_all(self):
        return self.art_list[:self.limit]

    def get_latest(self, cnt=100):
        if cnt < self.limit:
            return self.art_list[:cnt]
        else:
            return self.art_list[:self.limit]

