import json
import socket
import sys

class logstash:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    def sendmsg(self, message):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            return False

        try:
            sock.connect((self.HOST, self.PORT))
        except socket.error as msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            return False

        msg = message
        byt = (json.dumps(msg)).encode()
        sock.sendall(byt)
        #sock.send('\n')
        sock.close()
        return True