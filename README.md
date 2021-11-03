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
`python application_**.py`

## 설치안내
1. 라즈베리파이 imge 준비 : Raspbian 32-bit Desktop ver (2021-05-07)
2. 라즈베리파이 ssh, spi enable 
3. 원격 다운로드 `git clone https://github.com/AntonSangho/moya_attendance.git`
4. virtualenv 설치 `pip3 install virtualenv`
5. .bashrc 맨 마지막 줄에 path 넣기 `export PATH="$PATH":/home/pi/.local/bin`
6. .bashrc를 적용해주기 `source ~/.bashrc`
7. moyavenv 만들기기 `virtualenv moyavenv`
8. moyavenv 실행시키기 `source ./moyavenv/bin/activate`
9. requirement 설치하기 `pip install -r requirement.txt`
10. numpy issue 해결을 위해 libatlas-base-dev 설치하기 `sudo apt-get install libatlas-base-dev`
11. mfrc522 library 설치하기
	1. 원격저장소에서 받아오기 `git clone https://github.com/pimylifeup/MFRC522-python.git`
	2. `cd MFRC522-python`
	3. `python setup.py install `



## 파일 정보 및 목록 
- 실행파일
- 사운드파일
 

## 저작권 및사용권 정보 
reliquum 

## 배포자 및 개발자 연락처 
sanghoemail@gmail.com 

## 알려진 버그

## 문제 발생 해결첵 

## 업데이트 정보 

