from socket import *
import ssl
import base64
import time

# Get an input username and password from the user
# email = os.environ['EMAIL']
# password = os.environ['PASSWORD']
email = input('Email: ')
password = input('Password: ')
to = input('Send to: ')
# Create the openssl client socket
# Connect it to the specified mailserver on the given port
client = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))
client.connect(('smtp.gmail.com', 465))
BYTE_LENGTH = 1024
# Retrieve data from the client
recv = client.recv(BYTE_LENGTH).decode()
# Get the frist three characters from the recv message which indicate the status
status = recv[:3]
# Check for 220: Service ready, status code from the SMTP server
if status != '220':
    print('220 reply not received from server.')

## HELO ##
helo_msg = 'HELO Gmail\r\n'.encode()
client.send(helo_msg)
helo_recv = client.recv(BYTE_LENGTH).decode()
status = helo_recv[:3]
print(helo_recv)
# Status code 250: Requested mail action okay, completed
if status != '250':
    print('250 reply not received from server.')

## Authentication ##
base64_str = base64.b64encode(("\x00" + email + "\x00" + password).encode())
auth_msg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
client.send(auth_msg)
auth_recv = client.recv(BYTE_LENGTH).decode()
print(auth_recv)

## Message ##
# From
email_from = "MAIL FROM:<" + email + ">\r\n"
client.send(email_from.encode())
from_recv = client.recv(BYTE_LENGTH).decode()
print(from_recv)
# To
email_to = "RCPT TO:<" + to + ">\r\n"
client.send(email_to.encode())
to_recv = client.recv(BYTE_LENGTH)
to_recv = to_recv.decode()
print(to_recv)
# Data
message = "DATA\r\n"
client.send(message.encode())
message_recv = client.recv(BYTE_LENGTH)
message_recv = message_recv.decode()
print(message_recv)
# Subject
subject = "Subject: Hello!\r\n\r\n"
client.send(subject.encode())
date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
date = date + "\r\n\r\n"
client.send(date.encode())
# Message
msg = "\r\n Hello There!"
client.send(msg.encode())
client.send("\r\n.\r\n".encode())
msg_recv = client.recv(BYTE_LENGTH).decode()
print(msg_recv)
# Quit
quit = "QUIT\r\n"
client.send(quit.encode())
quit_recv = client.recv(BYTE_LENGTH)
print(quit_recv.decode())
client.close()