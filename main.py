from crawler import main_notice_crawler as yb, calendar_crawler as ycc, page_notice_crawler as yc

"""만든 클래스, 메소드들 실험하는 모듈"""


board = yc.PageNoticeCrawler()
cal = ycc.CalendarCrawler()
bc = yb.MainNoticeCrawler(limit=105)
