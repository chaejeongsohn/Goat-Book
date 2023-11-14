import unittest
from selenium import webdriver


# unittest.TestCase 사용
# https://docs.python.org/3/library/unittest.html
class NewVisitorTest(unittest.TestCase):
    # 테스트 시작 전
    def setUp(self):
        self.browser = webdriver.Firefox()

    # 테스트 완료 후
    def tearDown(self):
        self.browser.quit()

    # test_ 로 시작되는 메소드 = test 메소드 라는 의미
    def test_can_start_a_todo_list(self):
        self.browser.get("http://localhost:8000")

        self.assertIn("To-Do", self.browser.title) 

        self.fail("Finish the test!")



if __name__ == "__main__":
    unittest.main()


