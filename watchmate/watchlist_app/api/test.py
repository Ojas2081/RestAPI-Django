# # class Person:
# #     __name = 'Ojas'

# #     def showName(self):
# #         return f"name is {self.__name}"


# # p = Person()
# # # print(p.__name)
# # print(p.showName())

# x = 5


# def function1(x, *args):
#     print("args : ", args)
#     return x


# print("value of from local scope ", function1(9, 10, 11))

def is_Prime(num):
    if num < 0:
        return False
    elif num == 1:
        return False
    else:
        for i in range(2, (num//2)+1):
            if num % i == 0:
                return False
        return True


for i in range(1, 51):
    print(is_Prime(i))
