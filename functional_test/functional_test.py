import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

import tracemalloc
tracemalloc.start()



# 02. unittest 모듈로 기능 테스트 확장
# unittest.TestCase 사용
# https://docs.python.org/3/library/unittest.html
class NewVisitorTest(unittest.TestCase):
    # 테스트 시작 전
    def setUp(self):
        self.browser = webdriver.Chrome()

    # 테스트 완료 후
    def tearDown(self):
        self.browser.quit()

    # test_ 로 시작되는 메소드 = test 메소드 라는 의미
    # 04. Test로 할 수 있는 것들
    # Selenium 사용
    # - find_element
    # - find_elements
    # - By.SOMETHING : HTML 속성을 사용하여 검색할 수 있도록 매개변수화함
    # - send_keys: input 요소에 입력함
    # - Keys : Enter와 같은 특수 키 보내기
    def test_can_start_a_todo_list(self):
        # 홈페이지 방문
        self.browser.get("http://localhost:8000")

        # 페이지 title과 header 발견
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"),"Enter a to-do item")

        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # 명시적 대기(브라우저 로드 용도)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        # self.assertTrue(any(row.text == "1.Buy peacock feathers" for row in rows),
        #                 f"table에 새로운 to-do item이 없습니다. 입력받은 내용:\n{table.text}",)
        # 같은 내용을 아래 self.assertIn 로 구현
        self.assertIn(
            "1: Buy peacock feathers",
            [row.text for row in rows]
        )
        self.assertIn(
            "2: Use peacock feathers to make a fly",
            [row.text for row in rows],
        )
        



if __name__ == "__main__":
    unittest.main()


