from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from drive_restapi.models import members, currentusers

# Create your views here.

# 1) 관리자  
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

def manage_recommendation_menu(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_recommendation_menu.html', context)
    
def manage_orders(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_orders.html', context)

def staff_orders(request):
    context = {
        'a':''
    }
    return render(request, 'manager/staff_orders.html', context)
  
# 2) 고객

def user_car(request):
    """
    if request.method == 'GET':
        member = members.objects.all() #currentusers 데이터 가져오기
        c = request.GET.get('car') #m에 url "?car="형식에서 뒤에 있는 값 가져오기
        if c:
            member = members.filter(memberCar__icontains=c) #폼 값 = memberCar과 동일한 값 가져오기
        return render(request, 'client/user_car.html', {'post_list': member, 'm':c, })
    
    elif request.method == 'POST':
        userCar = request.POST['userCar']
        membership = False
        
        user = users(
            userCar = userCar,
            membership = membership
        )

        user.save()

        return render(request, 'client/user_car.html')
        """
    context = {
        'a':''
    }
    return render(request, 'client/user_car.html', context)   


def member_order(request):
    context = {
        'a':''
    }
    return render(request, 'client/member_order.html', context)    

def non_member_order(request):
    context = {
        'a':''
    }
    return render(request, 'client/non_member_order.html', context) 

def user_end(request):
    context = {
        'a':''
    }
    return render(request, 'client/user_end.html', context)
