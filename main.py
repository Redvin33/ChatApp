from tkinter import*
from _thread import*


import socket
import json

host = 'localhost'
port = 55555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
#Initializes default values to JSON message
message = { "channel" : "chat", "msg" : "", "command" : ""}
chatrooms = []



class chatroom:
    def __init__(self, channel):
        self.__window = Tk()
        self.__window.title(channel)
        self.__chat = Listbox(self.__window, bg ="#fff", width=100, height=40)
        self.__userlist = Listbox(self.__window, bg = "#fff", width=15, height=40)
        self.__channel = channel
        self.__scroll = Scrollbar(self.__window)


        self.__text_entry = Entry(self.__window, width = 20, text="" )
        self.__send_button = Button(self.__window, text="SEND", command = self.send)

        self.__chat.config(yscrollcommand = self.__scroll.set)
        self.__scroll.config(command=self.__chat.yview)

        #construction of TkInter grid
        self.__chat.grid( row=1, column=1, rowspan=4, columnspan=4 )
        self.__text_entry.grid( row=5, column=1 )
        self.__send_button.grid( row=5, column=2 )
        self.__userlist.grid(row=1, column=6, rowspan=4, columnspan= 2, padx= 20)
        self.__scroll.grid(row=1, column=5, rowspan=4)
        chatrooms.append(self)
        if len(chatrooms) == 1:
            start_new_thread(connection, ())

        #Sends server request to update channels userlist
        message["command"] = "userlist"
        message["channel"] = self.__channel

        s.send(json.dumps(message).encode('utf-8'))


        self.__window.protocol("WM_DELETE_WINDOW", self.deletewindow)

        self.__window.mainloop()

    #If window is closed, tells server that client disconnected from that channel
    def deletewindow(self):

        message["command"] = "userlist"
        message["channel"] = self.__channel
        message["msg"] = "remove"
        s.send(json.dumps(message).encode('utf-8'))
        chatrooms.remove(self)
        self.__window.destroy()

    def send(self):
        text = self.__text_entry.get()
        message["command"] = ""
        if text[0] == "/":
            message["command"] = text.split(' ')[0]
            message["channel"] = text.split(' ')[1]

            packet = json.dumps(message)
            s.send(packet.encode('utf-8'))
            self.__text_entry.delete(0, END)
            chatroom(message["channel"])
            return
        else:
            message["channel"] = self.__channel
            message["msg"] = text

        packet = json.dumps(message)
        s.send(packet.encode('utf-8'))
        message["command"] = ""
        self.__text_entry.delete(0, END)
        return

    def receive(self, mesg):
        self.__chat.insert(END, mesg)
        self.__chat.see("end")

    def getChannel(self):
        return self.__channel

    def updateuserlist(self, userlist):
        self.__userlist.delete(0, END)
        for user in userlist:
            self.__userlist.insert(END, user)
        return



def connection():

    while 1:
        rcv = s.recv(2048).decode('utf-8')
        msg = json.loads(rcv)

        for chat in chatrooms:
            if msg["channel"] == chat.getChannel():
                if msg["command"] == "userlist":
                    chat.updateuserlist(msg["msg"])
                else:
                    chat.receive(msg["msg"])


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
        s.send(channel.encode('utf-8'))
        chatroom(channel)

login_window()
