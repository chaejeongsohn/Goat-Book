from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError



class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "첫번째 아이템"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "두번째 아이템"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()  # Django 데이터베이스 쿼리
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "첫번째 아이템")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.text, "두번째 아이템")
        self.assertEqual(second_saved_item.list, mylist)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list = list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
