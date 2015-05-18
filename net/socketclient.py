#coding=utf-8

'''
Created on 2014-9-19

@author: liangkangzhu
'''

import socket

SOCKET_BUFFER_SIZE = 4 * 1024

def send_tcp_messages(addr, messages):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = None
    try:
        sock.connect(addr)
        sock.sendall(messages.encode('utf8'))
        response = sock.recv(SOCKET_BUFFER_SIZE)
    except:
        pass
    finally:
        sock.close()
    return response

def send_upd_messages(addr, messages):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    response = None
    try:
        sock.sendto(messages.encode('utf8'), addr)
        response = sock.recvfrom(SOCKET_BUFFER_SIZE)
    except:
        pass
    finally:
        sock.close()
    return response

def test_connection(addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rst = True
    try:
        sock.connect((addr, port))
    except:
        rst = False
    finally:
        sock.close()
    return rst
