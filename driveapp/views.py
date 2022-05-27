from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from drive_restapi.models import prod
from django.shortcuts import redirect
import requests, json
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

# 1) 관리자  
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

# 2) 고객
from drive_restapi.models import member, today_user
members = member.objects.all() #member 데이터 db에서 가져오기

def user_car(request):
    context = {
        'a'
        :''
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














"""

어서오세요. 스타벅스입니다~
주문을 원하시는 메뉴나 번호를 말씀해주세요

1) 메뉴 말할 경우
~ 메뉴를 선택하셨습니다. 결제 또는 추가할 메뉴를 말씀해주세요! (다시 주문 입력 대기)

2) 메뉴 하나 주문 후 30초 이상 침묵일 경우
결제 안내를 도와드리겠습니다 (주문 종료로 인식)

3) 메뉴 아무것도 주문하지 않고 30초 이상 침묵일 경우
주문 받을 때까지 대기

4) 결제 말할 경우
결제 안내를 도와드리겠습니다 (주문 종료로 인식)

5) TTS 결과 실패할 경우
주문을 인식하지 못했습니다. 다시 한번 말씀해주세요! (다시 주문 입력 대기)

"""

"""

[ 오디오 녹음 함수 ]
:  해당 함수는 시작부터 쭉 녹음해서 말이 끝나고 4초가 지나면 오디오 파일로 저장해줌.

0. 변수 (침묵시간 sielence) (한 번이라도 말했는지 여부 audio_once)
1. stream 열고, stream으로 부터 읽어서 Frame에 추가
2. 500 이상의 소리 크기가 감지되면 silence(침묵 시간 초기화), audio_once True(한번이라도 말함)
3. 아니라면 silence++ (침묵시간 증가), continue(루프 조건으로)
4. 한번이라도 말을 했고, 침묵시간이 50(약 4초) 지나면 break(종료)

=> True 반환.

"""

def mic(FORMAT, CHANNELS, RATE, CHUNK, INPUT_DEVICE_INDEX, WAVE_OUTPUT_FILENAME):

    # 변수
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    INPUT_DEVICE_INDEX = 1 #4 (error) -> 1 (success)
    WAVE_OUTPUT_FILENAME = "주문.wav"
    audio_once = False
    audio = pyaudio.PyAudio()
    # 녹음 시작
    logging.info("---녹음 시작")
    stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, input_device_index=INPUT_DEVICE_INDEX,
                        frames_per_buffer=CHUNK)

    frames = []
    silence = 0
    audio_once = False #한번이라도 말했으면
    
    while True:
        if (silence > 43) & (audio_once):
            break
            
        data = stream.read(CHUNK) #음성 데이터 스트림으로부터 읽어오기
        frames.append(data) #스트림 -> 프레임에 추가
        
        data_chunk = array('h', data) #볼륨 측정
        vol = max(data_chunk) #볼륨 측정
        
        if(vol >= 500):
            silence = 0
            audio_once = True
        else:
            silence += 1
            continue
        
    
    logging.info("녹음 끝---\n")

     #녹음 끝

    stream.stop_stream()
    stream.close()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    return True

"""

카카오 STT 함수
: 해당 함수는 오디오 파일을 텍스트로 변환 요청해주는 함수.

=> 요청 결과 코드와 값 = res.text = result
=> 타입 확인해서 성공하면, 성공한 결과 인식 값 반환
=> 실패하면, "주문을 인식하지 못했습니다." 반환

"""

def stt(request):

    url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    key = '51563f7b6dec012e347135fc5bc07bb7'
    headers = {
        "Content-Type": "application/octet-stream",
        #"Transfer-Encoding":"chunked",
        "Authorization": "KakaoAK " + key,
    }

    with open(request.GET['file_name']+".wav", 'rb') as fp:
        audio = fp.read()

    res = requests.post(url, headers=headers, data=audio)
    result = res.text

    #음성 인식 끝나고 반환 결과 있으면 Type 가져오기
    if result.find("type") != -1:
        type_str = result.find("type") + 7
        type_end = result.find("value") - 3
        result_type = result[type_str:type_end]
    
     #Type이 실패한 결과라면
    if result_type == "errorCalled": 
        val = "주문을 인식하지 못했습니다."

    #Type이 성공한 결과라면   
    else:
        val_str = result.find('"type":"finalResult"') + 30
        val_end = result.find("nBest") - 3
        val = result[val_str:val_end] #필요한 텍스트만 JSON에서 추출
        val_json = {"val":val}
    return JsonResponse(val_json)


def audio_play(request):
    playsound("tts"+request.GET['file_name']+".mp3")
    time.sleep(0.2)
    #os.remove("tts"+".mp3")
    return HttpResponse("tts"+request.GET['file_name']+".mp3"+" 실행 성공")
    
"""

카카오 TTS 함수
: 해당 함수는 텍스트를 오디오 파일로 합성해주는 함수

=> 음성 파일 이름 : "tts+번호.mp3"

"""
import pyaudio
import wave
from array import array
import numpy as np
import requests, json
import time

import requests
import io
import os
from playsound import playsound
import logging
logging.basicConfig(level='DEBUG')

def tts(request):
    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    key = '51563f7b6dec012e347135fc5bc07bb7'
    headers = {
        "Content-Type" : "application/xml",
        "Authorization" : "KakaoAK " + key,
    }

    data = "<speak>"+str(request.GET['text'])+"</speak>"
    
    res = requests.post(url, headers = headers, data = data.encode('utf-8'))
    
    with open("tts"+".mp3", "wb") as f:
        f.write(res.content)
    
    playsound("tts"+".mp3")
    time.sleep(0.2)

    os.remove("tts"+".mp3")

    return HttpResponse("tts"+request.GET['text']+".mp3"+" 실행 성공")

#처음 음성인식 확인할 때 -> 초수 안세도 되고, 무조건 들어오면 바로 녹음
def voice_recognize1(request):

    # 변수
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    INPUT_DEVICE_INDEX = 1 #4 (error) -> 1 (success)
    WAVE_OUTPUT_FILENAME = "주문"
    voice_result = ""
    audio = pyaudio.PyAudio()
    

    # 크기 측정
    while True:

        stream_vol = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, 
                    input_device_index=INPUT_DEVICE_INDEX,frames_per_buffer=CHUNK)

        #크기 측정
        data_vol=stream_vol.read(CHUNK)
        data_chunk_vol=array('h',data_vol)
        vol=max(data_chunk_vol)

        #목소리 감지
        if(vol>=500):
            logging.info("인식중...\n")
            audio_file = mic(FORMAT, CHANNELS, RATE, CHUNK, INPUT_DEVICE_INDEX, WAVE_OUTPUT_FILENAME+str(1)+".wav")
            
            #오디오파일 저장 성공했으면
            voice_result = "저장" #오디오 저장함
            audio.terminate()
            return HttpResponse(voice_result) #저장



#두번째 음성녹음 실행 -> 초수 재서 몇 초 이상이면 그냥 끝내고 넘어가기
def voice_recognize2(request):

    # 변수
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    INPUT_DEVICE_INDEX = 1 #4 (error) -> 1 (success)
    WAVE_OUTPUT_FILENAME = "주문"
    voice_result = ""
    silence_real = 0
    audio = pyaudio.PyAudio()
    

    # 크기 측정
    while True:

        stream_vol = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, 
                    input_device_index=INPUT_DEVICE_INDEX,frames_per_buffer=CHUNK)

        #크기 측정
        data_vol=stream_vol.read(CHUNK)
        data_chunk_vol=array('h',data_vol)
        vol=max(data_chunk_vol)

        #목소리 감지
        if(vol>=500):
            logging.info("인식중...\n")
            audio_file = mic(FORMAT, CHANNELS, RATE, CHUNK, INPUT_DEVICE_INDEX, WAVE_OUTPUT_FILENAME+str(1)+".wav")
            
            #오디오파일 저장 성공했으면
            voice_result = "저장" #오디오 저장함
            silence_real = 0 #침묵 시간 초기화
            audio.terminate()
            return HttpResponse(voice_result) #저장

        else:
            if (silence_real > 90):
                voice_result="대기초과" 
                audio.terminate()
                return HttpResponse(voice_result) #끝

            silence_real += 1

def member_order(request):
    context = {
        'a':''
    }
    return render(request, 'client/member_order.html', context)


def non_member_order(request):
    context = {
        'a':''
    }
    return render(request, 'client/non_member_order.html', context) 

def user_end(request):
    context = {
        'a':''
    }
    return render(request, 'client/user_end.html', context)
