from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page

# 03. Unit tests(단위 테스트)
# Functional tests
# - 사용자 관점에서 테스트
# - 실제로 작동하는 애플리케이션을 구축하는 데 도움이 되며 실수로 애플리케이션이 중단되지 않도록 보장
# - 앱 동작의 모든 작은 세부 사항을 다루는 것이 아니라 모든 것이 올바르게 연결되어 있는지 확인하기 위한 것입니다.
# Unit tests
# - 코드 테스트, 즉 프로그래머의 관점
# - 깨끗하고 버그가 없는 코드를 작성하는 데 도움
# - 모든 하위 수준 세부 사항과 특수 사례를 철저하게 확인하기 위해 존재합니다.

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.startswith("<html>"))
        self.assertTrue(html.endswith("</html>"))

    def test_home_page_returns_correct_html_2(self):
        response = self.client.get("/")
        self.assertContains(response, "<title>To-Do lists</title>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")
