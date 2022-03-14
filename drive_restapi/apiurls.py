# api/urls.py
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
"""
from .views import userView
user_list = userView.as_view({
    'post': 'create',
    'get': 'list'
})
user_detail = userView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', user_list, name='user_list'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
])
"""

from . import views

app_name = 'rest_api'
urlpatterns = [
    #연습
    path('', views.userView.as_view(), name='user'),
    path('<int:userID>', views.userView.as_view()), #api/5(userID)가 전달되는 경우 -> GET

    #고객
    # 1) 차량
    path('currentusers', views.currentuserView.as_view(), name='currentuser'), #현재 모든 자동차 고객 입력
    path('currentusers/<int:currentuserID>', views.currentuserView.as_view()), #일부 삭제

    path('members', views.memberView.as_view(), name='member'), #현재 모든 자동차 고객 입력
    path('members/<int:memberID>', views.memberView.as_view()), #멤버십 고객 자동차 일부 조회

    # 2) 주문
    path('orders/<int:memberid>/last', views.orderView.as_view(), name='order'), #최근 주문 메뉴
    path('prods/prodrecommend', views.orderView.as_view()), #점장 추천 메뉴
    path('prods/prosalesrate', views.orderView.as_view()), #인기 메뉴
    path('orders', views.orderView.as_view()), #고객 주문 세부 정보 입력
    
    #관리자
    # 1) 메뉴
    path('prods', views.prodView.as_view(), name='prod'), #현재 모든 자동차 고객 입력
    path('prods/<int:prodID>', views.prodView.as_view()), #일부 삭제
]   