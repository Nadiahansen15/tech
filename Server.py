import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


def handshake():
    # variable that holds the recieved data and the address is coming from
    data, address = sock.recvfrom(1024)

    # accepts or deny the access - if denied, close server.
    print('{}'.format(data.decode()))
    dataresv = data.decode()
    data_spilt = data.decode().split('=', 1)
    # checking the IP address and protocol
    if "com-0" in dataresv and socket.inet_aton(data_spilt[1]):
        # if OK sending accept to client
        sent = sock.sendto('com-0 accept '.encode() + IPAddr.encode(), address)
        print('com-0 accept=' + IPAddr)
    elif data:
        # if NOT OK closing server
        try:
            sent = sock.sendto('Connection Denied, closing server'.encode(), address)

        finally:
            sent = sock.sendto('Denied '.encode() + IPAddr.encode(), server_address)
            print('Connection Denied. Server closing')
            sock.close()
            exit()
    # receiving accept from client and checking
    data, address = sock.recvfrom(1024)
    if 'com-0 accept' in data.decode():
        print('ready')
        first_msg()

# checking first message is nr. 0 message
def first_msg():
    msg, address = sock.recvfrom(1024)
    message = msg.decode()
    if 'msg-0' in message:
        send_msg(message, address)
        msg_function()
    else:
        sent = sock.sendto('not protocol '.encode() + IPAddr.encode(), server_address)

# send messages
def send_msg(insert_msg, insert_address):
    pre_counter = int(insert_msg[4])
    counter = int(insert_msg[4])+1
    # checking the count is i order
    if counter - pre_counter == 1 and 'msg-' in insert_msg:
        print(insert_msg)
        print('received {} bytes from {}'.format(len(insert_msg), insert_address))
        # respond client
        sent = sock.sendto('I am server'.encode(), insert_address)
        print('res-', counter, '= sent {} bytes back to {}'.format(sent, insert_address))


def msg_function():
    while True:
        # read client message
        msg, address = sock.recvfrom(1024)
        # checking client message
        send_msg(msg.decode(), address)
        # if client sends exit, close socket.
        if b'exit' in msg:
            try:
                print('close')
            finally:
                sock.close()
                exit()


handshake()
