from urllib.request import urlopen
from bs4 import BeautifulSoup
import html_parser as hp


class YonseiBoardCrawler:
    """연세 공지사항 가져오는 클래스"""
    def __init__(self, limit):
        self.art_list = []  # 공지사항 리스트
        self.offset = 0  # 공지사항이 몇 번째 아이템인지

        self.limit = 10000 if limit == 0 else limit   # 너무 많아서 끊을거면 여기만 수정하면 됨
        base_url = r'https://www.yonsei.ac.kr/wj/support/notice.jsp'  # 목표 주소
        list_url = r'?mode=list&board_no=15&pager.offset='  # 리스트가 포함되어 있는 주소
        _step = 10  # 한 페이지에 몇 개씩 늘어나는지

        while True:
            try:
                html = urlopen(base_url + list_url + str(self.offset))
                bs_object = BeautifulSoup(html, "html.parser")
                page_arts = []
                page_arts = page_arts + bs_object.body.find("ul", {"class": "board_list"}).find_all("li")
                if len(page_arts) == 4 or self.offset > limit:
                    raise IndexError  # 마지막 페이지 처리
                for item in range(len(page_arts)):
                    tmp = []
                    if bool(page_arts[0].get("class")):     # 공지사항 부분
                        if self.offset < 10:                # 처음에만 추가
                            tmp = [
                                hp.reduce_spaces(page_arts[0].a.strong.get_text()),  # content
                                base_url + page_arts[0].a.get("href"),  # url
                                hp.reduce_spaces(page_arts[0].a.span.get_text())[3:-10],  # author
                                hp.dot_date_to_datetime(hp.reduce_spaces(page_arts[0].a.span.get_text())[-10:]),  # date
                                False
                            ]
                            page_arts.append(tmp)
                        else:
                            pass
                        page_arts.pop(0)
                    else:  # 일반 글 부분
                        if "만료" in hp.reduce_spaces(page_arts[0].a.strong.get_text()):  # 중에 만료된 거
                            tmp = [
                                hp.reduce_spaces(page_arts[0].a.strong).split("<")[1].replace("strong>", "").lstrip(),
                                # content
                                base_url + page_arts[0].a.get("href"),  # url
                                hp.reduce_spaces(page_arts[0].a.find_all("span")[1].get_text())[:-10],  # author
                                hp.dot_date_to_datetime(
                                    hp.reduce_spaces(page_arts[0].a.find_all("span")[1].get_text())[-10:]),  # date
                                True
                            ]
                        else:
                            tmp = [
                                hp.reduce_spaces(page_arts[0].a.strong.get_text()),  # content
                                base_url + page_arts[0].a.get("href"),  # url
                                hp.reduce_spaces(page_arts[0].a.span.get_text())[3:-10],  # author
                                hp.dot_date_to_datetime(hp.reduce_spaces(page_arts[0].a.span.get_text())[-10:]),  # date
                                False
                            ]
                    # print(tmp)
                        page_arts.append(tmp)
                        page_arts.pop(0)
            except IndexError:
                break
            # except KeyError:
            #     pass
            self.art_list += page_arts
            self.offset += _step

    def get_all(self):
        return self.art_list[:self.limit]

    def get_latest(self, cnt=100):
        if cnt < self.limit:
            return self.art_list[:cnt]
        else:
            return self.art_list[:self.limit]
