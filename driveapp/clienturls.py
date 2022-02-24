from django.urls import path

from . import views

urlpatterns = [
    path('1/', views.car),
    path('2/', views.car2),
    path('3/', views.order1),
    path('4/', views.order2),
    path('5/', views.order3),
    path('db/', views.db),
    path('search/', views.SearchFromView.as_view(), name='search')
]