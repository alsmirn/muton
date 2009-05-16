class Test(object):
    __slots__ = ('x', 'y')
    x = 10
    
    def __init__(self, *args, **kwargs):
        y = 2

inst = Test()
print inst.x

inst.x = 100
print inst.x