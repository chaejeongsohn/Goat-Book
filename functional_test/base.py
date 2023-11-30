import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

MAX_WAIT = 10


## static 파일을 자동으로 찾기 위해 test class 변경
class FunctionalTest(StaticLiveServerTestCase):
    
    # 테스트 시작 전
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' +  staging_server

    # 테스트 완료 후
    def tearDown(self):
        self.browser.quit()

    # 입력 행이 테이블에 로드 되도록 기다린다
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")  
                rows = table.find_elements(By.TAG_NAME, "tr")  
                self.assertIn(row_text, [row_text for row in rows])  
                return 
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:  
                    raise  
                time.sleep(0.5)


if __name__ == "__main__":
    unittest.main()


