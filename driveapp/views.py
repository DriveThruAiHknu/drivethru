from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from drive_restapi.models import members, todayUsers
from django.shortcuts import redirect
import requests, json
from django.contrib import messages

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
    context = {
        'a'
        :''
    }

    #POST 전송이 들어오면
    if request.method == 'POST':

        #POST 전송 데이터에 있는 'todayUserCar' 가져와서 restapi에 post로 전송 -> 데이터 집어넣기
        todayuserCar = request.POST['todayUserCar']
        url = 'http://localhost:8000/api/todayusers'
        data = {"todayUserCar" : todayuserCar}
        response = requests.post(url, data=data)
        #messages.info(request, response.text) -> 잘 들어갔는지 확인할 때 html 하단에 보면 나옴


        #MEMBER 데이터와 동일하면 MEMBER-ORDER 페이지로 이동
        member = members.objects.all() #member 데이터 db에서 가져오기
        if todayuserCar:
            member = member.filter(memberCar__icontains=todayuserCar) #memberCar와 동일한 차 번호 있는지 확인
            messages.info(request,member.exists())

            if (member.exists() == True): #member에 존재하는 게 True라면
                return redirect('/client/menu/member-orders')
            else:
                return redirect('/client/menu/non-member-orders')
        #return redirect('/client/menu/member-orders') #같은 앱 내 주소로 이동

    """
    if request.method == 'POST':
        url = 'http://localhost:8000/api/todayusers'
        #headers = {'Content-Type': 'application/json; charset=utf-8'}
        todayuserCar = request.POST.get('todayuserCar', False)
        #print(todayuserCar)
        response = requests.post(url, json={'todayuserCar':todayuserCar}).json()
        print(response['todayuserCar'])
        #return render(request, 'member_order.html', {'car':response['todayuserCar']})
        return render(request, 'client/member_order.html', {'car':response})

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
ㅡ
        todayuserCar = request.POST['todayuserCar']
        member = members.objects.all()
        member = members.filter(memberCar__icontains=todayuserCar) #폼 값 = todayuserCar과 동일한 값 가져오기
        if member:
            print(member)
        else:
            print(member+"와 일치하는 건 없음")
        return render(request, 'member_order.html', {'member':member})

    """
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
