import ds_protocol

'''
 The send function joins a ds server and sends a message, bio, or both

 :param server: The ip address for the ICS 32 DS server.
 :param port: The port where the ICS 32 DS server is accepting connections.
 :param username: The user name to be assigned to the message.
 :param password: The password associated with the username.
 :param message: The message to be sent to the server.
 :param bio: Optional, a bio for the user.
 '''


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None):
    client = ds_protocol.connect_server(server, port)
    response = ds_protocol.join(client, username, password)
    if response != "error":
        ds_protocol.post(client, response, message)
        ds_protocol.bio(client, response, bio)
    pass


def verify(server: str, port: int, username: str, password: str):
    client = ds_protocol.connect_server(server, port)
    response = ds_protocol.join(client, username, password)
    if response == "error":
        return True
    return False


# send("168.235.86.101", 2021, "Jun", "password123", "Hahaha", "I am Issac")
def test()
   send("168.235.86.101", 2021, "Jun", "password123", "Hahaha", "I am Issac")
