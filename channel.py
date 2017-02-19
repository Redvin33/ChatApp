import json

class Channel:

    def __init__(self, user, nick):
        self.__users = {}
        self.__users[user] = nick

    def addUser(self, user, nick):
        self.__users[user] = nick
        return

    def UserNames(self):
        return list(self.__users.values())


    def users(self):
        return list(self.__users.keys())

    def removeUser(self, user, channel):
        try:
            del self.__users[user]
            for user in self.__users:
                mesg = {}
                mesg["msg"] = self.__users[user] + "has disconnected."
                mesg["channel"] = channel
                msg = json.dumps(mesg)
                user.sendall(msg.encode('utf-8'))
        except:
            return

        return