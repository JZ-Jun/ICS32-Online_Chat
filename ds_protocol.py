import time
import socket
import json
import ast
from collections import namedtuple
# Create a namedtuple to hold the values we expect to retrieve from json messages.


def extract_token(json_msg: str) -> str:
    '''
    Call the json.loads function on a json string and convert it to a string object
    '''
    try:
        json_obj = json.loads(json_msg)
        token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return token


def extract_type(json_msg: str) -> str:
    '''
    Call the json.loads function on a json string and convert it to a string object
    '''
    try:
        json_obj = json.loads(json_msg)
        type = json_obj['response']['type']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return type


def connect_server(server: str, port: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, port))
    return client


def join(client, username: str, password: str):
    msg = '{"join": {"username":' + '"' + username + '"' + ',"password":' + '"' + password + '", "token":""}}'
    client.sendall(msg.encode('utf-8'))
    srv_msg = client.recv(4096)
    decode_srv_msg = srv_msg.decode('utf-8')
    print("Response", decode_srv_msg)
    if extract_type(decode_srv_msg) == "error":
        return "error"
    elif extract_type(decode_srv_msg) == "ok":
        return extract_token(srv_msg.decode('utf-8'))


def post(client, token: str, message: str):
    convert_message=ast.literal_eval(message)
    msg = '{"token":' + '"' + token + '"' + ', "post": {"entry":"' + str(convert_message.get('entry')) + '", "timestamp": "'\
          + str(convert_message.get('timestamp')) + '"}}'
    client.sendall(msg.encode('utf-8'))
    srv_msg = client.recv(4096)


def bio(client, token: str, bio: str):
    msg = '{"token":' + '"' + token + '"' + ', "bio": {"entry":"' + bio + '", "timestamp": "' + str(
        time.time()) + '"}}'
    client.sendall(msg.encode('utf-8'))
    srv_msg = client.recv(4096)

