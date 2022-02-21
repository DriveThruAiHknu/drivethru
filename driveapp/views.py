from django.shortcuts import render
from .models import membership #membership 모델

# Create your views here.
def car(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_1.html', context)

def car2(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_2.html', context)

def order1(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_3.html', context)

def order2(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_4.html', context)   

def order3(request):
    context = {
        'a':''
    }
    return render(request, 'client/client_5.html', context)      
def manage_login(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_login.html', context)
def manage_menu(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_menu.html', context)

def manage_menuadd(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_menu_add.html', context)
