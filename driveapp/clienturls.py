from django.urls import path

from . import views

urlpatterns = [
    path('1/', views.car),
    path('2/', views.car2),
    path('3/', views.order1),
    path('4/', views.order2),
    path('5/', views.order3),
    path('db/', views.db),
    path('search/', views.SearchFromView.as_view(), name='search'),
    path('re/1', views.re1),
    path('re/2', views.re2),
    path('re/3', views.re2),
    path('re/4', views.re2),
    path('rere/1', views.rere1),
    path('rere/2', views.rere2),
    path('rere/3', views.rere3),
    path('rere/4', views.rere4),

    #실제
    path('car', views.user_car),
    path('menu/member-orders', views.member_order),
    path('menu/non-member-orders', views.non_member_order),
    path('end', views.user_end),

    #REST
    #path('user', views.UserView.as_view()), #User에 관한 API를 처리하는 view로 Request를 넘김
    #path('user/<str:userCar>', views.UserView.as_view()) #User pk id가 전달되는 경우


]