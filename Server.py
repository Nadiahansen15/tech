import socket
import threading
from datetime import datetime
from time import perf_counter
import sys

# import timeout

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
sock.settimeout(4)
time = datetime.now()

connection = True
package_count = 0


def handshake():
    # variable that holds the recieved data and the address is coming from
    data, client_address = sock.recvfrom(1024)

    # accepts or deny the access - if denied, close server.
    print('{}'.format(data.decode()))
    dataresv = data.decode()
    data_spilt = data.decode().split('=', 1)
    # checking the IP address and protocol
    if dataresv.startswith('com-0') and socket.inet_aton(data_spilt[1]):
        # if OK sending accept to client
        sent = sock.sendto('com-0 accept '.encode() + IPAddr.encode(), client_address)
        print('com-0 accept=' + IPAddr)
    elif data:
        # if NOT OK closing server
        try:
            sent = sock.sendto('Connection Denied, closing server'.encode(), client_address)

        finally:
            sent = sock.sendto('Denied '.encode() + IPAddr.encode(), client_address)
            print('Connection Denied. Server closing')
            sock.close()
            exit()
    # receiving accept from client and checking
    data, client_address = sock.recvfrom(1024)
    if 'com-0 accept' in data.decode():

        f = open('Log.txt', 'a')
        f.write("Handshake completed :" + str(time) + " : " + IPAddr + "\n")
        f.close()

        print('ready')
        first_msg()


# checking first message is nr. 0 message
def first_msg():
    global address
    try:
        msg, address = sock.recvfrom(1024)
        message = msg.decode()
        if message.startswith('msg-0'):
            send_msg(message, address)
            msg_function()
        elif message.startswith('con-h '):
            send_msg(message, address)
            msg_function()
        else:
            sent = sock.sendto('not protocol '.encode() + IPAddr.encode(), address)

    except socket.timeout:
        no_response_msg = 'con-res 0xFE'
        sent = sock.sendto(no_response_msg.encode() + IPAddr.encode(), address)
        no_response_client, address = sock.recvfrom(1024)
        print(no_response_client.decode())
        sock.close()
        exit()


# send messages
def send_msg(insert_msg, insert_address):
    if insert_msg.startswith('msg-'):
        pre_counter = int(insert_msg[4])
        counter = int(insert_msg[4]) + 1
        # checking the count is in order
        if counter - pre_counter == 1 and 'msg-' in insert_msg:
            global package_count
            package_count += 1
            print(insert_msg)

            if package_count >= 25:
                allowedmessage = 'max 25 allowed'
                sent = sock.sendto(allowedmessage.encode(), address)
                print(allowedmessage)
                sock.close()
                exit()

        print('received {} bytes from {}'.format(len(insert_msg), insert_address))
        # respond client
        sent = sock.sendto('I am server'.encode(), insert_address)
        print('res-', counter, '= sent {} bytes back to {}'.format(sent, insert_address))

    elif insert_msg.startswith('con-h '):
        print('client alive: ' + insert_msg)

    else:
        print(insert_msg)
        print('error')


def msg_function():
    while connection:
        global address
        # read client message
        msg, address = sock.recvfrom(1024)
        # checking client message
        send_msg(msg.decode(), address)
        # if client sends exit, close socket.


handshake()
