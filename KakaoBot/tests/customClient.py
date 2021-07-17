from kakaopy.client import Client
import json
import hcskr
import asyncio
import schedule
import time
from selenium import webdriver
import time as time
from selenium.webdriver.common.keys import Keys
import os
import math
import numpy as np
import qrcode
import requests
import youtube_dl
from PIL import Image
import requests
from io import BytesIO
import urllib.request
import smtplib
from email.mime.text import MIMEText
import random
import glob
import os.path
from pytube import YouTube
from PIL import ImageGrab
import time
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime



sendEmail = "cozombot@naver.com"
password = "wee0909#"

smtpName = "smtp.naver.com" #smtp 서버 주소
smtpPort = 587 #smtp 포트 번호
passcode = random.randint(1, 9999)

def vError(WhyError):
    print('')
    print(' [자가진단] ' + WhyError + ' 설정 에러가 발생했습니다. hcs.eduro.go.kr 사이트에 있는 ' + WhyError + '의 정확한 값을 기입하시기 바랍니다.' )
    print(' [자가진단] 프로그램이 5초 뒤 종료됩니다.')
    time.sleep(5)

        
def singup(a):
    f = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\usr\usr.txt", 'a')
    f.write(a + "\n")
    f.close()
def signread(a):
    f = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\usr\usr.txt", 'r')
    data = f.read()
    if data.find(f"{a}") != -1:
        return 1

def fun_1(a,b):
    return str(np.roots([a, b]))
 


def fun_2(a,b,c):
    return str(np.roots([a, b, c]))
 


def filemaker(filename):
    f = open(rf"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\jindan\{filename}.txt",'w')
    f.close()

def song(url):
    #유튜브 전용 인스턴스 생성
    yt = YouTube(url)
    print(yt.title)


    print(yt.streams.filter(only_audio=True, file_extension='mp4').all())

    # 특정영상 다운로드
    yt.streams.filter(only_audio=True, file_extension='mp4').first().download(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\songs")

    print('success')
    os.system(r"cd C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\songs")
    files = glob.glob("*.mp4")
    for x in files:
        if not os.path.isdir(x):
            filename = os.path.splitext(x)
            try:
                os.rename(x,filename[0] + '.mp3')
            except:
                pass
    return yt.title

class CustomClient(Client):
    async def on_packet(self, packet):
        name = packet.packet_name
        body = packet.to_json_body()
        # print(f"{name} | {body}")

    async def on_message(self, chat):
        
        msgs = chat.message.split()
        print(chat.message)
        compile = chat.message.split("==>")

        if chat.message == "TEST":
            await chat.reply("KAKAOPY is running")

        if chat.message == "태그":
            # 이와 같은 방식으로 메세지를 보내는 법은 깃헙 위키에 나와 있습니다
            attachment = {'mentions': [{'user_id': chat.author_id, 'at': [1], 'len': 2}]}
            await chat.channel.send_chat("@태그", json.dumps(attachment), 1)
        if chat.message == "!정보":
            await chat.send_text(chat.author_id)
        if chat.message == "ping":
            await chat.reply("pong!") 
        if msgs[0] == "!자가진단설정":
            f = open(rf"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\jindan\{chat.author_id}.txt", 'w', encoding = "utf-8")
            await chat.reply(f"{msgs[1]}을(를) 이름으로 등록하였습니다\n{msgs[2]}을(를) 생년월일로 등록하였습니다\n{msgs[3]}을(를) 지역으로 등록하였습니다\n{msgs[4]}을(를) 학교로 등록하였습니다\n{msgs[5]}을(를) 학교급으로 등록하였습니다\n{msgs[6]}을(를) 비밀번호로 등록하였습니다")
            f.write(msgs[1] + " " + msgs[2] + " " + msgs[3] + " " + msgs[4] + " " + msgs[5] + " " + msgs[6] + "\n")
            f.close()
        if msgs[0] == "!즉시자가진단":
            await hcskr.asyncSelfCheck(msgs[1], msgs[2], msgs[3], msgs[4], msgs[5], msgs[6])
            await chat.send_text("자가진단 완료!")
            await hcskr.asyncSelfCheck(msgs[1], msgs[2], msgs[3], msgs[4], msgs[5], msgs[6] , msgs[7])
        if chat.message == "!자가진단":
            f = open(rf"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\jindan\{chat.author_id}.txt", 'r', encoding = "utf-8")
            data = f.readline()
            datas = data.split()
            await hcskr.asyncSelfCheck(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5])
            await chat.reply("자가진단 완료!")
        if chat.message == "!자가진단사진":
            f = open(rf"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\jindan\{chat.author_id}.txt", 'r', encoding = "utf-8")
            data = f.readline()
            datas = data.split()
            await hcskr.asyncSelfCheck(datas[0], datas[1], datas[2], datas[3], datas[4], datas[5])
            await chat.reply("자가진단 완료!")
            await chat.channel.send_text("로딩중")

            eduOffice = datas[2]    # 자가진단 사이트에 있는 시/도명을 입력해주세요.
            eduOffLvl = datas[4]   # 학교급을 입력해주세요 (유치원/초등학교/중학교/고등학교/특수학교)
            stdntName = datas[0]    # 이름을 입력해주세요.
            stdntBirt = datas[1] # 입력 예시: 200909 -> 2020년 09월 09일
            stdntSchn = datas[3]   # 학교명을 정확히 입력해주세요. 정확하게 입력하지 않을 경우 오류가 발생할 수 있습니다.
            stdntPass = datas[5] # hcs.eduro.go.kr 사이트에 로그인하는 비밀번호 4자리를 입력하세요. 반드시 비밀번호가 생성되어있어야 합니다.
            showstdntPass = False    #콘솔창에서 비밀번호를 표시합니다. (Default: False)
            waitingTime = 1
            if eduOffice == '서울' or eduOffice == '서울특별시':
                eduOfficeCode = '01'
                print(' [자가진단] 시/도 설정: 서울특별시')
            elif eduOffice == '부산광역시' or eduOffice == '부산':
                eduOfficeCode = '02'
                print(' [자가진단] 시/도 설정: 부산광역시')
            elif eduOffice == '대구광역시':
                eduOfficeCode = '03'
                print(' [자가진단] 시/도 설정: 대구광역시')
            elif eduOffice == '인천광역시':
                eduOfficeCode = '04'
                print(' [자가진단] 시/도 설정: 인천광역시')
            elif eduOffice == '광주광역시':
                eduOfficeCode = '05'
                print(' [자가진단] 시/도 설정: 광주광역시')
            elif eduOffice == '대전광역시':
                eduOfficeCode = '06'
                print(' [자가진단] 시/도 설정: 대전광역시')
            elif eduOffice == '울산광역시':
                eduOfficeCode = '07'
                print(' [자가진단] 시/도 설정: 울산광역시')
            elif eduOffice == '세종특별자치시':
                eduOfficeCode = '08'
                print(' [자가진단] 시/도 설정: 세종특별자치시')
            elif eduOffice == '경기도':
                eduOfficeCode = '10'
                print(' [자가진단] 시/도 설정: 경기도')
            elif eduOffice == '강원도':
                eduOfficeCode = '11'
                print(' [자가진단] 시/도 설정: 강원도')
            elif eduOffice == '충청북도':
                eduOfficeCode = '12'
                print(' [자가진단] 시/도 설정: 충청북도')
            elif eduOffice == '충청남도':
                eduOfficeCode = '13'
                print(' [자가진단] 시/도 설정: 충청남도')
            elif eduOffice == '전라북도':
                eduOfficeCode = '14'
                print(' [자가진단] 시/도 설정: 전라북도')
            elif eduOffice == '전라남도':
                eduOfficeCode = '15'
                print(' [자가진단] 시/도 설정: 전라남도')
            elif eduOffice == '경상북도':
                eduOfficeCode = '16'
                print(' [자가진단] 시/도 설정: 경상북도')
            elif eduOffice == '경상남도':
                eduOfficeCode = '17'
                print(' [자가진단] 시/도 설정: 경상남도')
            elif eduOffice == '제주특별자치도':
                eduOfficeCode = '18'
                print(' [자가진단] 시/도 설정: 제주특별자치도')
            else:
                vError("시/도")   # 에러 발생 !

            if eduOffLvl == '유치원':
                print(' [자가진단] 학교급 설정: 유치원')
                eduOffLvlCode = '1'
            elif eduOffLvl == '초등학교':
                print(' [자가진단] 학교급 설정: 초등학교')
                eduOffLvlCode = '2'
            elif eduOffLvl == '중학교':
                print(' [자가진단] 학교급 설정: 중학교')
                eduOffLvlCode = '3'
            elif eduOffLvl == '고등학교':
                print(' [자가진단] 학교급 설정: 고등학교')
                eduOffLvlCode = '4'
            elif eduOffLvl == '특수학교':
                print(' [자가진단] 학교급 설정: 특수학교')
                eduOffLvlCode = '5'
            else:
                vError("학교급")   #에러 발생 !

            if stdntName == '이름을_입력해주세요' or None:
                vError("이름")    #에러 발생 !
            else:
                print(' [자가진단] 이름 설정: ' + stdntName)
                
            if stdntBirt == '생년월일_6자리를_입력해주세요' or None:
                vError("생년월일(6자리)")    #에러 발생 !
            else:
                print(' [자가진단] 생년월일(6자리) 설정: ' + stdntBirt)

            if stdntSchn == '학교명을_정확히_입력해주세요' or None:
                vError("학교명")    #에러 발생 !
            else:
                print(' [자가진단] 학교명 설정: ' + stdntSchn)

            if stdntPass == '자가진단_비밀번호_4자리를_입력해주세요' or None:
                vError("비밀번호")    #에러 발생 !
            else:
                if showstdntPass == True:
                    print(' [자가진단] 비밀번호 설정: ' + stdntPass)
                elif showstdntPass == False:
                    print(' [자가진단] 비밀번호 설정: ****')  # showstdntPass Options이 False인 경우, 표시하지 않음
                else:
                    vError("showstdntPass 옵션(비밀번호 표시")  #에러 발생 !
                    



            print(' [자가진단] 유효성 검사가 완료되었습니다. 자가진단(무증상)을 시작합니다.')
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")

            driver = webdriver.Chrome(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\chromedriver.exe", chrome_options=options)
            print('')
            print(' [자가진단] Chrome Webdriver 로 실행됩니다.')
            driver.get("https://hcs.eduro.go.kr/#/loginHome")   
            print(' [자가진단] 자가진단 웹페이지가 열렸습니다.')
            elem = driver.find_element_by_id("btnConfirm2") #자가진단 참여버튼
            elem.click()
            print(' [자가진단] 자가진단 참여버튼을 클릭합니다.')
            elem = driver.find_element_by_xpath("//input[@class='input_text_common input_text_search']")    #학교검색
            elem.click()
            print(' [자가진단] 학교 데이터를 검색합니다.')
            elem = driver.find_element_by_xpath("//select['data-v-f6ebec28 name id']/option[@value='" + eduOfficeCode + "']")  #시/도 설정 메뉴 * 반드시 코드 사용할 것 *
            elem.click()
            elem = driver.find_element_by_xpath("//select['data-v-f6ebec28']/option[@value='" + eduOffLvlCode + "']")  #학교급 설정 메뉴 * 반드시 코드 사용할 것 *
            elem.click()
            elem = driver.find_element_by_xpath("//input[@class='searchArea']")  #학교검색메뉴
            elem.click()
            elem.send_keys(stdntSchn)
            elem.send_keys(Keys.ENTER)
            time.sleep(waitingTime)
            elem = driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul')
            elem.click() #학교선택
            elem = driver.find_element_by_class_name("layerFullBtn").click() #학교선택 버튼클릭(하단)
            print(' [자가진단] 학교를 선택합니다.')
            time.sleep(waitingTime)
            print(' [자가진단] 신상 정보를 입력합니다.')
            time.sleep(waitingTime)
            elem = driver.find_element_by_xpath("//input[@class='input_text_common']")  #이름??
            elem.click()
            elem.send_keys(stdntName)
            elem = driver.find_element_by_xpath("//input[@inputmode='numeric']")  #생년월일
            elem.send_keys(stdntBirt)
            elem = driver.find_element_by_xpath("//input[@id='btnConfirm']")  #신상정보제출
            elem.click()
            print(' [자가진단] 신상 정보 입력을 완료했습니다.')
            time.sleep(waitingTime)
            print(' [자가진단] 비밀번호를 통해 사용자 인증을 시도합니다.')
            time.sleep(waitingTime)
            elem = driver.find_element_by_xpath("//input[@class='input_text_common']")  #비밀번호입력폼
            elem.send_keys(stdntPass)
            elem = driver.find_element_by_xpath("//input[@id='btnConfirm']")  #비밀번호제출
            elem.click()
            print(' [자가진단] 비밀번호를 통해 사용자 인증을 완료했습니다.')
            time.sleep(2)
            driver.save_screenshot(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\jindan\screenshot.png")
            print(' [자가진단] 브라우저를 종료합니다.')
            driver.close()
            await chat.channel.send_text('완료!')
            await chat.send_photo_by_path(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\jindan\screenshot.png", 720, 720)

        if chat.message == "!사용자 정보":
            await chat.channel.get_user_info(int(chat.author_id))
        if chat.message == "이모티콘":
            print("dfsdfs")
            attachment = {'name': '(이모티콘)', 'path': '4414234.emot_007.webp', 'type': 'image/webp', 's': 0, 'alt': '카카오 이모티콘'}
            await chat.channel.send_chat("",json.dumps(attachment),12) 
        if chat.message == "보이스톡 걸기":
            attachment = {'type': 'invite', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            message = {'type': 'invite', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            await chat.channel.send_chat(json.dumps(message),json.dumps(attachment),51)
        if chat.message == "보이스톡 끊기":
            attachment = {'type': 'cancel', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            message = {'type': 'cancel', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            await chat.channel.send_chat(json.dumps(message),json.dumps(attachment),51)
        if chat.message == "페이스톡 걸기":
            attachment = {'type': 'v_invite', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            message = {'type': 'v_invite', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            await chat.channel.send_chat(json.dumps(message),json.dumps(attachment),51)
        if chat.message == "페이스톡 끊기":
            attachment = {'type': 'v_cancel', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            message = {'type': 'v_cancel', 'csIP': '', 'csIP6': '', 'csPort': 9000, 'callId': '', 'duration': 0}
            await chat.channel.send_chat(json.dumps(message),json.dumps(attachment),51)
        if chat.message == "말":
            await chat.send_text("안녕")
        if msgs[0] == "!실프":
            attachment = {'userId': msgs[1]}
            await chat.channel.send_chat("카카오톡 프로필",json.dumps(attachment),17) 
        if msgs[0] == "!일방":
            a = int(msgs[1])
            b = int(msgs[2])
            await chat.reply(str(fun_1(a, b)))
        if msgs[0] == "!이방":
            a = int(msgs[1])
            b = int(msgs[2])
            c = int(msgs[3])
            await chat.reply(str(fun_2(a, b, c)))
        if msgs[0] == "!삭제":
            await chat.channel.delete_message(chat.log_id)
        if chat.type == 18:
            await chat.channel.send_chat("",json.dumps(chat.attachment),18)
        if msgs[0] == "!임지":    

            drinsBlogImage = msgs[1]
            saveName = r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qrin.png"

            urllib.request.urlretrieve(drinsBlogImage, saveName)
            print("저장되었습니다")
            await chat.send_photo_by_path(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qrin.png", 480, 480)
        if msgs[0] == "!큐":
            url = msgs[1]
            qr_img = qrcode.make(url)
            qr_img.save(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qr.png")   
            await chat.send_photo_by_path(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qr.png", 720, 720)             
        if msgs[0] == "!임지큐":
            drinsBlogImage = msgs[2]
            saveName = r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qrin.png"

            urllib.request.urlretrieve(drinsBlogImage, saveName)
            print("저장되었습니다")
            iu_img = Image.open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qrin.png")  # .crop((150, 40, 235, 150))

            #썸내일 만들기
            iu_img.thumbnail((60, 60))
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(msgs[1])
            qr.make()
            iu_instagram = qr.make_image().convert('RGB')

            #이미지 가운데 위치시키기
            pos = ((iu_instagram.size[0] - iu_img.size[0]) // 2, (iu_instagram.size[1] - iu_img.size[1]) // 2)

            iu_instagram.paste(iu_img, pos)
            iu_instagram.save(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qr.png")
            #print(iu_instagram.size)
            iu_instagram.save(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qr.png")
            #print(iu_instagram.size)
            await chat.send_photo_by_path(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\qr\qr.png", 720, 720)
        if compile[0] == "!PY":
            f = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\compile\compiler.py", 'w' , encoding = "utf-8")
            f.write(compile[1])
            f.close()
            result = os.popen(r"python -u C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\compile\compiler.py").read()
            await chat.reply(result)
        if compile[0] == "!C":
            f = open(rf"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\compile\compiler.c", 'w', encoding = "utf-8")
            f.write(compile[1])
            f.close()
            result = os.popen(r'cd "c:\Users\spark\Desktop\kakaopy\KakaoBot\tests\compile\" && gcc compiler.c -o compiler && "c:\Users\spark\Desktop\kakaopy\KakaoBot\tests\compile\"compiler').read()
            await chat.reply(result)
        if msgs[0] == "!노래":
            await chat.send_audio_by_path(rf"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\songs\{song(msgs[1])}.mp3")
        if chat.message == "!로그":
            await chat.reply(chat.log_id)
        f = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\admin\admin.txt")
        data = f.read()
        if  data.find(f"{chat.author_id}") != -1:  
            if msgs[0] == "!어드민추가":
                f = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\admin\admin.txt", 'a', encoding = "utf-8")
                f.write(" " + f"{msgs[1]}")
                await chat.reply(f"어드민 추가 {msgs[1]}")
            if msgs[0] == "!강퇴":
                await chat.channel.kick_member(int(msgs[1]))
            if compile[0] == "!감지":
                wf = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\scan\scan.txt", 'a')
                rf = open(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\scan\scan.txt", 'r')
                data = rf.read()
                if data.find(compile[1]) == -1:
                    wf.write(compile[1])
                    await chat.reply("감지 시작")
                else:
                    await chat.reply("이미 감지중")
            if chat.message == "!감지해제":
                os.remove(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\scan\scan.txt")
            if compile[0] == "!메일":
                await chat.reply("메일을 보내는중...")
                recvEmail = compile[1]
                text = compile[3]
                msg = MIMEText(text)

                msg['Subject'] = compile[2]
                msg['From'] = sendEmail
                msg['To'] = recvEmail
                print(msg.as_string())

                s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
                s.starttls() #TLS 보안 처리
                s.login( sendEmail , password ) #로그인  
                s.sendmail( sendEmail, recvEmail, msg.as_string() ) #메일 전송, 문자열로 변환하여 보냅니다.
                s.close() #smtp 서버 연결을 종료합니다.
                await chat.reply("메일 전송 완료!")
            if chat.message == "!화면":
                img=ImageGrab.grab()
                img.save(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\screen\screencapture.png")
                await chat.send_photo_by_path(r"C:\Users\spark\Desktop\kakaopy\KakaoBot\tests\screen\screencapture.png",  720, 720)
            if chat.message == "!도배":
                for i in range(10):
                    await chat.channel.send_text("도배")
                    time.sleep(0.5)