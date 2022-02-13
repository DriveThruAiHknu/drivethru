from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.manage_login),
    path('menu/', views.manage_menu),
    path('menu/manage_menu_add.html',views.manage_menuadd)
]