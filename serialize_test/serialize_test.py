#Модуль socket для сетевого программирования
from socket import *
import pickle
import timeit
import os
from lxml import objectify, etree
# import jsonpickle

#данные сервера
host = '0.0.0.0'
port = 2000
addr = (host,port)
cnt = 1000

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)

class Object:
    def __init__(self):
        self.integer = 170                          # integer
        self.string = "I AM non empty string"       # string
        self.dict = dict(a = 0, b = 1)              # dict
        self.real = 0.78                            # float
        self.arr = [0] * 1000                       # array

def TestPickle(ob):
    data = pickle.dumps(ob)
    def ser():
        pickle.dumps(ob)
    def des():
        pickle.loads(data)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "PICKLE - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

def TestXML(ob):
    xmlObj = objectify.Element("obj")
    xmlObj.integer = ob.integer
    xmlObj.string = ob.string
    xmlObj.dict = ob.dict
    xmlObj.real = ob.real
    xmlObj.arr = ob.arr
    data = etree.tostring(xmlObj)
    def ser():
        etree.tostring(xmlObj)
    def des():
        objectify.fromstring(data)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "XML - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

def TestJSON(ob):
    data = jsonpickle.encode(ob)
    def ser():
        jsonpickle.encode(ob)
    def des():
        jsonpickle.decode(data)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "JSON - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

def TestProto(ob):
    pob = object_pb2.ObjectProto(
        Integer = ob.integer,
        String = ob.string,
        Dict = ob.dict,
        Real = ob.real,
        Arr = ob.arr
    )
    data = pob.SerializeToString()
    def ser():
        pob.SerializeToString()
    def des():
        pob.FromString(data)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "PROTO - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

def TestAvro(ob):
    schema = avro.schema.parse(open("object.avsc", "rb").read())
    writer = avro.io.DatumWriter(schema)
    bytes_writer = BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write({"integer": ob.integer, "string": ob.string, "dict": ob.dict, "real": ob.real, "arr": ob.arr}, encoder)
    data = bytes_writer.getvalue()
    def ser():
        bytes_writer = BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write({"integer": ob.integer, "string": ob.string, "dict": ob.dict, "real": ob.real, "arr": ob.arr}, encoder)
        bytes_writer.getvalue()
    def des():
        bytes_reader = BytesIO(data)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        reader.read(decoder)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "AVRO - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

def TestYaml(ob):
    data = yaml.dump(ob, Dumper=Dumper)
    def ser():
        yaml.dump(ob, Dumper=Dumper)
    def des():
        yaml.load(data, Loader=Loader)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "YAML - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

def TestMessagePack(ob):
    object = {
        "integer": ob.integer,
        "string": ob.string,
        "dict": ob.dict,
        "real": ob.real,
        "arr": ob.arr
    }
    data = msgpack.packb(object, use_bin_type=True)
    def ser():
        msgpack.packb(object, use_bin_type=True)
    def des():
        msgpack.unpackb(data, raw=False)
    s = timeit.Timer(ser)
    d = timeit.Timer(des)
    return "MESSAGE PACK - " + str(len(data)) + " - " + str(s.timeit(cnt) * 1000 / cnt) + "ms - " + str(d.timeit(cnt) * 1000 / cnt) + "ms"

f = os.environ['FORMAT']
if f == "pickle":
    test_func = TestPickle
elif f == "xml":
    test_func = TestXML
elif f == "json":
    import jsonpickle
    test_func = TestJSON
elif f == "proto":
    os.system("python3 -m grpc_tools.protoc -I. --python_out=./ object.proto")
    import object_pb2
    test_func = TestProto
elif f == "avro":
    import avro.schema
    from avro.datafile import DataFileReader, DataFileWriter
    from io import BytesIO
    test_func = TestAvro
elif f == "yaml":
    import yaml
    from yaml import Loader, Dumper
    test_func = TestYaml
elif f == "msgpack":
    import msgpack
    test_func = TestMessagePack
else:
    print("Incorrect format", flush=True)
    exit(1)

#Бесконечный цикл работы программы
while True:
    
    print('now wait data...', flush=True)
    
    #recvfrom - получает UDP сообщения
    message, addr = udp_socket.recvfrom(10024)
    print('client addr: ', addr, flush=True)
    print('message = ', message[0:10].decode(), flush=True)
    if message[0:11] == b"get_result ":
        message = message[11:]
        x = pickle.loads(message)
        result = test_func(x).encode()
        #sendto - передача сообщения UDP
        udp_socket.sendto(result, addr)
