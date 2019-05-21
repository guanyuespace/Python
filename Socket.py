from socket import *
from time import ctime

HOST='127.0.0.1'
PORT= 80
BUFSIZ = 1024
ADDR=(HOST, PORT)
sock=socket(AF_INET, SOCK_STREAM)
sock.bind(ADDR)
sock.listen(5)
while True:
    print('waiting for connection')
    tcpClientSock, addr=sock.accept()
    print('connect from ', addr)
    while True:
        try:
            data=tcpClientSock.recv(BUFSIZ)
        except:
            print(e)
            tcpClientSock.close()
            break
        if not data:
            break
        s='<h1>Hi,you send me :[%s] %s</h1>' %(ctime(), data.decode('utf8'))
        tcpClientSock.send(s.encode('utf8'))
        print([ctime()], ':', data.decode('utf8'))
tcpClientSock.close()
sock.close()


# http://127.0.0.1/getSession?jscode=023ROxBK1bjhs30uJlBK1T5gBK1ROxBx&appid=wxea74db422c9ef21d&appsecret=83e0d4cc526a7b08ca492fc6977c5d62
# Result：
# waiting for connection
# connect from  ('127.0.0.1', 57829)
# ['Tue May 21 15:35:33 2019'] : GET /getSession?jscode=023ROxBK1bjhs30uJlBK1T5gBK1ROxBx&appid=wxea74db422c9ef21d&appsecret=83e0d4cc526a7b08ca492fc6977c5d62 HTTP/1.1
# Host: 127.0.0.1
# Connection: keep-alive
# Cache-Control: max-age=0
# Upgrade-Insecure-Requests: 1
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
# DNT: 1
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6


# from socket import *
#
# HOST='127.0.0.1'
# PORT=80
# BUFSIZ=1024
# ADDR=(HOST, PORT)
# client=socket(AF_INET, SOCK_STREAM)
# client.connect(ADDR)
# while True:
#     data=input('>')
#     if not data:
#         break
#     client.send(data.encode('utf8'))
#     data=client.recv(self.BUFSIZ)
#     if not data:
#         break
#     print(data.decode('utf8'))
