# -*- coding : cp949 -*-

import socket


'''
HOST='' #호스트를 지정하지 않으면 가능한 모든 인터페이스를 의미한다.
PORT=50007 #포트지정
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1) #접속이 있을때까지 기다림
conn, addr = s.accept() #접속 승인
print('Connected by', addr)
while True:

    #conn.send(b'Hello, python')
    server_data = "connect"
    s.sendall(server_data.encode())
    print("sending data : ", server_data)

    if not server_data:
        break

    client_data = s.recv(1024)
    print("receive data : ", client_data)

    #conn.send(data) #받은 데이터를 그대로 클라이언트에 전송

conn.close()
'''

HOST='' #호스트를 지정하지 않으면 가능한 모든 인터페이스를 의미한다.
PORT=50007 #포트지정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST,PORT))
while True:
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()
    send_data = bytes('ReAdy', encoding = 'ascii')
    #send_data = b'ReAdy'
    client_socket.sendall(send_data)

    data = client_socket.recv(1024)
    data = data.decode('utf-8')

    if data:
        print(data)
    if data == 'quit':
        break


client_socket.close()
