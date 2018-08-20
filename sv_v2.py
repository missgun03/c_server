
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from winsound import *


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("สวัสดี นี่คือระบบจำลองการสนทนา กรุณาใสชื่อแล้วกด Enter", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'ยินดีต้อนรับ %s! ถ้าคุณต้องการออกจากการสนทนา, ใส่ {quit} เพื่อออก.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s ได้เข้าร่วมการสนทนา!" % name
    broadcast(bytes(msg, "utf8"))
    keys = clients.keys()
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")

        # elif msg == bytes('@'+name, "utf8"):
        #     # msg = msg.replace('@' + name, '')
        #     whis(msg, name + ": ")
        #     found = True
        #     if (not found):
        #         client.send('Trying to send message to invalid person.'.encode('utf-8'))
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s ได้ออกจากการสนทนา." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def whis(msg, prefix=""):

        clients.send(bytes(prefix, "utf8") + msg)

clients = {}
addresses = {}

HOST = ''
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()