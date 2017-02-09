#python4

import socket
import sys
import csv
import pymysql
from _thread import  start_new_thread
#
HOST = '' #all available interfaces
PORT = 30


#1. open Socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Database 연결
    ipAddr = socket.gethostbyname(socket.gethostname())
    conn2 = pymysql.connect(host = ipAddr , port = 3306 , user = 'root' , passwd='', charset='utf8', autocommit= True)
    cur = conn2.cursor()

    # cur.execute("CREATE DATABASE IF NOT EXIST CARINFO")
    cur.execute("USE CarInfoDB")

   # Timestamp, Raspberry ID, CAN ID, DATA Length, DATA[0], DATA[1], ... , DATA[7]

except socket.error as msg :
    print ('Socket created')
    sys.exit(0)

#2. bind to a address and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind Failed. Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
    sys.exit()

print ('Socket bind complete')

#3. Listen for incoming connections
s.listen(10)
print ('Socket now listening')


#keep talking with the client


def client_thread(conn):
    # conn.sendall("Welcome to the Server. Type messages and press enter to send.\n")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        # reply = "OK . . " + data.decode()
        reply = data.decode() # 받은 데이터 문자열
        conn.sendall(reply.encode(encoding='utf_8', errors='strict'))
        print(reply)
        #database 삽입

#        st = reply.split(',')
        st = ['']*12
	
        st[0]=reply[0:17]
        st[1]=reply[17:20]
        st[2]=reply[20:21]
        st[3]=reply[21:23]
        st[4]=reply[23:25]
        st[5]=reply[25:27]
        st[6]=reply[27:29]
        st[7]=reply[29:31]
        st[8]=reply[31:33]
        st[9]=reply[33:35]
        st[10]=reply[35:37]
        st[11]=reply[37:48]      
        
        cur.execute("INSERT INTO `CarInfoDB`.`carinfo` (`Timestamp`, `can_id`, `data_length`, `data[0]`, `data[1]`, `data[2]`, `data[3]`, `data[4]`, `data[5]`, `data[6]`, `data[7]`, `car_id`) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (st[0],st[1], st[2], st[3], st[4], st[5], st[6], st[7], st[8], st[9], st[10], st[11]))

    conn.close()

while 1:
    #4. Accept connection
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(client_thread,(conn,))
s.close()

