class Singleton:
    """
    Singleton pattern realisation
    """
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


class CallSingleton(Singleton):
    def __init__(self):
        self._call = lambda: None

    def __call__(self):
        self._call()
