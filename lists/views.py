from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return render(
        request,
        "home.html",
        # POST.get: Post가 없을때, 일반적인 Get요청의 기본값
        {"new_item_text":request.POST.get("item_text","")},  
        )