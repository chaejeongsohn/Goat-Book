from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item


EMPTY_ITEM_ERROR = "공백은 입력할 수 없습니다."
DUPLICATE_ITEM_ERROR = "동일한 항목이 이미 있습니다."


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.TextInput(attrs={
            'placeholder': 'Enter a to-do item',
            'class':'form-control form-control-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError("공백은 입력할 수 없습니다.")
        return text
    

class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)



    def save(self):
        return forms.models.ModelForm.save(self)


