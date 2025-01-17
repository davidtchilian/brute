#!/usr/bin/env python3

import hashlib
import sys
import bcrypt as bcrypt_lib
import re
import os
import time
import binascii
import threading
from Crypto.Hash import MD4

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    WHITE = '\033[0m'
def in_color(color, string):
    return f"{color}{string}{Color.WHITE}"

def sha_512(string):
    return hashlib.sha512(string.encode()).hexdigest()

def sha_1(string):
    return hashlib.sha1(string.encode()).hexdigest()

def bcrypt(string):
    return bcrypt_lib.hashpw(string.encode('utf-8'), bcrypt_lib.gensalt()).decode('utf-8')

def sha_256(string):
    return hashlib.sha256(string.encode()).hexdigest()

def md5(string):
    return hashlib.md5(string.encode()).hexdigest()

def ntlm(string):
    md4 = MD4.new()
    md4.update(string.encode('utf-16le'))
    ntlm = md4.digest()
    return ntlm.hex()

def get_wordlists():
    wordlists_to_return = []
    w = [os.path.join("wordlists", f) for f in os.listdir("wordlists")]
    for wordlist in w:
        if os.path.isdir(wordlist):
            for f in os.listdir(wordlist):
                wordlists_to_return.append(os.path.join(wordlist, f))
        else:
            wordlists_to_return.append(wordlist)
    return wordlists_to_return

def crack_hash_thread(hash_to_crack, hash_function):
    start = time.time()
    worldists = get_wordlists()
    for wordlist in worldists:
        with open(wordlist, "r") as f:
            for line in f:
                line = line.strip()
                if hash_function(line) == hash_to_crack:
                    time_taken = round(time.time() - start, 2)
                    print(f"[+] Found {hash_function.__name__.upper()} : {in_color(Color.YELLOW, hash_to_crack)}:{in_color(Color.GREEN, line)} in {time_taken}s")
                    return


def crack_hash_launcher(hashes_and_functions_to_launch):
    global threads
    for hash_to_crack, detected_hashing_algorithms in hashes_and_functions_to_launch.items():
        for hashing_function in detected_hashing_algorithms:
            t = threading.Thread(target=crack_hash_thread, args=(hash_to_crack, hashing_function))
            threads.append(t)
            t.start()




def crack_hash_detect(hash_to_crack):
    hash_to_crack = hash_to_crack.lower()
    regex_to_function = [
        (r"^\$2[ayb]\$.{56}$", bcrypt),
        (r"^[A-Fa-f0-9]{32}$", md5),
        (r"^[A-Fa-f0-9]{32}$", ntlm),
        (r"^[A-Fa-f0-9]{40}$", sha_1),
        (r"^[A-Fa-f0-9]{64}$", sha_256),
        (r"^[A-Fa-f0-9]{128}$", sha_512)
    ]

    detected_hashing_algorithms = []
    hashes_and_functions_to_launch = {}

    for regex, fct in regex_to_function:
        if re.match(regex, hash_to_crack):
            detected_hashing_algorithms.append(fct)

    if not detected_hashing_algorithms:
        print(f"[–] Hashing algorithm not found for {hash_to_crack}")
        print("Supported algorithms: ", end="")
        for regex in regex_to_function.values():
            print(regex.__name__, end=" ")
        print()
        print("[-] Abandonning hash : ", hash_to_crack)
        return
    else:
        hashes_and_functions_to_launch[hash_to_crack] = []
        for hashing_function in detected_hashing_algorithms:
            print(f"[+] Likely {hashing_function.__name__.upper()} for {hash_to_crack}...")
            hashes_and_functions_to_launch[hash_to_crack].append(hashing_function)
    crack_hash_launcher(hashes_and_functions_to_launch)

import argparsing


args = argparsing.args
threads = []
if args.hash:
    hash_to_crack = args.hash
    crack_hash_detect(hash_to_crack)
else:
    hashes = []
    with open(args.file, "r") as f:
        hashes = f.readlines()
        threads = []
    for hash_to_crack in hashes:
        crack_hash_detect(hash_to_crack.strip())
    for t in threads:
        t.join()

