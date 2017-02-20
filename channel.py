

class Channel:

    def __init__(self, user, nick, name):
        self.__users = {}
        self.__users[user] = nick
        self.name = name

    def adduser(self, user, nick):
        self.__users[user] = nick

        return

    def usernames(self):
        return list(self.__users.values())

    def users(self):
        return list(self.__users.keys())

    def removeuser(self, user):
        del self.__users[user]
        return
