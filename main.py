from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
from tkinter import *
import socket
import pickle


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print("hi")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content_len = int(self.headers.get('Content-Length'))
        message = self.rfile.read(content_len).decode('utf-8')
        objective = message[0:3]
        print(message)
        users = get_users()
        if objective == 'GR:':  # get report
            message2 = ''
            for x in range(0, len(users)):
                message2 = message2 + '|' + users[x][0] + '|' + users[x][1]
            self.wfile.write(bytes(message2, "utf-8"))
            self.wfile.close()
        if objective == 'SU:':  # sign up
            user = message[3:]
            for x in range(0, len(users)):
                if user == users[x][0]:
                    self.wfile.write(bytes(str(x) + '|' + str(users[x][1]), "utf-8"))
                    self.wfile.close()
                    break
                if x == len(users) - 1:
                    self.wfile.write(bytes(str(x) + '|' + '0', "utf-8"))
                    self.wfile.close()
                    users.append([user, '0'])
                    dbfile = open('userData.text', 'wb')
                    pickle.dump(users, dbfile)
                    dbfile.close()
            if len(users) == 0:
                self.wfile.write(bytes(str(0) + '|' + '0', "utf-8"))
                self.wfile.close()
                users.append([user, '0'])
                dbfile = open('userData.text', 'wb')
                pickle.dump(users, dbfile)
                dbfile.close()
        if objective == 'AP:':  # add points
            userNumber = int(message[3:message.find('|')])
            points = int(message[message.find('|') + 1:])
            users[userNumber][1] = points
            dbfile = open('userData.text', 'wb')
            pickle.dump(users, dbfile)
            dbfile.close()
        print(users)


def get_users():
    dbfile = open('userData.text', 'rb')
    users = pickle.load(dbfile)
    dbfile.close()
    return users


server_address = ('localhost', 9999)
httpd = HTTPServer(server_address, Server)
print("server started")
httpd.serve_forever()
