#!/usr/bin/env python

import paramiko


def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/_/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        print('========== ACTIVE SESSION ==========')
        ssh_session.exec_command(command)
        print(ssh_session.recv(1024))
    return


ssh_command('127.0.0.1', 2222, 'test', 'testpwd', 'id')
