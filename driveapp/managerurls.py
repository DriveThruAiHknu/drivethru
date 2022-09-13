from django.urls import path

from . import views

urlpatterns = [
    path('login', views.manage_login),
    path('menu', views.manage_menu),
    path('manage-menu-addendum',views.manage_menuadd),
    path('manage-menu-update',views.manage_menuupdate),
    path('manage-orders',views.manage_orders),
    path('manage-recommendation-menu',views.manage_recommendation_menu),
    path('staff-orders',views.staff_orders),
]