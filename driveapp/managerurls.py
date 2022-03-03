from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.manage_login),
    path('menu/', views.manage_menu),
    path('menu/manage_menu_add.html',views.manage_menuadd),
    path('menu/manage_orders.html',views.manage_orders),
    path('menu/manage_recommendation_menu.html',views.manage_recommendation_menu),
]