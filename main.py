import socket
from threading import Thread
import time
from model.modelEncoderADC import angleToADC, ADCtoAngle

class Client:
    def __init__(self, host, port):
        self.sock = self._setup_socket(host, port)
        thread = Thread(target=self.send_cmd)
        thread.daemon = True
        thread.start()

        print(f"************* Successfully connected to TCPServer {host}:{port} ****************")
        print("SET <parameter> <value>: Set value for a parameter angle of fan")
        # print("GET <parameter>: Read the value of a parameter of fan")
        print("Enter the command:")
        while(True):
            data = self.sock.recv(4096)
            if not data:
                break
            print(data.decode())

    def send_cmd(self):
        while(True):
            user_cmd = input()
            args = user_cmd.split()
            if ((len(args) < 2) or args[0].lower() not in ["get","set"] or args[1] not in ["speed", "angle"] or (True if (args[0].lower() == "set" and len(args) <3) else False) ):
                print("Sorry! App doesn't support this cmd")
                continue
            if(args[0].lower() == "set"):
                value = angleToADC(args[2])
                print('Desire Value: ', value)
                stringToSend =  'S' + chr(int(value/1000)) + chr(int((value%1000)/100)) + chr(int((value%1000)%100))+ '\n'
                self.sock.send(stringToSend.encode('utf-8'))


    @staticmethod
    def _setup_socket(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock



if __name__ == "__main__":
    client = Client('192.168.113.10', 23)