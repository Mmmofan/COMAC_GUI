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
        # self.igps_client.bind(self.addr)

    def read_data(self):
        self.igps_client.sendto(b'go', self.addr)
        data,addr = self.igps_client.recvfrom(self.bufsize)
        # try:
        dict_data = json.loads(data.decode('utf-8'))
        self.data += [dict_data]
        # except:
        #     self.judge()

    def close(self):
        self.igps_client.close()

    def fliter_data(self):
        self.output = self.data[-1]

    # def judge(self):
    #     pass
'''
{"coord":{"3":{"Flags":0,"TransCount":"2.4.","Valid":true,"X":6457.98193359375,"Y":-3672.16162109375,"Z":-9470.173828125}},
"id":590593573,
"raw":{"3":{"2":{"Flags":0,"LocalCount":253343952,"RPM":1800,"T":33.340641021728516,"t1":0.9559048414230347,"t2":0.2501751780509949},
"4":{"Flags":0,"LocalCount":254042966,"RPM":1750,"T":34.28936004638672,"t1":0.44152122735977173,"t2":0.721427321434021}}}}
'''
if '__name__'=='__main__':
    re=IGPS_receiver('127.0.0.1', 10000, 1024)






