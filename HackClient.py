import multiprocessing
import socket
from configparser import ConfigParser
import threading

# get config file
parser = ConfigParser()
parser.read('con.ini')

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
# print("Your Computer Name is:" + hostname)
# print("Your Computer IP Address is: " + IPAddr)
server_address = ('localhost', 10000)
counter = 1
count = 0
max_package = parser.getboolean('Max', 'Start')

connection = True
keep_a_live = True


def heartbeat():
    if keep_a_live:
        threading.Timer(3.0, heartbeat).start()
        heartmsg = 'con-h 0x00'
        sent = sock.sendto(heartmsg.encode(), server_address)
    else:
        print("no heartbeat")
        sock.close()


# sending IP to server
def handshake():
    conn = 'com-' + str(counter) + '=' + IPAddr
    sent = sock.sendto(conn.encode(), server_address)
    # Receive Connection
    data, server = sock.recvfrom(1024)
    dataresv = data.decode()
    print('{}'.format(data.decode()))
    data_spilt = data.decode().split('t ', 1)
    # checking protocol and IP Address
    if dataresv.startswith('com-0 accept') and socket.inet_aton(data_spilt[1]):
        accept = 'com-' + str(counter) + ' accept'
        # if OK sending accept to server
        sent = sock.sendto(accept.encode(), server_address)
        if not parser.getboolean('Max', 'Start'):
            global keep_a_live
            keep_a_live = parser.getboolean('Heartbeat', 'KeepALive')
            heartbeat()
            if parser.getint('Heartbeat', 'Time') == 3:
                msg_function()
            else:
                no_response_msg()

        else:
            keep_a_live = parser.getboolean('Heartbeat', 'KeepALive')
            heartbeat()
            maxpackage()
    else:
        # if NOT OK closing
        sent = sock.sendto('denied '.encode() + IPAddr.encode(), server_address)
        print('Connection Denied. Client closing')
        sock.close()
        exit()


def no_response_msg():
    while connection:
        data, server = sock.recvfrom(1024)
        dataresv = data.decode()
        if dataresv.startswith('con-res 0xFE'):
            print(dataresv)
            error_msg = 'con-res 0xFF'
            print("disconnected")
            sent = sock.sendto(error_msg.encode(), server_address)
            global keep_a_live
            keep_a_live = False
            sock.close()
            exit()


def msg_function():
    global count
    while connection:
        # Sending Message to Server
        message = input('\nmsg:')

        # Send data
        sendmsg = 'msg-' + str(count) + ' ' + message
        sent = sock.sendto(sendmsg.encode(), server_address)
        print(sendmsg)
        print('sending {} bytes to {}'.format(sent, server_address))
        count += 1
        # Receive response
        data, server = sock.recvfrom(1024)
        print('res-', count, '= {}'.format(data.decode()))
        count += 1


def maxpackage():
    global count
    while max_package:
        # loop to send amount from config file of msg to server
        for i in range(parser.getint('Max', 'MaxPackage')):
            sending = 'msg-' + str(count) + '= max'
            count += 2
            sent = sock.sendto(sending.encode(), server_address)
            # uses multiprocessing to send x of msg to server
            send_i = multiprocessing.Process(target=sock.sendto, args=(sending.encode(), server_address))
            send_i.start()
        # recieves response from server and closes client socket
        data, server = sock.recvfrom(1024)
        resv = data.decode()
        print(resv)
        global keep_a_live
        keep_a_live = False
        sock.close()
        break


handshake()
