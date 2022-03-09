from re import search
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.db.models import Q
from .forms import postForm
from .models import users #users 모델
from django.http.response import HttpResponseRedirect

"""
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
"""

# Create your views here.
def car(request):
    user = users.objects.all() #전부 가져오기
    context = {'users_list' : user}
    return render(request, 'client/client_1.html', context)

def car2(request):
    user = users.objects.all() #membership 데이터 가져오기
    m = request.GET.get('car') #m에 url "?car="형식에서 뒤에 있는 값 가져오기
    if m:
        user = users.filter(userCar__icontains=m) #폼 값 = userCar과 동일한 값 가져오기
    return render(request, 'client/client_2.html', {'post_list': user, 'm':m, })

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


#다시 UI 수정

def re1(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_1.html', context)

def re2(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_2.html', context)

def re3(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_3.html', context)

def re4(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_4.html', context)


#두번째 버전
def rere1(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_re_1.html', context)

def rere2(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_re_2.html', context)

def rere3(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_re_3.html', context)

def rere4(request):
    context = {
        'a':''
    }
    return render(request, 'client/re_re_4.html', context)

    

# database 도전

def db(request):
    user = users.objects.all() #전부 가져오기
    context = {'users_list' : user}
    return render(request, 'client/client_db.html', context)

class SearchFromView(FormView):
    form_class = postForm
    template_name = 'client/client_db_2.html'

    def form_valid(self, form):
        schWord = '%s' % self.request.POST['search_word']
        post_list = users.objects.filter( Q(userCar__icontains = schWord)).distinct()

        context={}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list
        return render(self.request, self.template_name, context)


# 실제 고객 UI

def user_car(request):

    if request.method == 'GET':
        user = users.objects.all() #membership 데이터 가져오기
        m = request.GET.get('car') #m에 url "?car="형식에서 뒤에 있는 값 가져오기
        if m:
            user = users.filter(userCar__icontains=m) #폼 값 = userCar과 동일한 값 가져오기
        return render(request, 'client/user_car.html', {'post_list': user, 'm':m, })
    
    elif request.method == 'POST':
        userCar = request.POST['userCar']
        membership = False
        
        user = users(
            userCar = userCar,
            membership = membership
        )

        user.save()

        return render(request, 'client/user_car.html')


def user_car2(request):
    if request.method == 'GET':
        user = users.objects.get(userCar=request.GET['car']) #userCar에 해당하는 user 객체 가져오기
        if user.membership == True: # 고객이면
            context = {}
            request.session['userCar'] = user.userCar
            request.session['userMember'] = user.membership
            context['userCar'] = request.session['userCar']
            context['userMember'] = request.session['userMember']
            return HttpResponseRedirect(request, '/menu/member-orders')
        else:
            return render(request, 'client/menu/non-member-orders')

    else:
        return render(request, 'client/user_car.html')

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

#POST 구현

"""
class UserView(APIView):
    #POST /users
    def post(self, request):
        user_serializer = UserSerializer(data=request.data) #Request의 data를 UserSerializer로 변환
 
        if user_serializer.is_valid():
            user_serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
            return Response(user_serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    #GET /users
    #GET /users/{userCar}
    def get(self, request, **kwargs):
        if kwargs.get('userCar') is None:
            user_queryset = users.objects.all() #모든 User의 정보를 불러온다.
            user_queryset_serializer = UserSerializer(user_queryset, many=True)
            return Response(user_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            userCar = kwargs.get('userCar')
            user_serializer = UserSerializer(users.objects.get(userCar=userCar)) #car에 해당하는 User의 정보를 불러온다
            return Response(user_serializer.data, status=status.HTTP_200_OK)
 
    #PUT /user/{userCar}
    def put(self, request, **kwargs):
        if kwargs.get('userCar') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            userCar = kwargs.get('userCar')
            user_object = users.objects.get(userCar=userCar)
 
            update_user_serializer = UserSerializer(user_object, data=request.data)
            if update_user_serializer.is_valid():
                update_user_serializer.save()
                return Response(update_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
 
    #DELETE /user/{userCar}
    def delete(self, request, **kwargs):
        if kwargs.get('userCar') is None:
            return Response("invalid request", status=status.HTTP_400_BAD_REQUEST)
        else:
            userCar = kwargs.get('userCar')
            user_object = users.objects.get(userCar=userCar)
            user_object.delete()
            return Response("test ok", status=status.HTTP_200_OK)

            """