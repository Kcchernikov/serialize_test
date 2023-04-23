from socket import *
import sys
import pickle

host = 'localhost'
port = 2000
addr = (host,port)

udp_socket = socket(AF_INET, SOCK_DGRAM)

class Object:
    def __init__(self):
        self.integer = 179                          # integer
        self.string = "I AM non empty string"       # string
        self.dict = dict(a = 0, b = 1)              # dict
        self.real = 0.78                            # float
        self.arr = [0] * 1000                       # array


ob = Object()
serType = input("Write one of serialization types:\n\tpickle,\n\txml,\n\tjson,\n\tproto,\n\tavro,\n\tyaml,\n\tmsgpack\n") + " "
data = b'get_result ' + serType.encode() + pickle.dumps(ob)
udp_socket.sendto(data, addr)
message, addr = udp_socket.recvfrom(1024)
print(message.decode())

