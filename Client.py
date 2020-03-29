import socket
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is: " + IPAddr)
server_address = ('localhost', 10000)
counter = 0
sent = sock.sendto(IPAddr.encode(), server_address)
# Receive Connection
data, server = sock.recvfrom(1024)
print('C: Com-0 <', IPAddr, '> ')
print('S: Com-0 {}'.format(data.decode()))
if b'accept' in data:
    sent = sock.sendto('accept < '.encode() + IPAddr.encode() + ' >'.encode(), server_address)
    print('C: Com-0 accept <', IPAddr, '>')
elif data:
    sent = sock.sendto('denied < '.encode() + IPAddr.encode() + ' >'.encode(),server_address)
    print('Connection Denied. Client closing')
    sock.close()
    exit()

while True:
    # Sending Message to Server
    message = input('\nmsg:')
    # Send data
    print('C: msg-', counter, '= {!r}'.format(message))
    sent = sock.sendto(message.encode(), server_address)
    print('C: sending {} bytes to {}'.format(sent, server_address))
    counter += 1
    # Receive response
    data, server = sock.recvfrom(1024)
    print('S: res-', counter, '= {}'.format(data.decode()))
    counter += 1
    if message == 'exit':
        try:
            print('close')
        finally:
            sock.close()
            exit()
