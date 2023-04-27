from socket import *

host = '0.0.0.0'
port = 2000

addr = {"pickle": ("serialize-test-pickle", port),
        "xml": ("serialize-test-xml", port),
        "json": ("serialize-test-json", port),
        "proto": ("serialize-test-proto", port),
        "avro": ("serialize-test-avro", port),
        "yaml": ("serialize-test-yaml", port),
        "msgpack": ("serialize-test-msgpack", port)
}

port = 2000
curAddr = (host,port)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(curAddr)

class Object:
    def __init__(self):
        self.integer = 179                          # integer
        self.string = "I AM non empty string"       # string
        self.dict = dict(a = 0, b = 1)              # dict
        self.real = 0.78                            # float
        self.arr = [0] * 1000                       # array


while True:
    
    print('now wait request...', flush=True)
    
    message, client_addr = udp_socket.recvfrom(10024)
    print('client addr: ', client_addr, flush=True)
    print('message = ', message[0:10].decode(), flush=True)
    if message[0:11] == b"get_result ":
        message = message[11:]
        serType = message.split(maxsplit=1)
        serType[0] = serType[0].decode()
        if serType[0] in addr:
            print("sended to", addr[serType[0]], flush=True)
            udp_socket.sendto(b"get_result " + serType[1], addr[serType[0]])
            message, server_addr = udp_socket.recvfrom(10024)
            udp_socket.sendto(message, client_addr)
        elif serType[0] == "all":
            for type in addr:
                print("sended to", addr[type], flush=True)
                udp_socket.sendto(b"get_result " + serType[1], addr[type])
                message, server_addr = udp_socket.recvfrom(10024)
                udp_socket.sendto(message, client_addr)
