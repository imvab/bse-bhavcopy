from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock

# Create your views here.


def homepage(request):
    data = {
        'stocks': Stock.objects.all()
    }
    # return HttpResponse("pythonprogramming.net homepage! Wow so #amaze.")
    return render(request, 'base.html')
