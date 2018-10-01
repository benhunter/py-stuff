# https://web.archive.org/web/20060612061259/http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html

'''
Singleton pattern. Use of singleton is driven by shared state. See also Borg pattern. Also note that modules are effectively singletons.
'''


class Singleton(object):
    '''
    Only one instance of the class can be instantiated.
    '''
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class ChildOfSingleton(Singleton):
    pass


c = ChildOfSingleton()
d = ChildOfSingleton()

id(c)
id(d)


class Borg:
    '''
    All Borg objects share the same symbol table of writable attributes, __dict__

    Note: Borg has issues with 'new style' classes, aka class Name(object): instead of class Name():
    '''
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
    # and whatever else is needed in the class
