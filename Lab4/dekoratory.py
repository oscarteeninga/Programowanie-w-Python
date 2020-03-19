import time
import array

def debug(fun):
    print("Init:\t\tZadeklarowano debug.")
    def wrapper():
        t = time.time()
        fun()
        print("Time:\t", time.time() - t)
    return wrapper

def silence(fun, array):
    def wrapper():
        try:
            fun()
            if (type(array) != type([])):
                raise ValueError("ValueError")
        except ValueError as a:
            print(a, ":\tParametr powinien być listą!")
        except tuple(array) as a:
            print(a,":\tWyjątek obsłuzony.")
    return wrapper

@debug
def Foo():
    print("Message:\tHello")
    raise KeyError("KeyError")

Foo = silence(Foo, [TypeError, KeyError])

Foo()
