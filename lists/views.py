from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == "POST":
        item = Item()
        item.text = request.POST.get("item_text", "")
        item.save()
        return redirect("/")

    return render(
        request,
        "home.html",
        # POST.get: Post가 없을때, 일반적인 Get요청의 기본값
        {"new_item_text":request.POST.get("item_text","")},  
        )