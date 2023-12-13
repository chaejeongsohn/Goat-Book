from django.test import TestCase
from django.utils.html import escape
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm,
)
from unittest import skip

EMPTY_ITEM_ERROR = "공백은 입력할 수 없습니다."


## / 루트 페이지: 새로운 목록 생성, 표시
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response,"home.html")  # 어떤 템플릿이 사용되는지 확인

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    # 올바른 form 사용하고 있는지 확인
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


## List item 등록 URL 추가
class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/lists/new", data={"text":"A new list item"})  # POST 실행
        self.assertEqual(Item.objects.count(), 1)  # Item 하나가 데이터베이스에 저장되었는지 확인
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new list item")  # 입력이 잘들어갔는지 확인
  
    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"text":"A new list item"})
        new_list = List.objects.get()
        self.assertRedirects(response, f"/lists/{new_list.id}/")  # POST 요청이후에 반환되는 뷰 확인

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response= self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("공백은 입력할 수 없습니다.")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(Item.objects.count(), 0)

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/',
            data={'text':''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("공백은 입력할 수 없습니다.")
        self.assertContains(response, expected_error)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)


## List View 페이지: 기존 항목 표시, 목록에 새 항목 추가
class ListViewTest(TestCase):
    ## List View 페이지 템플릿이 있는지 확인
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_to_template(self):
        other_list =List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"],correct_list)

    ## List View 페이지에 모든 항목이 있는지 확인
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

    ## POST의 요청이 유효한 경우 테스트
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/", 
                         data={"text":"이미 존재하는 list에 새로운 Item 추가"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "이미 존재하는 list에 새로운 Item 추가")
        self.assertEqual(new_item.list, correct_list)

    ## POST의 요청이 유효한 경우 테스트
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/",
                                    data={"text":"이미 존재하는 list에 새로운 Item 추가"})
        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    ## POST의 요청이 유효하지 않은 경우 테스트
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    ## POST의 요청이 유효하지 않은 경우 테스트
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    ## get일때 form이 사용되는지 확인
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'],ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    ## form에 관해 오류가 있는지 확인하는 테스트
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text':''})

    ## form에 빈값을 넣어도 양식이 맞는지 테스트
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    ## form에 빈값을 넣으면 오류가 발생하는지 테스트
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    ## 아이템 중복 체크
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text':'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)