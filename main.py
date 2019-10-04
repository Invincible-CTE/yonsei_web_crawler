import yonsei_calendar_crawler as ycc
import yonsei_crawler as yc
import yonsei_board as yb

"""만든 클래스, 메소드들 실험하는 모듈"""


board = yc.YonseiCrawler()
cal = ycc.YonseiCalendarCrawler()
bc = yb.YonseiBoardCrawler(limit=105)
