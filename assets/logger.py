class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super(Singleton, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instance


class Logger(metaclass=Singleton):
    def __init__(self):
        self.log_message = "Logger initialized!\n"
        self.counter = 0

    def log(self, message):
        self.log_message += " " + message + "\n"

    def count(self):
        self.counter += 1

    def count_return(self):
        return self.counter
