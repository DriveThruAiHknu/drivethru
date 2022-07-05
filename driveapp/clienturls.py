from django.urls import path

from . import views

urlpatterns = [
    path('car', views.user_car),
    path('menu/member-orders', views.member_order),
    path('menu/non-member-orders', views.non_member_order),
    path('end', views.user_end),
    path('analyzer', views.stem_analyzer),
]