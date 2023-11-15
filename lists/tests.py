from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response,"home.html")  # 어떤 템플릿이 사용되는지 확인

    ########[GET 구현: 기존 항목을 템플릿에 전달]############
    def test_displays_all_list_items(self):
        Item.objects.create(text = "itemdy 1")
        Item.objects.create(text = "itemdy 2")
        response = self.client.get("/")
        self.assertContains(response, "itemdy 1")
        self.assertContains(response, "itemdy 2")

    def test_can_save_a_POST_request(self):
        self.client.post("/", data={"item_text":"A new list item"})  # POST 실행

        self.assertEqual(Item.objects.count(), 1)  # Item 하나가 데이터베이스에 저장되었는지 확인
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")  # 입력이 잘들어갔는지 확인

        ########[Code smell: POST 테스트가 너무 길어요]############
        # self.assertContains(response, "A new list item")  
        # self.assertTemplateUsed(response, "home.html")  # 어떤 템플릿이 사용되는지 확인

        # self.assertRedirects(response, "/")

    # unit test는 한 가지만 테스트 해야한다.   
    def test_redirects_after_POST(self):
        response = self.client.post("/", data={"item_text":"A new list item"})
        self.assertRedirects(response, "/")  # POST 요청이후에 반환되는 뷰 확인

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "첫번째 아이템"
        first_item.save()

        second_item = Item()
        second_item.text = "두번째 아이템"
        second_item.save()

        saved_items = Item.objects.all()  # Django 데이터베이스 쿼리
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "첫번째 아이템")
        self.assertEqual(second_saved_item.text, "두번째 아이템")