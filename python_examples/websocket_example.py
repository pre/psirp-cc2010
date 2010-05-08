# http://stackoverflow.com/questions/2153294/python-example-of-joes-erlang-websocket-example

import threading
import socket

def start_server():
    tick = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.2.3', 80))
    sock.listen(100)
    while True:
        print 'listening...'
        csock, address = sock.accept()
        tick+=1
        print 'connection!' 
        handshake(csock, tick)
        print 'handshaken'
        while True:
            interact(csock, tick)
            tick+=1


def send_data(client, str):
    #_write(request, '\x00' + message.encode('utf-8') + '\xff')
    str = '\x00' + str.encode('utf-8') + '\xff'
    return client.send(str)
def recv_data(client, count):
    data = client.recv(count)    
    return data.decode('utf-8', 'ignore')

def handshake(client, tick):
    our_handshake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"+"Upgrade:     WebSocket\r\n"+"Connection: Upgrade\r\n"+"WebSocket-Origin: http://localhost:8888\r\n"+"WebSocket-Location: "+" ws://localhost:1234/websession\r\n\r\n"
    shake = recv_data(client, 255)
    print shake
    #We want to send this without any encoding
    client.send(our_handshake)

def interact(client, tick):
    data = recv_data(client, 255)
    print 'got:%s' %(data)
    send_data(client, "clock ! tick%d" % (tick))
    send_data(client, "out ! %s" %(data))

if __name__ == '__main__':
    start_server()