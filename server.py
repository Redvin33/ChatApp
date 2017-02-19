import socket
import json
from channel import Channel
from _thread import*

host = 'localhost'
port = 7777
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = {}
channels = {}


def client_thread(conn):

    try:
        while True:

            packet = conn.recv(2048).decode('utf-8')
            msg = json.loads(packet)
            reply = connections[conn] + ": " + msg["msg"]
            print(msg)
            if msg["command"] == "/join":
                chan = msg["channel"]
                if chan not in channels.keys():
                    channels[chan] = Channel(conn, connections[conn])
                    print("Channel " + chan + " created." )
                else:
                    channels[chan].addUser(conn, connections[conn])
                continue

            for chan in channels:
                if msg["channel"] == chan:
                    for user in channels[chan].users():
                        msg["msg"] = reply
                        mesg = json.dumps(msg)
                        user.sendall(mesg.encode('utf-8'))

    except error as e:
        print(e)
        for channel in channels:
            channels[channel].removeUser(conn, channel)
        print(connections[conn][0] + " has disconnected")
        del connections[conn]
        conn.close()
        return




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
        if chan not in channels.keys():
            channels[chan] = Channel(conn, nickname)
        else:
            channels[chan].addUser(conn, nickname)
        connections[conn] = nickname
        print("connected to: " + str(addr[0]) + ":" + str(addr[1]))
        msg = {}
        msg["msg"] = channels[chan].UserNames()
        msg["command"] = "userlist"
        print(msg)
        mesg = json.dumps(msg)
        conn.sendall(mesg.encode('utf-8'))
        start_new_thread(client_thread, (conn,))

main()