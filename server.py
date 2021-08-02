import socket
import binascii
import requests
import time
timeout = 10000 
host = '192.168.3.253'              #your ip address
port = 8888                         #listening port
addr = (host, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("",port))
while True:
    server.settimeout(timeout)
    try:
	    d = server.recvfrom(1024)
    except socket.timeout: 
	    print('Time is out. {0} seconds have passed'.format(timeout))
    received = d[0]
    addr = d[1]
    data_bytes = binascii.hexlify(received)                     #convert UDP packets to HEX
    data_string = str(data_bytes)                               # Parsing some data from UDP packet
    module_id = data_string[27]                                 # Parsing some data from UDP packet
    spo2_hex = str(data_string[34]+data_string[35])             # Parsing some data from UDP packet
    pulse_hex = str(data_string[46]+data_string[47])            # Parsing some data from UDP packet
    spo2_int = int(spo2_hex, 16)                                # Parsing some data from UDP packet
    pulse_int = int(pulse_hex, 16)                              # Parsing some data from UDP packet
    if module_id == '6':
        print(data_bytes)
        print(spo2_int)
        print(pulse_int)
        body = {
        "pulse_int" : f'{pulse_int}',
        "spo2_int" : f'{spo2_int}'
        }
        headers = {'Content-type': 'application/json'}
        r = requests.post(f'http://{host}:5000/post', headers = headers, json = body)                       #POST request to flask server on port 5000
        print(r)
server.close()