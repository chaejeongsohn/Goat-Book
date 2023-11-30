from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class NewVisitorTest(FunctionalTest):

    def test_can_start_a_todo_list(self):
        # Lisa가 홈페이지 방문
        self.browser.get(self.live_server_url)

        # Lisa가 페이지 title과 header 발견
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"),"Enter a to-do item")
        
        # Lisa가 첫번째 입력
        inputbox.send_keys("공작 깃털 구매")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 공작 깃털 구매")

        # Lisa가 두번째 입력
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("공작 깃털로 부채 만들기")
        inputbox.send_keys(Keys.ENTER)   

        # Lisa가 입력 테이블 확인
        self.wait_for_row_in_list_table("1: 공작 깃털 구매")
        self.wait_for_row_in_list_table("2: 공작 깃털로 부채 만들기")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 첫번째 유저 Lisa가 방문하고, 허나 입력함 
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("공작 깃털 구매")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 공작 깃털 구매")

        # Lisa의 URL 
        lisa_list_url = self.browser.current_url
        self.assertRegex(lisa_list_url, "/lists/.+")  # assertRegex: string이 정규식과 일치하는지 확인하는 도우미 함수(unittest에서 추가됨)

        ## 브라우저의 쿠키 삭제
        ## 새 유저가 방문한 경우, 시뮬레이션
        self.browser.delete_all_cookies()

        # 새로운 유저 Francis가 방문한 경우, Lisa가 작성한 항목은 없어야 함
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("공작 깃털 구매", page_text)
        self.assertNotIn("부채 만들기", page_text)

        # Francis가 첫번째 입력
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("우유 구매")
        inputbox.send_keys(Keys.ENTER) 
        self.wait_for_row_in_list_table("1: 우유 구매")

        # Francis가 새로운 URL 받음
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, lisa_list_url)  # 고유한 url부여 받았는지 확인

        # Lisa의 흔적이 없는지 한번 더 확인
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("공작 깃털 구매", page_text)
        self.assertIn("우유 구매", page_text)

