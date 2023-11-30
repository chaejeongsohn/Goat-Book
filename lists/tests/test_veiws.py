from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List



## / 루트 페이지: 새로운 목록 생성, 표시
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response,"home.html")  # 어떤 템플릿이 사용되는지 확인

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


## List item 등록 URL 추가
class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"item_text":"A new list item"})  # POST 실행
        self.assertEqual(Item.objects.count(), 1)  # Item 하나가 데이터베이스에 저장되었는지 확인
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new list item")  # 입력이 잘들어갔는지 확인
  
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text":"A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")  # POST 요청이후에 반환되는 뷰 확인


## List View 페이지: 기존 항목 표시, 목록에 새 항목 추가
class ListViewTest(TestCase):
    # List View 페이지 템플릿이 있는지 확인
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_to_template(self):
        other_list =List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"],correct_list)

    # List View 페이지에 모든 항목이 있는지 확인
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = "첫번째 아이템", list=correct_list)
        Item.objects.create(text = "두번째 아이템", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="다른 리스트 아이템", list=other_list)
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertContains(response, "첫번째 아이템")
        self.assertContains(response, "두번째 아이템")
        self.assertNotContains(response, "다른 리스트 아이템")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item", 
                         data={"item_text":"이미 존재하는 list에 새로운 Item 추가"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "이미 존재하는 list에 새로운 Item 추가")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/add_item",
                                    data={"item_text":"이미 존재하는 list에 새로운 Item 추가"})
        self.assertRedirects(response, f"/lists/{correct_list.id}/")