#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


try:
    method = sys.argv[1]
    receiver = sys.argv[2][0:sys.argv[2].find('@')]
    IP = sys.argv[2][sys.argv[2].find('@')+1:sys.argv[2].find(':')]
    port = int(sys.argv[2][sys.argv[2].rfind(':')+1::])
except IndexError:
    print("Usage: python3 client.py method receiver@IP:SIPport")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, port))

    message = method + " sip:" + receiver + "@" + IP + " SIP/2.0"
    print("Enviando: " + message)
    my_socket.send(bytes(message, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    print('Recibido -- ', data.decode('utf-8'))
    print("Terminando socket...")

    if data.decode('utf-8') != '':
        received = data.decode('utf-8').split()
        print(received)
        print(received[1] + received[4] + received[7])
        if 'Trying' in received:
            if 'Ringing' in received:
                if 'OK' in received:
                    message2 =  'ACK' + " sip:" + receiver + "@" + IP + " SIP/2.0"
                    print("Enviando " + message2)
                    my_socket.send(bytes(message2, 'utf-8') + b'\r\n')

print("Fin.")
