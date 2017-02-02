from tkinter import*
from _thread import*

import socket
import json

host = 'localhost'
port = 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
#Initializes default values to JSON message
message = { "channel" : "chat", "msg" : "", "command" : ""}


class chatroom:
    def __init__(self, channel):
        self.__window = Tk()
        self.__window.title(channel)
        self.__chat = Label(self.__window, bg ="#fff", width=30, height=40, pady=20, text="", justify=LEFT)
        self.__channel = channel

        self.__text_entry = Entry(self.__window, width = 20, text="" )
        self.__send_button = Button(self.__window, text="SEND", command = self.send)
        self.__send = False

        #construction of TkInter grid
        self.__chat.grid( row=1, column=1, rowspan=4, columnspan=4 )
        self.__text_entry.grid( row=5, column=1 )
        self.__send_button.grid( row=5, column=2 )

        s.send(channel.encode('utf-8'))
        start_new_thread(self.connection, ())
        self.__window.mainloop()

    def send(self):
        text = self.__text_entry.get()
        if text[0] == "/":
            message["command"] = text.split(' ')[0]
            message["channel"] = text.split(' ')[1]
            chatroom(message["channel"])
        else:
            message["channel"] = self.__channel
            message["msg"] = text

        packet = json.dumps(message)
        s.send(packet.encode('utf-8'))
        return

    def receive(self, mesg):
        self.__chat.configure(text = self.__chat.cget("text") + mesg + "\n", anchor ="w")


    def connection(self):
        print("Connected to " + self.__channel + ".")

        while 1:
            rcv = s.recv(2048).decode('utf-8')
            msg = json.loads(rcv)
            if msg["channel"] == self.__channel:
                self.receive(msg["msg"])


class login_window:
    def __init__(self):
        self.__window = Tk()
        self.__nickname_text = Label( self.__window, text = "Choose nickname: " )
        self.__nickname_entry = Entry( self.__window, width = 15 )
        self.__channel_text = Label( self.__window, text="Channel: " )
        self.__channel = Entry( self.__window, width =15)
        self.__login_button = Button( text="LOGIN", command = self.login )

        #construction of TkInter grid
        self.__nickname_text.grid( row =1, column = 1 )
        self.__nickname_entry.grid( row = 1, column = 2 )
        self.__channel_text.grid(row=2, column = 1)
        self.__channel.grid( row =2, column=2 )
        self.__login_button.grid( row= 3, column = 2 )

        self.__window.mainloop()

    def login(self):
        nickname = self.__nickname_entry.get()
        channel = self.__channel.get()
        self.__window.destroy()
        s.send(nickname.encode('utf-8'))
        chatroom(channel)


login_window()
