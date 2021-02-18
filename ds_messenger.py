class DirectMessage:
    def __init__(self):
        recipient = None
        message = None
        timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        token = None

    def send(self, message: str, recipient: str) -> bool:
        pass

    def retrieve_new(self) -> DirectMessage:
        pass

    def retrieve_all(self) -> list:
        pass

print("Hello World test test")