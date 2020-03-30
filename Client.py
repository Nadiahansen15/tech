import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is: " + IPAddr)
server_address = ('localhost', 10000)
counter = 0


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
    if 'com-0 accept' in dataresv and socket.inet_aton(data_spilt[1]):
        accept = 'com-' + str(counter) + ' accept'
        # if OK sending accept to server
        sent = sock.sendto(accept.encode(), server_address)
        send()
    elif data:
        # if NOT OK closing
        sent = sock.sendto('denied '.encode() + IPAddr.encode(), server_address)
        print('Connection Denied. Client closing')
        sock.close()
        exit()


def send():
    count = 0
    while True:
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
        if message == 'exit':
            try:
                print('close')
            finally:
                sock.close()
                exit()


handshake()
