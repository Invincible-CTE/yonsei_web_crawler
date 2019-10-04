from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np


class YonseiCrawler:
    """연세대학교 페이지들의 공지사항을 크롤링 하는 클래스
    url 설정을 안 하면 컴정 홈페이지의 공지사항을 크롤링함"""

    def __init__(self, url=r'http://it.yonsei.ac.kr/index.php?mid=board_notice&page='):
        """http://swuniv.yonsei.ac.kr/index.php?mid=board_notice&page="""

        self.art_list = []      # 공지사항 리스트
        self.target_url = url   # 목표 주소
        page = 1  # 공지사항이 몇 페이지인지
        while True:     # 공지사항 page가 없을 때까지 체크
            target_url = self.target_url + str(page)
            html = urlopen(target_url)
            bs_object = BeautifulSoup(html, "html.parser")
            page_arts = []
            try:
                page_arts = page_arts + bs_object.body.find("table",
                                                            {"class": "bd_lst bd_tb_lst bd_tb"}).find_all("tr")
            except AttributeError:
                break
            page_arts.pop(0)

            # art_list의 데이터를 하나씩 가져와서 리스트로 묶어서 다시 넣고 원본 데이터는 삭제
            for i in range(len(page_arts)):
                page_arts.append([int(tr_to_txt(page_arts[0].find("td", {"class": "no"}))),
                                  tr_to_txt(page_arts[0].find("td", {"class": "title"})),
                                  target_url + page_arts[0].find("td", {"class": "title"}).find("a").get("href"),
                                  tr_to_txt(page_arts[0].find("td", {"class": "author"})),
                                  tr_to_txt(page_arts[0].find("td", {"class": "time"})),
                                  int(tr_to_txt(page_arts[0].find("td", {"class": "m_no"})))])
                page_arts.pop(0)

            page += 1
            self.art_list += page_arts

    def get_all(self):
        """모든 공지사항을 [index, title, url, author, time, m_no] 순의
        리스트의 데이터로 가져오는 메소드"""
        return self.art_list

    def get_latest(self, cnt=5):
        """최신 cnt개의 공지사항을 [index, title, url, author, time, m_no] 순의
        리스트의 데이터로 가져오는 메소드"""
        return self.art_list[:cnt]

    def get_latest_attr(self, attr, cnt=5):
        """최신 cnt개의 공지사항의 특정 애트리뷰트들만 가져오는메소드
        attr 종류는 index(0), title(1), url(2), author(3), time(4), m_no(5)"""
        tmp_arr = np.ndarray(self.art_list)
        return_value = ""

        if type(attr) == str:
            if attr == 'index':
                return_value = tmp_arr[:5, 0]
            elif attr == 'title':
                return_value = tmp_arr[:5, 1]
            elif attr == 'url':
                return_value = tmp_arr[:5, 2]
            elif attr == 'author':
                return_value = tmp_arr[:5, 3]
            elif attr == 'time':
                return_value = tmp_arr[:5, 4]
            elif attr == 'm_no':
                return_value = tmp_arr[:5, 5]
            else:
                raise IndexError
        elif type(attr) == int:
            if attr > 5:
                raise IndexError
            return_value = tmp_arr[:5, attr]
        else:
            raise AttributeError

        return list(return_value)


def tr_to_txt(tr_str):
    """description
    tr태그의 정보만을 추출하여 str 타입의 데이터를 리턴하는 함수"""
    return str(tr_str.text).replace("\t", "").replace("\r", "").replace("\n", "")
