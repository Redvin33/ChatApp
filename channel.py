class channel:
    def __init__(self, user):
        self.__users = []
        self.__users.append(user)

    def addUser(self, user):
        self.__users.append(user)

    def users(self):
        return self.__users

alist = list(map(lambda x: x*x, [1, 5]))
print(alist)