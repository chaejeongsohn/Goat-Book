import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

import tracemalloc
tracemalloc.start()


class NewVisitorTest(unittest.TestCase):
    # 테스트 시작 전
    def setUp(self):
        self.browser = webdriver.Chrome()

    # 테스트 완료 후
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row_text for row in rows])

    def test_can_start_a_todo_list(self):
        # 홈페이지 방문
        self.browser.get("http://localhost:8000")

        # 페이지 title과 header 발견
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"),"Enter a to-do item")
        
        # 첫번째 입력
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # 명시적 대기(브라우저 로드 용도)
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # 두번째 입력
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)   
        time.sleep(1)  # 명시적 대기(브라우저 로드 용도)

        # 입력 테이블 확인
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")




if __name__ == "__main__":
    unittest.main()


