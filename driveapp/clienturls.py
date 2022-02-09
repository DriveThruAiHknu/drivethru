from django.urls import path

from . import views

urlpatterns = [
    path('1/', views.car),
    path('2/', views.car2),
]