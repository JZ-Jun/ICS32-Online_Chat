import socket
import json, time


class DSUProtocolError(Exception):
    """
    Custom DSU error that helps catch incorrect inputs or error responses from the server.
    """
    pass


class DirectMessage:
    """
    The DirectMessage class is responsible for working with individual messages.
    It currently supports getters and setters for all of the attributes.
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for DirectMessage object.

        :param recipient: sender or reciever of DirectMessage
        :param message: the message being sent or received from DS server
        :param timestamp: time when the message was sent
        :type recipient: str (default None)
        :type message: str (default None)
        :type timestamp: float
        
        """
        self.recipient = None
        self.message = None
        self.timestamp = time.time()


    def set_recipient(self, rec:str) -> None:
        """
        Setter method that changes the recipient.

        :param rec: new recipient 
        :type rec: str
        """
        self.recipient = rec


    def get_recipient(self) -> str:
        """
        Getter method that returns the recipient.

        :return: recipient attr of the DirectMessage
        :rtype: str
        """
        return self.recipient


    def set_message(self, msg:str) -> None:
        """
        Setter method that changes the message.

        :param msg: new message
        :type msg: str
        """
        self.message = msg


    def get_message(self) -> str:
        """
        Getter method that returns message.

        :return: message attr of the DirectMessage
        :rtype: str
        """
        return self.message


    def set_time(self, time:float) -> None:
        """
        Setter method that changes the time.

        :param time: new timestamp from time library
        :type time: float
        """
        self.timestamp = time


    def get_time(self) -> float:
        """
        Getter method that returns time.

        :return: time attr of the DirectMessage
        :rtype: float
        """
        return self.timestamp


class DirectMessenger:
    """
    The DirectMessenger class exposes the properties required to send direct messages to the
    DS Server. This class implements similar functionality to the ds_protocol and connects to
    the server using sockets.

    When creating a program, you can use the DirectMessenger with attr username and password
    to establish a connection and send messages. It also has functionality to retrieve new and
    all messages directed towards the user specified in the initialization signature.
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Constructs all the necessary attributes for the DirectMessenger object.

        :param dsuserver: server to connect to (auto set to ICS 32 DS server)
        :param username: username to connect with DS server
        :param password: password for the username
        :type dsuserver: str
        :type username: str
        :type password: str
        
        """
        self.token = None
        self.dsuserver = '168.235.86.101'
        self.username = username
        self.password = password
		
    def send(self, message:str, recipient:str) -> bool:
        """
        Sends a DirectMessage to the DS server.

        :param message: message wanting to be sent
        :param recipient: person you are sending the message to
        :type message: str
        :type recipient: str
        :return: true if message successfully sent, false if send failed.
        :rtype: bool
        """
        try:
            #establishes connection and sends a join message for token
            self.connect()
            self.join()
            
            dm = DirectMessage()
            dm.set_recipient(recipient)
            dm.set_message(message)

            x = {
                "token": self.token,
                "directmessage": {
                    "entry": dm.get_message(),
                    "recipient": dm.get_recipient(),
                    "timestamp": dm.get_time()
                    }
                }
            send_msg = json.dumps(x)
            self.writeCom(send_msg)
            resp = self.response()
            #disconnects from the server (closes sockets)
            self.disconnect()
            
            if resp["response"]["type"] == 'ok':
                return True
            else:
                return False
        except DSUProtocolError as dse:
            print(dse)


    def retrieve_new(self) -> list:
        """
        Retrieves all the new messages from the DS Server and converts them to DirectMessage objects.

        :return: returns a list of DirectMessage objects containing all new messages
        :rtype: list
        """
        try:
            #establishes connection and sends a join message for token
            self.connect()
            self.join()
            response_list = []

            x = {
                "token": self.token,
                "directmessage": "new"
                }
            retrieve_msg = json.dumps(x)
            self.writeCom(retrieve_msg)
            resp = self.response()

            #loops through response list and creates DirectMessage objects with provide attr
            for msgs in resp["response"]["messages"]:
                dm = DirectMessage()
                dm.set_message(msgs["message"])
                dm.set_recipient(msgs["from"])
                dm.set_time(msgs["timestamp"])

                response_list.append(dm)

            #disconnects from the server (closes sockets)
            self.disconnect()
            return response_list
        except DSUProtocolError as dse:
            print(dse)
            
        
 
    def retrieve_all(self) -> list:
        """
        Retrieves all the messages from the DS Server and converts them to DirectMessage objects.

        :return: returns a list of DirectMessage objects containing all messages
        :rtype: list
        """
        try:
            #establishes connection and sends a join message for token
            self.connect()
            self.join()
            response_list = []

            x = {
                "token": self.token,
                "directmessage": "all"
                }
            retrieve_msg = json.dumps(x)
            self.writeCom(retrieve_msg)
            resp = self.response()

            #loops through response list and creates DirectMessage objects with provide attr
            for msgs in resp["response"]["messages"]:
                dm = DirectMessage()
                dm.set_message(msgs["message"])
                dm.set_recipient(msgs["from"])
                dm.set_time(msgs["timestamp"])

                response_list.append(dm)

            #disconnects from the server (closes sockets)
            self.disconnect()
            return response_list
        except DSUProtocolError as dse:
            print(dse)


    def join(self) -> None:
        """
        Sends a join message to the DS Server to get the token for retrieve, send functions.

        :raises DSUProtocolError: custom error for failed connections
        """
        try:
            x = {
                "join": {
                    "username": self.username,
                    "password": self.password,
                    "token": ""
                    }
                }
            join_msg = json.dumps(x)
            self.writeCom(join_msg)
            resp = self.response()

            #makes sure a response is given from the server
            if resp is not None:
                self.token = resp["response"]["token"]
        except:
            raise DSUProtocolError("an error occurred while connecting")
        

    def connect(self) -> None:
        """
        Makes initial connection with the DS Server using sockets.

        :raises DSUProtocolError: custom error for failed connections
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dsuserver, 3021))

            self.f_send = sock.makefile('w')
            self.f_recv = sock.makefile('r')
        except:
            raise DSUProtocolError("an error occurred while connecting")


    def disconnect(self) -> None:
        """
        Disconnects the user from the server by closing the sockets.
        """
        self.f_send.close()
        self.f_recv.close()


    def writeCom(self, msg:str) -> None:
        """
        Abstracted function that writes the json message to the server.

        :param msg: json message to send to DS server
        :type msg: str
        :raises DSUProtocolError: custom error for failed connections
        """
        try:
            self.f_send.write(msg + '\n')
            self.f_send.flush()
        except:
            raise DSUProtocolError("an error occurred while connecting")


    def response(self) -> dict:
        """
        Abstracted function that takes responses from the server

        :raises DSUProtocolError: custom error for failed connections
        :return: dictionary conversion of json message response
        :rtype: dict
        """
        try: 
            resp = self.f_recv.readline()[:-1]

            self.resp_msg = json.loads(resp)

            #prints response to the console
            if "message" in self.resp_msg["response"]:
                print(self.resp_msg["response"]["message"])
            elif len(self.resp_msg["response"]["messages"]) > 1:
                #only shows the last message (for simplicity in console)
                print('...', self.resp_msg["response"]["messages"][-1])
            else:
                print(self.resp_msg["response"]["messages"])

            if self.resp_msg["response"]["type"] == 'error':

                #print(self.resp_msg["response"]["message"])
                self.disconnect()
                raise DSUProtocolError
            else:
                return self.resp_msg
        except:
            raise DSUProtocolError("an error occurred while connecting")

"""
Practice Test
if __name__ == '__main__':
    dm1 = DirectMessenger('168.235.86.101', 'harry123123', '123')
    dm1.send('ok then', 'abigail9009')
    print(dm1.retrieve_all()[0].get_message())
"""
