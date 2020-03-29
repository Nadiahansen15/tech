import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# variable that holds the recieved data and the address is comming from
data, address = sock.recvfrom(1024)

# accepts or deny the access - if denied, close server.
print('C: Com-0 < {} >'.format(data.decode()))
ipdata = data.decode().split('.', 3)
one, two, three, four = (int(ipdata[0])), (int(ipdata[1])), (int(ipdata[2])), (int(ipdata[3]))

if (0 <= one <= 255) and (0 <= two <= 255) and (0 <= three <= 255) and (0 <= four <= 255):
    sent = sock.sendto('accept < '.encode() + IPAddr.encode() + ' >'.encode(), address)
    print('S: Com-0 accept', '<', IPAddr, '>')
elif data:
    try:
        sent = sock.sendto('Connection Denied, closing server'.encode(), address)
    finally:
        sent = sock.sendto('Denied < '.encode() + IPAddr.encode() + ' >'.encode(), server_address)
        print('Connection Denied. Server closing')
        sock.close()
        exit()

data, address = sock.recvfrom(1024)
print('C: Com-0 {} '.format(data.decode()))
counter = 0
while True:
    data, address = sock.recvfrom(1024)
    print('C: msg-', counter, '=', data.decode())
    print('S: = received {} bytes from {}'.format(len(data), address))
    if data:
        counter += 1
        sent = sock.sendto('I am server'.encode(), address)
        print('S: res-', counter, '= sent {} bytes back to {}'.format(sent, address))
        counter += 1
    if b'exit' in data:
        try:
            print('close')
        finally:
            sock.close()
            exit()
