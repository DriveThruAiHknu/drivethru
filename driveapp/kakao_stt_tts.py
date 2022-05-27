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

    # 녹음 시작
    print("---녹음 시작")
    stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, input_device_index=INPUT_DEVICE_INDEX,
                        frames_per_buffer=CHUNK)

    frames = []
    silence = 0
    audio_once = False #한번이라도 말했으면
    
    while True:
        if (silence > 50) & (audio_once):
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
        
    
    print("녹음 끝---\n")

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

=> 요청 결과 코드와 값 반환.

"""

def stt(file_name):

    url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
    key = '51563f7b6dec012e347135fc5bc07bb7'
    headers = {
        "Content-Type": "application/octet-stream",
        #"Transfer-Encoding":"chunked",
        "Authorization": "KakaoAK " + key,
    }

    with open(file_name, 'rb') as fp:
        audio = fp.read()

    res = requests.post(url, headers=headers, data=audio)
    return (res.text)

"""

카카오 TTS 함수
: 해당 함수는 텍스트를 오디오 파일로 합성해주는 함수

=> 음성 파일 이름 : "tts+번호.mp3"

"""

def tts(text, num):
    url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
    key = '51563f7b6dec012e347135fc5bc07bb7'
    headers = {
        "Content-Type" : "application/xml",
        "Authorization" : "KakaoAK " + key,
    }
    
    data = "<speak>"+text+"</speak>"
    
    res = requests.post(url, headers = headers, data = data.encode('utf-8'))
    
    with open("tts"+str(num)+".mp3", "wb") as f:
        f.write(res.content)

"""

환경

"""

# 녹음
import pyaudio
import wave
from array import array
import numpy as np
import requests, json
import time

import requests
import io
from playsound import playsound
#import playsound

# STT
file_num = 0
result_type = ""
result_val = ""
result_list = []
audio_save = False #True 일때만 STT 변환
audio_once = False

# 사용자 변수
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
INPUT_DEVICE_INDEX = 1 #4 (error) -> 1 (success)
WAVE_OUTPUT_FILENAME = "주문"
audio = pyaudio.PyAudio()

# 소리 감지
silence_real = 0

#TTS
tts_num = 1

"""

Main

"""

print("🌿어서오세요! 스타벅스입니다🌿")
tts("어서오세요! 스타벅스입니다~", tts_num)
playsound("tts"+str(tts_num)+".mp3")
tts_num += 1
time.sleep(0.2)
           
print("주문을 원하시는 메뉴나 번호를 말씀해주세요💚\n")
tts("주문을 원하시는 메뉴나 번호를 말씀해주세요~", tts_num)
playsound("tts"+str(tts_num)+".mp3")
tts_num += 1






while True:
    
    stream_vol = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, 
                    input_device_index=INPUT_DEVICE_INDEX,frames_per_buffer=CHUNK)
    
    #크기 측정
    data_vol=stream_vol.read(CHUNK)
    data_chunk_vol=array('h',data_vol)
    vol=max(data_chunk_vol)
    val=""
    
    #목소리 감지
    if(vol>=500):
        
        print("인식중...\n")
        audio_file = mic(FORMAT, CHANNELS, RATE, CHUNK, INPUT_DEVICE_INDEX, WAVE_OUTPUT_FILENAME+str(file_num)+".wav")
        result = stt(WAVE_OUTPUT_FILENAME+str(file_num)+".wav")
        #print(result) #주석
        file_num += 1
        
        #음성 인식 끝나고 반환 결과 있으면 Type 가져오기
        if result.find("type") != -1:
            type_str = result.find("type") + 7
            type_end = result.find("value") - 3
            result_type = result[type_str:type_end]
    
        #Type이 실패한 결과라면
        if result_type == "errorCalled": 
            print("주문을 인식하지 못했습니다.\n 다시 한번 말씀해주세요!")
            tts("주문을 인식하지 못했습니다", tts_num)
            playsound("tts"+str(tts_num)+".mp3")
            tts_num += 1
            time.sleep(0.2)
            tts("다시 한번 말씀해주세요~", tts_num)
            playsound("tts"+str(tts_num)+".mp3")
            tts_num += 1
            continue #다시
            
        #Type이 성공한 결과라면   
        else:
            val_str = result.find('"type":"finalResult"') + 30
            val_end = result.find("nBest") - 3
            val = result[val_str:val_end] #필요한 텍스트만 JSON에서 추출
            
            #정상 텍스트 값이라면 (성공단어가 비어있지 않으면. 결제가 아니라면.)
            if (val != "") & (val != "결제"):
                result_list.append(val)
                stream_vol.stop_stream()
                stream_vol.close()
                silence_real = 0
                audio_once=True
                print(val, "\n메뉴를 선택하셨습니다. 결제 또는 추가할 메뉴를 말씀해주세요!\n")
                tts(val+"\n메뉴를 선택하셨습니다~", tts_num)
                playsound("tts"+str(tts_num)+".mp3")
                time.sleep(0.2)
                tts_num += 1
                tts("결제 또는 추가할 메뉴를 말씀해주세요~", tts_num)
                playsound("tts"+str(tts_num)+".mp3")
                tts_num += 1
                continue
            
            #결제라면
            elif val == "결제":
                print("✔️ 결제 안내를 도와드리겠습니다")
                tts("결제 안내를 도와드리겠습니다~", tts_num)
                playsound("tts"+str(tts_num)+".mp3")
                tts_num += 1
                break
                         
    else:
        if (silence_real > 90) & (audio_once):
            print("\n✔️ 결제 안내를 도와드리겠습니다\n")
            tts("결제 안내를 도와드리겠습니다~", tts_num)
            playsound("tts"+str(tts_num)+".mp3")
            tts_num += 1
            break
            
        silence_real += 1

audio.terminate()

import os

#TTS시 이미 경로 존재해서 permission denied 에러 해결 위해 주문 종료 후 전체 파일 삭제
for i in range(1, tts_num, 1):
    os.remove("tts"+str(i)+".mp3")
    
tts_num = 1