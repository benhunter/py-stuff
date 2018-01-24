import paramiko
import threading
import threading

import paramiko


# using key from the Paramiko demo files

class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, ):
