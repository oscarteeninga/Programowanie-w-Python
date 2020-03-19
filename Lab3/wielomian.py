def chain(*iterables):
    # chain('ABC', 'DEF') --> A B C D E F
    for it in iterables:
        for element in it:
            yield element

def repeat(object, times=None):
    # repeat(10, 3) --> 10 10 10
    if times is None:
        while True:
            yield object
    else:
        for i in range(times):
            yield object

def zip_longest(*args, fillvalue=None):
    # zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
    def sentinel(counter = ([fillvalue]*(len(args)-1)).pop):
        yield counter()         # yields the fillvalue, or raises IndexError
    fillers = repeat(fillvalue)
    iters = [chain(it, sentinel(), fillers) for it in args]
    try:
        for tup in zip(*iters):
            yield tup
    except IndexError:
        pass

class Wielomian:
    wspol = []
    def __init__(self, *args, **kwargs):
        self.wspol = args

    def __str__(self):
        return f"Wielomian {self.wspol}"
    def __add__(self, other):
        if type(other) != Wielomian:
            print("Podano nie wielomian")
            pass
        else:
            self.wspol = list(zip_longest(self.wspol, other.wspol, fillvalue=+0))


W = Wielomian(1, 2, 3)
W2 = Wielomian(2, 3, 4)
W + W2
print(W)