from django.shortcuts import render
from django.http import HttpResponse
from control.models import Order

# Create your views here.


def index(request):
    order = Order.objects.all()
    return render(request, "home.html",{"orders":order})
