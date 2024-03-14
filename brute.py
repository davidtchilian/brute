#!/usr/bin/env python3

import hashlib
import sys
import bcrypt as bcrypt_lib
import re
import os
import time

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

def crack_hash(hash_to_crack):
    regex_to_function = {
        r"^\$2[ayb]\$.{56}$": bcrypt,
        r"^[A-Fa-f0-9]{32}$": md5,
        r"^[A-Fa-f0-9]{40}$": sha_1,
        r"^[A-Fa-f0-9]{64}$": sha_256,
        r"^[A-Fa-f0-9]{128}$": sha_512,
        r"^[A-Fa-f0-9]{32}:[A-Fa-f0-9]{32}$": md4
    }

    detected_hashing_algorithms = []

    detected = False
    for regex, function in regex_to_function.items():
        if re.match(regex, hash_to_crack):
            detected_hashing_algorithms.append(function)
            detected = True
            break

    if not detected:
        print(f"[–] Hashing algorithm not found for {hash_to_crack}")
        print("Supported algorithms: ", end="")
        for regex in regex_to_function.values():
            print(regex.__name__, end=" ")
        print()
        print("[-] Exiting...")
        sys.exit(1)
    else:
        for hashing_function in detected_hashing_algorithms:
            print(f"\n[+] Detected {hashing_function.__name__.upper()} for {hash_to_crack}...")
            start = time.time()
            worldists = get_wordlists()

            for wordlist in worldists:
                with open(wordlist, "r") as f:
                    for line in f:
                        line = line.strip()
                        if hashing_function(line) == hash_to_crack:
                            time_taken = round(time.time() - start, 2)
                            print(f"[+] Found: {in_color(Color.YELLOW, hash_to_crack)}:{in_color(Color.GREEN, line)} in {time_taken}s")
                            return

    print(f"[–] Wordlist ended, hash not found for {hash_to_crack}")



import argparsing

args = argparsing.args

if args.hash:
    hash_to_crack = args.hash
    crack_hash(hash_to_crack)
else:
    hashes = []
    with open(args.file, "r") as f:
        hashes = f.readlines()
        threads = []
    for hash_to_crack in hashes:
        crack_hash(hash_to_crack.strip())

print("[+] Done")