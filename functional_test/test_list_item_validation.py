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
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)

        # 홈페이지가 refresh되며, 빈 값을 리스트에 넣을수 없다는 오류 메세지가 뜸
        # 페이지가 새로고침 된다면, 페이지가 로드되길 기다리는 명시적 대기가 필요함
        # 사용자 에러메세지가 나오는게 아니라, CSS 가상선택자(pseudoselector)를 확인한다.
        self.wait_for(lambda: 
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # 아이템에 문자를 넣으니, 작동이 됨
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        
        # 두번째 빈 아이템을 submit하니 같은 오류 메세지가 뜸
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)
        self.wait_for(lambda: 
            self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid')
        )

        # # 다시 올바르게 아이템에 문자를 입력함
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Make tea')
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

