import socket
import sys
import threading


def hexdump(src_bytes, length=16):
    '''
    Dump hexadecimal
    :param src_bytes: Bytes, Bytearray, or compatible object
    :param length: Length of each output line
    :return:
    '''
    result = []
    digits = 4  # python2 code, all python3 strings are Unicode: if isinstance(src, unicode) else 2

    # for i in xrange(0, len(src), length):
    for i in range(0, len(src_bytes), length):
        s = src_bytes[i:i + length]
        hexa = ' '.join(["%0*X" % (digits, x) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append('%04X   %-*s   %s' % (i, length * (digits + 1), hexa, text))

    print('\n'.join(result))


def hexdump_string(src_string, length=16):
    '''
    Dump hexadecimal
    :param src_string: String or compatible object
    :param length: Length of each output line
    :return:
    '''
    result = []
    digits = 4  # python2 code, all python3 strings are Unicode: if isinstance(src, unicode) else 2

    # for i in xrange(0, len(src), length):
    for i in range(0, len(src_string), length):
        s = src_string[i:i + length]
        hexa = ' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = ''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s])
        result.append('%04X   %-*s   %s' % (i, length * (digits + 1), hexa, text))

    print('\n'.join(result))


def receive_from(connection, timeout=1):
    buffer = bytearray(b'')

    # Set 1 second timeout
    # Adjust based on target
    connection.settimeout(timeout)  # TODO what's the point in setting a timeout? to prevent blocking
    try:
        # Read into buffer until no data or timeout.
        while True:
            print('connection.recv(4096),', connection.getsockname())
            # data = connection.recv(4096).decode('utf-8')  # TODO decode or leave as bytes?
            data = connection.recv(4096)  # TODO decode or leave as bytes? let's try bytes...bytearray is mutable

            if not data:
                print('No data!!')
                connection.close()
                break
            buffer += data
    except socket.timeout as e:
        print('Exception', e, type(e))
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
        remote_buffer = receive_from(remote_socket)  # TODO now returning bytes
        print('Receive first, dumping recv')
        hexdump(remote_buffer)

        # send it to response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data for local client, send it
        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            # client_socket.sendall(remote_buffer.encode('utf-8'))  # now working with bytes TODO send or sendall?
            client_socket.sendall(remote_buffer)  # TODO send or sendall?

    # now loop and read from local, send to remote, send to local.

    while True:
        try:
            # read for local host
            print('Receive from client', client_socket.getsockname())
            local_buffer = receive_from(client_socket)  # TODO now returning bytes

            if len(local_buffer):

                print("[==>] Received %d bytes from localhost." % len(local_buffer))
                hexdump(local_buffer)

                # send it to our request handler
                local_buffer = request_handler(local_buffer)

                # send off data to remote host
                # remote_socket.sendall(local_buffer.encode('utf-8'))  # now working with bytes TODO send or sendall?
                remote_socket.sendall(local_buffer)  # TODO send or sendall?
                print("[==>] Sent to remote.")

                # receive the response
                print('Receive from remote', remote_socket.getsockname())
                remote_buffer = receive_from(remote_socket)  # TODO now returning bytes

                if len(remote_buffer):
                    print("[<==] Received %d bytes from remote." % len(remote_buffer))
                    hexdump(remote_buffer)

                    # send to response handler
                    remote_buffer = response_handler(remote_buffer)

                    # send response to local socket
                    # client_socket.sendall(remote_buffer.encode('utf-8'))  # now working with bytes TODO send or sendall?
                    client_socket.sendall(remote_buffer)  # TODO send or sendall?

                    print("[<==] Send to localhost.")

                if not len(local_buffer) or not len(remote_buffer):
                    client_socket.close()
                    remote_socket.close()
                    print("[*] No more data. Closing connections")

                    break
        except OSError as e:
            print('OSError:', e)
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
        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def usage():
    print("Usage: ./proxy.py <LHOST> <LPORT> <RHOST> <RPORT> <Receive first?>")
    print("Usage: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")


def main():
    if len(sys.argv[1:]) != 5:
        usage()
        sys.exit(1)
    # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    if "true" == sys.argv[5].lower():
        receive_first = True
    elif "false" == sys.argv[5].lower():
        receive_first = False
    else:
        print("Bad argument in <Receive first?>")
        usage()
        sys.exit(1)
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)
    sys.exit(0)


if __name__ == '__main__':
    main()
