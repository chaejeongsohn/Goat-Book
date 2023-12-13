from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ExistingListItemForm, ItemForm
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .forms import ItemForm



# Create your views here.
def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


# def new_list(request):
#     newList = List.objects.create()
#     text = request.POST.get("text", "").strip()

#     if not text:
#         error_msg = "공백은 입력할 수 없습니다."
#         return render(request, "list.html", {'list': newList, 'error_msg': error_msg})
    
#     Item.objects.create(text = text, list=newList)
#     return redirect(newList)


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        newList = List.objects.create()
        form.save(for_list=newList)
        return redirect(newList)
    else:
        return render(request, "home.html", {"form": form})
    

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(request, "list.html", {"list": our_list, "form": form})