from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unittest import skip



class ItemValidationTest(FunctionalTest):

    # def get_error_element(self):
    #     return self.browser.find_element_by_css_selector('.has-error')

    # @skip
    def test_cannot_add_empty_list_items(self):
        # 빈 리스트, 빈 inbut을 submit함
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys(Keys.ENTER)

        # 홈페이지가 refresh되며, 빈 값을 리스트에 넣을수 없다는 오류 메세지가 뜸
        # 페이지가 새로고침 된다면, 페이지가 로드되길 기다리는 명시적 대기가 필요함
        self.wait_for(lambda: 
            self.browser.find_element(By.CLASS_NAME, 'has-error')
        )
        error_msg = self.browser.find_element(By.CLASS_NAME, 'has-error').text
        self.assertEqual(error_msg, "공백은 입력할 수 없습니다.")

        # 아이템에 문자를 넣으니, 작동이 됨
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        
        # 두번째 빈 아이템을 submit하니 같은 오류 메세지가 뜸
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CLASS_NAME, 'has-error').text,
            "공백은 입력할 수 없습니다."
        ))

        # # 다시 올바르게 아이템에 문자를 입력함
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Make tea')
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

