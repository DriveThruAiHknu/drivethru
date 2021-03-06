from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from drive_restapi.models import prod
from django.shortcuts import redirect
import requests, json
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse


"""
1) 관리자
""" 
def manage_login(request):
    context = {
        'a':''
    }
    return render(request, 'manager/manage_login.html', context)


def manage_menu(request):    
    class_prods = prod.objects.all()
    return render(request, 'manager/manage_menu.html', {'class_prods':class_prods})


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



"""
2) 고객
"""


# 1. 차 조회
from drive_restapi.models import member, today_user
members = member.objects.all() #member 데이터 db에서 가져오기

def user_car(request):
    context = {
        'a':''
    }

    #POST 전송이 들어오면
    if request.method == 'POST':

        #POST 전송 데이터에 있는 'todayUserCar' 가져와서 restapi에 post로 전송 -> 데이터 집어넣기
        todayuserCar = request.POST['todayUserCar']
        url = 'http://localhost:8000/api/todayusers'
        #url = 'http://3.37.186.91:8000/api/todayusers'
        data = {"today_user_car" : todayuserCar}
        response = requests.post(url, data=data)
        #messages.info(request, response.text) -> 잘 들어갔는지 확인할 때 html 하단에 보면 나옴


        #MEMBER 데이터와 동일하면 MEMBER-ORDER 페이지로 이동
        if todayuserCar:
            member = members.filter(member_car__icontains=todayuserCar) #memberCar와 동일한 차 번호 있는지 확인
            messages.info(request,member.exists())

            if (member.exists() == True): #member에 존재하는 게 True라면
                return redirect('/client/menu/member-orders')
            else:
                return redirect('/client/menu/non-member-orders')
        #return redirect('/client/menu/member-orders') #같은 앱 내 주소로 이동
        
    return render(request, 'client/user_car.html', context)


# 2. 고객 주문
from drive_restapi.models import prod
prods = prod.objects.all() #prod 데이터 db에서 가져오기
prods_val = prod.objects.values_list()
prod_list = list(prods_val)
print(prod_list)


def member_order(request):
    #context = { 'a':''}
    return render(request, 'client/member_order.html', {'prods':prod_list})


def non_member_order(request):
    context = {
        'a':''
    }
    return render(request, 'client/non_member_order.html', context) 


def user_end(request):
    context = {
        'a':''
    }
    return render(request, 'client/user_end.html', context)\



#3) 형태소 분석기
"""
형태소 분석기
"""
from ckonlpy.tag import Postprocessor
from ckonlpy.tag import Twitter
import pandas as pd
from ckonlpy.utils import load_wordset
from ckonlpy.utils import load_replace_wordpair
from ckonlpy.utils import load_ngram

from django.http import JsonResponse
import os

def stem_analyzer(requests):
    print("stt로 받은 문자열")
    print(requests.GET['resText'])
    sent = requests.GET['resText']


    twitter = Twitter()

    #메뉴 추가하기
    cafemenu = pd.read_csv('cafemenu.csv')
    cafemenu['이름'].dropna()

    menudata=cafemenu['이름'].str.replace(' ', '')#데이터 형식 변경
    for i in menudata:
        twitter.add_dictionary(i, 'Noun')

    menudata=cafemenu['이름']
    for i in menudata:
        twitter.add_dictionary(i, 'Noun')
        
    #옵션 종류 추가하기
    cafeoption = pd.read_csv('cafeoption.csv')
    cafeoption['옵션 종류'].dropna()
    optiondata=cafeoption['옵션 종류'].str.replace(' ', '')

    for i in optiondata:
        twitter.add_dictionary(i, 'Noun')
        
    optiondata=cafeoption['옵션 종류']
    for i in optiondata:
        twitter.add_dictionary(i, 'Noun')
 
    #문장에 필요없는 단어
    stopwords = load_wordset('./tutorials/stopwords.txt')

    #의미가 같은 것으로 변경할 단어
    replace = load_replace_wordpair('./tutorials/replacewords.txt')

    #띄어쓰기 없애는 단어로
    ngrams = load_ngram('./tutorials/ngrams.txt')

    #첫번째 분석 하기
    postprocessor = Postprocessor(
            base_tagger = twitter, # base tagger
            replace = replace, # 해당 단어 set 치환
            stopwords = stopwords # 해당 단어 필터
        )

    mywords = ""
    for i in postprocessor.pos(sent):
        mywords+=i[0]

    #print("단어 변환+단어 삭제 결과:  "+mywords)

    #두번째 분석 하기
    postprocessor = Postprocessor(
        base_tagger = twitter, # base tagger
        replace = replace, # 해당 단어 set 치환
        stopwords = stopwords, # 해당 단어 필터
    )

    mywords2 = ""
    for i in postprocessor.pos(mywords):
        mywords2+=i[0]
    #print("단어 변환+단어 삭제2 결과:  "+mywords2)
        
    #띄어쓰기만 조정
    postprocessor = Postprocessor(
        base_tagger = twitter, # base tagger
        ngrams = ngrams # 해당 복합 단어 set을 한 단어로 결합
    )

    orderdata = []
    order = []
    delete_word = [' ', '-']

    for i in postprocessor.pos(mywords2):
        orderdata.append(i[0])
    #print("단어만 추가: ", orderdata)

    #부호 삭제하여 리스트에 추가

    for i in orderdata:
        for j in delete_word:
            i=i.replace(j, '')
        order.append(i)
    print("\n")
    print("결과:", order)

    return JsonResponse(order, safe=False)
