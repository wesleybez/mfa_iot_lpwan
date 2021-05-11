import ssl
from socket import socket, AF_INET, SOCK_DGRAM
from dtls import do_patch
do_patch()
sock = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM))
sock.connect(('10.1.1.222', 5684))
sock.send('Hi there')