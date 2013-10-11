#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-10-11 上午11:12
# **************************************

import paramiko
from celery.task import task


@task
def invoke_shell_remote(shell_path, ip, port=36000, username='Administrator', password='1qazXSW@'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username, password)
    _, out, _ = client.exec_command(shell_path)
    output = []
    result = ''.join(output)
    return result


@task
def test(shell_path, ip, port=36000, username='Administrator', password='1qazXSW@'):
    result = shell_path + ip + username + password + str(port)
    return result