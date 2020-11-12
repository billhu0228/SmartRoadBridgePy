import io
import socket
from srbpy.model import Model, Bridge
from srbpy.server.json_encoders import ModelEncoder
from srbpy.stdlib.std_piers import *
import json

BUF_SIZE = 1024


class SRBServer():
    def __init__(self, address="localhost", port: int = 50050):
        self.address = address
        self.port = port

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("create socket successfully!")
        server.bind((self.address, self.port))
        print('bind socket successfully!')
        server.listen(5)
        print('listen successfully!')
        client = None
        while True:  # 循环收发数据包，长连接
            if client is None:
                client, address = server.accept()  # 因为设置了接收连接数为1，所以不需要放在循环中接收
            try:
                data = client.recv(BUF_SIZE)
                if data.decode("utf-8") == "align":
                    client.send(b"ok")
                    client.send(b"58469")
                else:
                    client.send("未知命令.".encode())
            except (Exception)as  e:
                print(e)
                client = None

            # conn.send(b"welcome to srbpy.server")
            # conn.settimeout(30)
            # while True:
            #    szBuf = conn.recv(1024)
            #    rev=str(szBuf, 'utf-8')
            #    if rev=="exit":
            #        conn.close()
            #        print("end of servive")


#


if __name__ == "__main__":
    server = SRBServer(address="192.168.145.28", port=50050)
    server.run()
