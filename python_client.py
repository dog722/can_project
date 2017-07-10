import socket
import can
import time
import socket 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
#GPIO.output(22,True)

#socket셋팅
HOST = '52.79.108.212'#서버
PORT = 30
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.connect((HOST,PORT))


# 실제 차량에서 테스트하기 전, 가상의 캔 데이터를 만들어서 보냄 #
bus = can.interface.Bus(channel='can0' , bustype='socketcan_native')
msg = can.Message(arbitration_id=0x7de ,data=[0,25,0,1,3,1,4,1] , extended_id=False)

car_id = socket.gethostname()

#timestamp 문자 변환
timestamp = msg.timestamp
timestamp2= '%.017x'%timestamp

#canId 문자 변환
can_id = msg.arbitration_id
can_id2 = '%03x'%can_id

#length 문자 변환
data_length = msg.dlc
data_length2 = '%01x'%data_length

#data[0]-data[7]까지 문자 변환
data = msg.data
i=0
data2 = ['0'] * data_length
for temp in data:
    data2[i] = '%02x'%temp
    i+=1

#join함수 참고하기!
final_can_msg = timestamp2+can_id2+data_length2+ \
                data2[0]+data2[1]+data2[2]+data2[3]+ \
                data2[4]+data2[5]+data2[6]+data2[7]+car_id

#최종 문자열 및 길이 출력
print('final_can_msg : '+final_can_msg + '  length: '+ str(len(final_can_msg)))

j=0
while True : 
	s.send(final_can_msg.encode(encoding='utf_8', errors='strict'))
	time.sleep(0.5)
	print(final_can_msg + "\n")
