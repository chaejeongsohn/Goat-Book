from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class LayoutAndStylingTest(FunctionalTest):
    
    def test_layout_and_styling(self):
        # Lisa가 홈페이지 방문
        self.browser.get(self.live_server_url)

        # Lisa의 브라우저 윈도우 크기 지정
        self.browser.set_window_size(1024, 768)

        # Lisa는 input박스가 가운데 정렬됨을 발견하고, 입력함
        inputbox = self.get_item_input_box()
        inputbox.send_keys("테스트")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 테스트")

        # Lisa는 새 목록의 페이지에서도 input박스가 가운데 정렬됨을 발견함
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(  # 연산의 오차범위를 10픽셀로 지정 > 반올림 오류, 스크롤바 등으로 인한 현상 처리 도움
            inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10, 
        )



