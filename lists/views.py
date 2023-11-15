from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == "POST":
        # item = Item()
        # item.text = request.POST.get("item_text", "")
        # item.save()
        # Django 의 .objects.create() 를 사용해서 한 줄로 객체 생성

        Item.objects.create(text = request.POST["item_text"])
        return redirect("/")

    ########[GET 구현: 기존 항목을 템플릿에 전달]############
    items = Item.objects.all()
    return render(request, "home.html",{"items": items})
    # return render(
    #     request,
    #     "home.html",
    #     # POST.get: Post가 없을때, 일반적인 Get요청의 기본값
    #     {"new_item_text":request.POST.get("item_text","")},  
    #     )