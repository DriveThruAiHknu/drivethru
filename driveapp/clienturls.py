from django.urls import path

from . import views

urlpatterns = [
    path('car', views.user_car),
    path('menu/member-orders', views.member_order),
    path('menu/non-member-orders', views.non_member_order),
    path('end', views.user_end),
    path('stt', views.stt),
    path('tts', views.tts),
    path('play',views.audio_play),
    path('voice1', views.voice_recognize1),
    path('voice2', views.voice_recognize2),
]