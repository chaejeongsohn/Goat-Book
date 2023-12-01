from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .forms import ItemForm



# Create your views here.
def home_page(request):
    return render(request, "home.html", {'form': ItemForm()})


def new_list(request):
    newList = List.objects.create()
    item_text = request.POST.get("item_text", "").strip()

    if not item_text:
        error_msg = "공백은 입력할 수 없습니다."
        return render(request, "list.html", {'list': newList, 'error_msg': error_msg})

    Item.objects.create(text = item_text, list=newList)
    return redirect(newList)


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    error_msg = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=our_list)
            item.full_clean()
            item.save()
            return redirect(our_list)
        except ValidationError:
            error_msg = "공백은 입력할 수 없습니다."
    return render(request, "list.html", {"list": our_list, 'error_msg': error_msg})