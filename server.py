import socket
from _thread import*

host = 'localhost'
port = 7777
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = {}


def client_thread(conn, channel):
    for user in connections:
        if connections[user][1] == channel:
            user.sendall(str.encode(connections[conn][0] + " has joined the room." +"\n" ))

    conn.send(str.encode("Welcome " + connections[conn][0] + "\n"))

    while True:
        try:
            data = conn.recv(2048).decode('utf-8')
            reply = connections[conn][0] + ": " + data
            for user in connections:
                if connections[user][1] == channel:
                    user.sendall(str.encode(reply))

        except:
            print(connections[conn][0] + " has disconnected")
            del connections[conn]
            break

    conn.close()


def main():
    print("Waiting for a connection.")

    try:
        ss.bind((host, port))
    except socket.error as e:
        print(str(e))

    ss.listen(5)

    while True:
        conn, addr = ss.accept()
        nickname = conn.recv(2048).decode('utf-8')
        chan = conn.recv(2048).decode('utf-8')
        connections[conn] = nickname, chan
        print("connected to: " + str(addr[0]) + ":" + str(addr[1]))
        start_new_thread(client_thread, (conn, chan))

main()