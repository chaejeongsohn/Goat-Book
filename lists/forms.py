from django import forms

class ItemForm(forms.Form):
    item_text = forms.CharField(label='Item Text', max_length=255, strip=True)

    def clean_item_text(self):
        item_text = self.cleaned_data['item_text']
        # Your custom validation logic if needed
        if not item_text:
            raise forms.ValidationError("공백은 입력할 수 없습니다.")
        return item_text
