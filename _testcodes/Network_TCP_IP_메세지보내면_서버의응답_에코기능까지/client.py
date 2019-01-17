import socket

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('192.168.109.231', 4000))                    # 연결 시도할 서버의 ip주소, 포트번호
    while True:

        send_data = input()                         # 사용자 입력대기
        print("서버로보낸 메시지:", send_data)      # 그냥 내가 보낸 데이터 출력(확인용)

        s.sendall(send_data.encode())               # str형태를 전송가능한 byte형태로 인코딩함.
        if not send_data: break

        recive_data = s.recv(1024)                           # 서버로 부터 오는 데이터
        print("서버에서 받은 메세지", recive_data.decode())  # 서버에서 받은 데이터를 출력.

    s.close()

if __name__ == '__main__':
  run()