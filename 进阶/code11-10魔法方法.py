class User():
    def __init__(self, name) -> None:
        print( "User.__init__")
        self.__name__ = name
    
    def __str__(self) -> str:
        return self.__name__ 
    
    def __add__(self, b):
        return self.__name__ + "." + b.__name__
    def __eq__(self, value: object) -> bool:
        return self.__name__ == value.__name__
    
if __name__ == '__main__':
    jack = User('jack')
    print(jack.__dict__)
    print(str(jack))
    
    marry = User('marry')
    print(jack+marry)
    
    marry1 = User('marry')
    print(marry1 == marry)