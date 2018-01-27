import socket
import sys
import threading

import paramiko

# using key from the Paramiko demo files
# host_key = paramiko.RSAKey(filename='test_rsa.key')
host_key = paramiko.RSAKey.generate(bits=512)


class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'test') and (password == 'testpwd'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print('[+] Listening for connection...')
    client, addr = sock.accept()
except Exception as e:
    print('[-] Listen failed:', str(e))
    sys.exit(1)
print('[+] Got a connection.')

try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException as x:
        print('[-] SSH negotiation failed')
    chan = bhSession.accept(20)
    if not chan:  # Added error handling
        exit(1)

    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send('Welcome to bh_ssh')
    while True:
        try:
            command = input("Enter command: ")
            if command != 'exit':
                chan.send(command)
                print(chan.recv(1024))  # TODO test for \n added here
            else:
                chan.send('exit')
                print('Exiting')
                bhSession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bhSession.close()
except Exception as e:
    print('[-] Caught exception:', e)  # TODO test if we need str(e) here
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)
