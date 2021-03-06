import socket
import json
from channel import Channel
from _thread import*

host = 'localhost'
port = 55555
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = {}
channels = {}


def disconnectmsg(chan, conn):
    for user in channels[chan].users():
        msg = {}
        msg["command"] = ""
        msg["channel"] = chan
        msg["msg"] = connections[conn] + " has disconnected"
        mesg = json.dumps(msg)
        user.sendall(mesg.encode('utf-8'))
    return



def UpdateUserlist(chan):
    msg= {}
    msg["channel"] = chan.name
    msg["msg"] = chan.usernames()
    msg["command"] = "userlist"
    mesg = json.dumps(msg)

    for user in chan.users():
        user.sendall(mesg.encode('utf-8'))

def client_thread(conn):

    try:

        while True:

            packet = conn.recv(2048).decode('utf-8')
            msg = json.loads(packet)
            reply = connections[conn] + ": " + msg["msg"]

            if msg["command"] == "userlist":
                if msg["msg"] == "remove":
                    channels[msg["channel"]].removeuser(conn)
                    if len(channels[msg["channel"]].users()) == 0:
                        del channels[msg["channel"]]
                        continue
                    disconnectmsg(msg["channel"], conn)
                UpdateUserlist(channels[msg["channel"]])
                continue

            elif msg["command"] == "/join":
                chan = msg["channel"]
                if chan not in channels.keys():
                    channels[chan] = Channel(conn, connections[conn], chan)
                    print("Channel " + chan + " created." )

                else:
                    channels[chan].adduser(conn, connections[conn])

                UpdateUserlist(channels[chan])

                continue

            else:
                for chan in channels:
                    if msg["channel"] == chan:
                        for user in channels[chan].users():
                            msg["msg"] = reply
                            mesg = json.dumps(msg)
                            user.sendall(mesg.encode('utf-8'))

    except:
        print(connections[conn] + " has disconnected")
        del connections[conn]
        conn.close()
        return




def main():
    print("Waiting for a connection.")

    try:
        ss.bind((host, port))
    except socket.error as e:
        print(str(e))
        exit()

    ss.listen(16)

    while True:
        conn, addr = ss.accept()
        nickname = conn.recv(2048).decode('utf-8')
        chan = conn.recv(2048).decode('utf-8')
        if chan not in channels.keys():
            channels[chan] = Channel(conn, nickname, chan)

        else:
            channels[chan].adduser(conn, nickname)

        connections[conn] = nickname

        print("connected to: " + str(addr[0]) + ":" + str(addr[1]))
        start_new_thread(client_thread, (conn,))


main()