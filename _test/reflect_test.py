class Cat:
    def __init__(self):
        self.name='cat'
        print('Cat')

class CallCat:
    def __init__(self):
        self.c = eval('Cat')()

call = CallCat()
print('')