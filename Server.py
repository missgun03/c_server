import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

clients = {}

s.bind((ip, port))
s.listen()
print('Server Ready...')
print('Ip Address of the Server::%s'%ip)

def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = 'There are four commands in Messenger\n1::@chatlist=>gives you the list of the people currently online\n2::@quit=>To end your session\n3::@broadcast=>To broadcast your message to each and every person currently present online\n4::Add the name of the person at the end of your message preceded by @ to send it to particular person'

    while clientConnected:
        try:
            msg = client.recv(1024).decode('utf-8')
            response = 'Number of People Online\n'
            found = False
            if '@chatlist' in msg:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) +'::' + name+'\n'
                client.send(response.encode('utf-8'))
            elif '@help' in msg:
                client.send(help.encode('utf-8'))
            elif '@all' in msg:
                msg = msg.replace('@all','')
                for k,v in clients.items():
                    v.send(msg.encode('utf-8'))
            elif '@quit' in msg:
                response = 'Stopping Session and exiting...'
                client.send(response.encode('utf-8'))
                clients.pop(uname)
                print(uname + ' has been logged out')
                clientConnected = False
            else:
                for name in keys:
                    if('@'+name) in msg:
                        msg = msg.replace('@'+name, '')
                        clients.get(name).send(msg.encode('utf-8'))
                        found = True
                if(not found):
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
        except:
            clients.pop(uname)
            print(uname + ' has been logged out')
            clientConnected = False


        


while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('utf-8')
    print('%s connected to the server'%str(uname))
    client.send('Welcome to Messenger. Type @help to know all the commands'.encode('ascii'))
    
    if(client not in clients):
        clients[uname] = client
        threading.Thread(target = handleClient, args = (client, uname, )).start()
        
    