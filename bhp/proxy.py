import socket
import sys
import threading


def hexdump(src, length=16):
    result = []
    digits = 4 # python2 code, all python3 strings are Unicode: if isinstance(src, unicode) else 2

    # for i in xrange(0, len(src), length):
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = ''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s])
        result.append('%04X   %-*s   %s' % (i, length * (digits + 1), hexa, text))

    print('\n'.join(result))

def receive_from(connection):
    buffer = ""

    # Set 2 second timeout
    # Adjust based on target
    connection.settimeout(2)
    try:
        # Read into buffer until no data or timeout.
        while True:
            print('connection.recv(4096),', connection.getsockname())
            data = connection.recv(4096).decode('utf-8')

            if not data:
                print('No data!!')
                break
            buffer += data
    except Exception as e:
        print('Exception', e)
        pass
    return buffer

def request_handler(buffer):
    # perform packet modifications, look for credentials or data
    return buffer

def response_handler(buffer):
    # perform packet modifications, look for credentials or data
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    print('Connected to remote:', remote_socket.getsockname())

    if receive_first:

        print('Receive from remote first')
        remote_buffer = receive_from(remote_socket)
        print('Receive first, dumping recv')
        hexdump(remote_buffer)

        # send it to response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data for local client, send it
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.sendall(remote_buffer.encode('utf-8'))  # TODO send or sendall?

    # now loop and read from local, send to remote, send to local.

    while True:

        # read for local host
        print('Receive from client', client_socket.getsockname())
        local_buffer = receive_from(client_socket)

        if len(local_buffer):

            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off data to remote host
            remote_socket.sendall(local_buffer.encode('utf-8'))  # TODO send or sendall?
            print("[==>] Sent to remote.")

            # receive the reponse
            print('Receive from remote', remote_socket.getsockname())
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print("[<==] Received %d bytes from remote." % len(remote_buffer))
                hexdump(remote_buffer)

                #send to response handler
                remote_buffer = response_handler(remote_buffer)

                # send response to local socket
                client_socket.sendall(remote_buffer.encode('utf-8'))  # TODO send or sendall?

                print("[<==] Send to localhost.")

            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print("[*] No more data. Closing connections")

                break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))

    except:
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(1)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        print("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

if __name__ == '__main__':
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    if "True" in sys.argv[5]:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)