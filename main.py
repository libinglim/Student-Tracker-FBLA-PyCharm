from http.server import BaseHTTPRequestHandler, HTTPServer
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
        users = get_users();

        dbfile = open('userData.text', 'wb')
        pickle.dump(users, dbfile)
        dbfile.close()
        for x in range(0, len(users)):
            if users[x][0] == 'this0':
                users.pop(x)
                break
        print(users)
        if objective == 'GU:':  # get username
            user_number = int(message[3:])
            self.wfile.write(bytes(users[user_number][0], "utf-8"))
        if objective == 'SU:':  # sign up
            user_name = message[3:message.find('|')]
            parsedMessage = message[message.find('|') + 1:]
            pass_word = parsedMessage[0:parsedMessage.find('|')]
            grade = parsedMessage[parsedMessage.find('|') + 1:]
            for x in range(0, len(users)):
                if user_name == users[x][0]:
                    self.wfile.write(bytes('no', "utf-8"))
                    break
                if x == len(users) - 1:
                    users.append([user_name, pass_word, grade, '0'])
                    self.wfile.write(bytes('ye' + str(len(users) - 1) + '|' + '0', "utf-8"))
                    dbfile = open('userData.text', 'wb')
                    pickle.dump(users, dbfile)
                    dbfile.close()
            if len(users) == 0:
                users.append([user_name, pass_word, grade, '0', ''])
                self.wfile.write(bytes('ye' + str(0) + '|' + '0', "utf-8"))
                dbfile = open('userData.text', 'wb')
                pickle.dump(users, dbfile)
                dbfile.close()
            print(users)
        if objective == 'SI:':
            user_name = message[3:message.find('|')]
            pass_word = message[message.find('|') + 1:]
            for x in range(0, len(users)):
                if user_name == users[x][0] and pass_word == users[x][1]:
                    self.wfile.write(bytes('ye' + str(x) + '|' + users[x][3], "utf-8"))
                    break
                if x == len(users) - 1:
                    self.wfile.write(bytes('no', "utf-8"))
            if len(users) == 0:
                self.wfile.write(bytes('no', "utf-8"))
        if objective == 'UP:':  # user points
            userNumber = int(message[3:])
            self.wfile.write(bytes(users[userNumber][3], "utf-8"))

        if objective == 'AP:':  # add points
            userNumber = int(message[3:message.find('|')])
            points = int(message[message.find('|') + 1:])
            users[userNumber][3] = str(points)
            dbfile = open('userData.text', 'wb')
            pickle.dump(users, dbfile)
            dbfile.close()
        if objective == 'CP:':  # clear points
            for x in range(0, len(users)):
                users[x][3] = '0'
            dbfile = open('userData.text', 'wb')
            pickle.dump(users, dbfile)
            dbfile.close()
        if objective == 'GR:':  # generate report
            message2 = ''
            for x in range(0, len(users)):
                for y in range(0, 4):
                    message2 = message2 + str(users[x][y]) + '|'
            print(users)
            self.wfile.write(bytes(message2, "utf-8"))
        if objective == 'AC:':  # add clubs
            user_number = int(message[3:message.find('|')])
            users[user_number][4] = ''
            users[user_number][4] = users[user_number][4] + message[message.find('|') + 1:]
            dbfile = open('userData.text', 'wb')
            pickle.dump(users, dbfile)
            dbfile.close()
        if objective == 'GC:':  # get clubs
            user_number = int(message[3:message.find('|')])
            if len(users[user_number]) == 4:
                users[user_number].append('')
            self.wfile.write(bytes(users[user_number][4] + 'a', "utf-8"))
            dbfile = open('userData.text', 'wb')
            pickle.dump(users, dbfile)
            dbfile.close()


def get_users():
    dbfile = open('userData.text', 'rb')
    users = pickle.load(dbfile)
    dbfile.close()
    return users


server_address = ('localhost', 9999)
httpd = HTTPServer(server_address, Server)
print("server started")
httpd.serve_forever()
