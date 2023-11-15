from django.test import LiveServerTestCase
import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):
    # 테스트 시작 전
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_can_start_a_todo_list(self):
        self.browser.get(self.live_server_url)

    # 테스트 완료 후
    def tearDown(self):
        self.browser.quit()

    # def check_for_row_in_list_table(self, row_text):
    #     table = self.browser.find_element(By.ID, "id_list_table")
    #     rows = table.find_elements(By.TAG_NAME, "tr")
    #     self.assertIn(row_text, [row_text for row in rows])

    ##########[암시적 및 명시적 대기 및 Voodoo time.sleeps에 대해]###########
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")  # 기존코드
                rows = table.find_elements(By.TAG_NAME, "tr")  # 기존코드
                self.assertIn(row_text, [row_text for row in rows])  # 기존코드
                return  # while 루프 탈출
            # AssertionError : 테이블이 있지만, 페이지가 다시 로드되기 전의 테이블인 경우
            # WebDriverException : 페이지가 로드안됨, selenium이 페이지에서 요소 못 찾은 경우
            except (AssertionError, WebDriverException):
                if time.time - start_time > MAX_WAIT:  # 시간 초과할때까지 코드를 시도할때마다 예외가 발생한다면
                    raise  # 테스트가 실패한 이유 추적
                time.sleep(0.5)

    def test_can_start_a_todo_list(self):
        # 홈페이지 방문
        self.browser.get("http://localhost:8000")

        # 페이지 title과 header 발견
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"),"Enter a to-do item")
        
        # 첫번째 입력
        inputbox.send_keys("공작 깃털 구매")
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)  # 명시적 대기(브라우저 로드 용도)
        self.wait_for_row_in_list_table("1: 공작 깃털 구매")

        # 두번째 입력
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("공작 깃털로 부채 만들기")
        inputbox.send_keys(Keys.ENTER)   
        # time.sleep(1)  # 명시적 대기(브라우저 로드 용도)

        # 입력 테이블 확인
        self.wait_for_row_in_list_table("1: 공작 깃털 구매")
        self.wait_for_row_in_list_table("2: 공작 깃털로 부채 만들기")




if __name__ == "__main__":
    unittest.main()


