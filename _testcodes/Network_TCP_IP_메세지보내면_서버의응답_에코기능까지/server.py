## server.py

import socket

def run_server(port=4000):      # 사용할 포트 번호 설정.
  host = ''
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))        # ip주소와 포트를 바인딩
    s.listen(1)                 # Client의 연결 요청을 받기 위한 준비
    conn, addr = s.accept()     # 수신 대기, 수신 완료시 Client의 ip주소와 port를 받음.

    while True:

        data = conn.recv(1024)  # Client로 부터 온 데이터 (버퍼크기 1024로 정함, 변경가능)

        if not data: break
        print("Client 한테 온 메세지:", data.decode() )  # byte로 된것을 decode시켜 원래 형태로 변환.

        data1 = '서버의 응답: Thank you I accept your data'.encode()     # 받았다고 다시 Client에게 알림.
        conn.sendall(data1)                                              # encode시킨 data1을 Client에게 날려보냄.

        #conn.sendall(data)  # <= 이것은 에코 모드. (받은것을 그데로 줌) 

    conn.close()

if __name__ == '__main__':
  run_server()