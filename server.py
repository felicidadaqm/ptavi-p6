#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os.path
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
    
        for line in self.rfile:
            print("El cliente nos manda " + line.decode('utf-8'))

            if line.decode('utf-8') == '\r\n' or not line:
               continue
            else:
               request = line.decode('utf-8').split(" ")

            if request[2] != 'SIP/2.0\r\n':
                self.wfile.write(b'SIP/2.0 400 Bad Request')
            elif request[0] == 'INVITE':
                self.wfile.write(b'SIP/2.0 100 Trying' + b'SIP/2.0 180 Ringing' + b'SIP/2.0 200 OK')
            elif request[0] == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK')
            elif request[0] == 'ACK':
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + audio
                print("Vamos a ejecutar: " + aEjecutar)
                os.system(aEjecutar)
            elif request [0] != 'INVITE' and request[0] != 'BYE' and request[0] != 'ACK':
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed')


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        IP = sys.argv[1]
        port = int(sys.argv[2])
        if os.path.exists(sys.argv[3]):
            audio = sys.argv[3]
        else:
            print("Usage: python3 server.py IP port audio_file")
            sys.exit()
    except IndexError:
        print("Usage: python3 server.py IP port audio_file")

    serv = socketserver.UDPServer(('', port), EchoHandler)
    print("Listening...")
    serv.serve_forever()
