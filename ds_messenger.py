import socket
import json, time
from collections import namedtuple

class DSUProtocolError(Exception):
    pass


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = time.time()

    def set_recipient(self, rec:str) -> None:
        self.recipient = rec

    def get_recipient(self) -> str:
        return self.recipient

    def set_message(self, msg:str) -> None:
        self.message = msg

    def get_message(self) -> str:
        return self.message

    def set_time(self, time:float):
        self.timestamp = time

    def get_time(self) -> float:
        return self.timestamp


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = '168.235.86.101'
        self.username = username
        self.password = password
		
    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
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

        self.disconnect()
        
        if resp["response"]["type"] == 'ok':
            return True
        else:
            return False


    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
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

        for msgs in resp["response"]["messages"]:
            dm = DirectMessage()
            dm.set_message(msgs["message"])
            dm.set_recipient(msgs["from"])
            dm.set_time(msgs["timestamp"])

            response_list.append(dm)
	
	self.disconnect()
        return response_list
            
        
 
    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
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

        for msgs in resp["response"]["messages"]:
            dm = DirectMessage()
            dm.set_message(msgs["message"])
            dm.set_recipient(msgs["from"])
            dm.set_time(msgs["timestamp"])

            response_list.append(dm)
	
	self.disconnect()
        return response_list
        

    def join(self):
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
        if resp is not None:
            self.token = resp["response"]["token"]
        

    def connect(self) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dsuserver, 3021))

            self.f_send = sock.makefile('w')
            self.f_recv = sock.makefile('r')
        except:
            raise DSUProtocolError


    def disconnect(self) -> None:
        self.f_send.close()
        self.f_recv.close()


    def writeCom(self, msg:str) -> None:
        try:
            self.f_send.write(msg + '\n')
            self.f_send.flush()
        except:
            raise DSUProtocolError


    def response(self) -> dict:
        resp = self.f_recv.readline()[:-1]

        resp_msg = json.loads(resp)
        print(resp_msg)

        if resp_msg["response"]["type"] == 'error':

            print(resp_msg["response"]["message"])
            self.disconnect()
            raise DSUProtocolError
        else:
            return resp_msg

if __name__ == '__main__':
    dm1 = DirectMessenger('168.235.86.101', 'abigail9009', '123')
    dm1.send('hello bird', 'abigail9009')
    print(dm1.retrieve_all()[0].get_message())

    
