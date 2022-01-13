# 모야입출입시스템
라즈베리파이로 RFID카드로 입장과 출입을 웹사이트에서 보여주는 프로젝트

# 구성 및 필수 조건 
### BOM

| 부품명 | 수량 |  
| ----------- | ----------- | 
| 라즈베리파이 3B | 1ea |  
| 라즈베리파이 터치스크린 7인치  | 1ea |
| 3A 전원 아답터 | 1ea |
| USB , aux 스피커 | 2ea |
| RFID-RC522 | 1ea |
| RFID card  | 600ea |


###  pin 연결 

|  Raspberry pi  | RFID  |  
| ----------- | ----------- | 
| GPIO 8 | SDA |  
| GPIO 11  | SCK |
| GPIO 10 | MOSI |
| GPIO 9 | MISO |
| GND | GND |
| GPIO 25 | RST |
| 3.3V | 3.3V |


### 실행
```bash 
python application_**.py
```

## 설치안내
1. 라즈베리파이 imge 준비 : Raspbian 32-bit Desktop ver (2021-05-07)
2. ssh, spi enable 
3. moya_attendance  
```bash
git clone https://github.com/AntonSangho/moya_attendance.git 	#원격 다운로드 
pip3 install virtualenv 										#virtualenv 설치
export PATH="$PATH":/home/pi/.local/bin 						#.bashrc맨 마지막 줄에 path 넣기
source ~/.bashrc												# .bashrc를 적용해주기
virtualenv moyavenv 											#moyavenv 만들기기
source ./moyavenv/bin/activate 									#moyavenv 실행시키기
pip install -r requirements.txt 									#requirements 설치하기
sudo apt-get install libatlas-base-dev #numpy issue 해결을 위해 libatlas-base-dev 설치하기
```
4. mfrc522 library 
```bash
cd moya_attendance
git clone https://github.com/pimylifeup/MFRC522-python.git
cd MFRC522-python
python setup.py install
cd ..
git submodule add ./MFRC522-python
```
5. VNC Cloud
```bash
sudo apt update
sudo apt install realvnc-vnc-server realvnc-vnc-viewer
```
```doc
Enabling VNC Server graphically
* On your Raspberry Pi, boot into the graphical desktop.
* Select Menu > Preferences > Raspberry Pi Configuration > Interfaces.
* Ensure VNC is Enabled.
```
6. Systemctl - flask service
```bash
sudo cp moya-flask-xx.service /lib/systemd/system/moya-flask-xx.service
sudo chmod 644 /lib/systemd/system/moya-flask-xx.service #권한설정 변경
sudo systemctl daemon-reload #변경한것 적용하기
sudo systemctl enable moya-flask-xx.service #활성화 시키기
sudo systemctl start moya-flask-xx.service #재부팅후에도 실행되도록 하기
```
7. Systemctl - kiosk

```bash
#불필요한 소프트웨어 제거
sudo apt-get purge wolfram-engine scratch scratch2 nuscratch sonic-pi idle3 -y
sudo apt-get purge smartsim java-common minecraft-pi libreoffice* -y
sudo apt-get clean
sudo apt-get autoremove -y
```
```bash
#업데이트하기
sudo apt-get update
sudo apt-get upgrade
```
```bash
#xdotool설치
sudo apt-get install xdotool unclutter sed
```
```doc
#부팅시 자동로그인
sudo raspi-config
Boot Option 
Desktop 
Desktop Autologin
`````
```bash
#부팅시 자동실행하도록하기
sudo cp kiosk.service /lib/systemd/system/kiosk.service
sudo systemctl daemon-reload
```

```doc
#명령어
-활성화 : sudo systemctl enable kiosk.service   
-시작하기: sudo systemctl start kiosk.service 
-상태확인 : sudo systemctl status kiosk.service 
-중지하기: sudo systemctl stop kiosk.service
-비활성화: sudo systemctl disable kiosk.service
```

8. xterminal
```bash
sudo vim /etc/xdg/lxsession/LXDE-pi/autostart
#파일의 밑에다가 아래 라인 추가
@lxterminal --geometry=80x55
```

9. Disable power warning 
```bash
sudo vim /boot/config.txt
#아래 내용 추가 
avoid_warnings=2
```

10. 한글깨짐 해결
```doc
raspi-config 
set-locale : korean 
charactor Set :UTF-8 
```

11. Crontab
```bash
#crontab 설정 열기
sudo crontab -e
#Editer를 vim으로 한 후에 맨 마지막 줄 가기
: $
#자정에 재부팅되록 설정
0 0 * * * /sbin/shutdown -r now
```

12. 권한설정 
- moya 사용자계정만들기
```bash
sudo su 
adduser moya 
```
- moya 그룹을 추가하기
```bash
sudo su 
cat /etc/group | grep pi (pi의 그룹확인)
usermod -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,spi,i2c,gpio moya
```
- 부팅시 moya계정으로 자동로그인하기
```bash
sudo vim /etc/lightdm/lightdm.conf
```
 autologin-user=moya 로 변경


## 파일 정보 및 목록 
- 실행파일
- 사운드파일
 

## 저작권 및사용권 정보 
reliquum 

## 배포자 및 개발자 연락처 
sanghoemail@gmail.com 

## 알려진 버그

## 문제 발생 해결첵 
- wifi가 잘 안잡한다
: 사용하려고하는 wifi에 priority 설정한다. (sudo vi /etc/wpa_supplicant/wpa_supplicant.conf)
- 스크린이 자주 꺼진다.
: SD카드 불량
## 업데이트 정보 

## 참고
[키오스크모드](https://pimylifeup.com/raspberry-pi-kiosk/)
[부팅스크립트만들기](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)

