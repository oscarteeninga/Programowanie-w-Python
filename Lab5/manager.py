class Opener():
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print("opening...")
        self.file = open(self.filename, 'w+')
        return self
    
    def __exit__(self, *args):
        print("closing...")
        self.file.close()

    def write(self, text):
        print("writing...")
        print("text: " + text)
        self.file.write(text)

    def read(self):
        print("read: ")
        for i in self.file:
            print(i)

    def boom(self):
        raise ValueError

