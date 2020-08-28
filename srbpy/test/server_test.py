import socket
import time

HOST = '192.168.145.28'
PORT = 50050

client = None

while True:
    if client is None:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 心跳检测
            client.connect((HOST, PORT))
        except (Exception)as e:
            print(e)
            continue
    try:
        input_ = {"command":""}
        client.send(input_.encode())
        data = client.recv(1024).decode("utf-8")
        if data=="ok":
            data = client.recv(1024).decode("utf-8")
            print(data)
    except (Exception) as e:
        print(e)
        client = None
