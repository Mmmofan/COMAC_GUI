import socket
import json
class IGPS_receiver(object):

    def __init__(self, host, port, bufsize):
        self.sever_host = host
        self.sever_port = port
        self.bufsize = bufsize
        self.addr = (self.sever_host, self.sever_port)
        self.data = []
        self.igps_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.igps_client.bind(self.addr)

    def read_data(self):
        data = self.igps_client.recv(self.bufsize)
        dict_data = json.loads(data.decode('utf-8'))
        self.data = dict_data

    def close(self):
        self.igps_client.close()

    def fliter_data(self):
        self.output_x = self.data[-1]["coord"]["3"]["X"]
        self.output_y = self.data[-1]["coord"]["3"]["y"]
        self.output_z = self.data[-1]["coord"]["3"]["y"]

'''
{"coord":{"3":{"Flags":0,"TransCount":"2.4.","Valid":true,"X":6457.98193359375,"Y":-3672.16162109375,"Z":-9470.173828125}},
"id":590593573,
"raw":{"3":{"2":{"Flags":0,"LocalCount":253343952,"RPM":1800,"T":33.340641021728516,"t1":0.9559048414230347,"t2":0.2501751780509949},
"4":{"Flags":0,"LocalCount":254042966,"RPM":1750,"T":34.28936004638672,"t1":0.44152122735977173,"t2":0.721427321434021}}}}
'''
if '__name__'=='__main__':
    '''大致操作过程：建立连接，sever开始不断发送数据，read_data一次读取一次数据包，udp性质决定，一次一个完整的包，然后fliter_data对字典
    处理，读取xyz数据，最后可通过close断开连接'''
    re = IGPS_receiver('127.0.0.1', 10000, 1024)#建立连接






