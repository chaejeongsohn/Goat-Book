from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest import skip



class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # 빈 리스트, 빈 inbut을 submit함
        # 홈페이지가 refresh되며, 빈 값을 리스트에 넣을수 없다는 오류 메세지가 뜸
        # 아이템에 문자를 넣으니, 작동이 됨
        # 두번째 빈 아이템을 submit하니 같은 오류 메세지가 뜸
        self.fail('write me!')

