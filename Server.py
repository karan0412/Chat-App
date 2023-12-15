# Karan Parmar- S11198967
# Savindya Merisha Fernando- S11199815
# Prashant Sharma- S11195863
import socket
import threading


HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
PORT = 49776  # Arbitrary non-privileged port

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to a specific address and port
server.bind((HOST, PORT))

# Listen for incoming connections
server.listen(1)
clients = []
usernames = []


#def sendClientList():
        #client_list = str(clients)
        #for username in usernames:
            #username.send(bytes(client_list, "utf-8"))



def broadcast(message):
    for client in clients:
        client.send(message)


def hande_client(client):

    #sendClientList()
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{usernames} has left the chat room!'.encode('utf-8'))
            usernames.remove(username)
            #sendClientList()
            break

def receive_message():
    while True:
        print('Server is running and listening ... ')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('username?' .encode('utf-8'))
        username = client.recv(1024)
        usernames.append(username)
        clients.append(client)
        print(f'the nickname of this client is {username}'.encode('utf-8'))
        broadcast(f'{username} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=hande_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive_message()



