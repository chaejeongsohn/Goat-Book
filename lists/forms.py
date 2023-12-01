from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "공백은 입력할 수 없습니다."


class ItemForm(forms.ModelForm):
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

    def clean_text(self):
        text = self.cleaned_data['text']
        if not text:
            raise forms.ValidationError("공백은 입력할 수 없습니다.")
        return text
