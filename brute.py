#!/usr/bin/env python3

import hashlib
import sys
import bcrypt as bcrypt_lib
import re
import os

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    WHITE = '\033[0m'
def in_color(color, string):
    return f"{color}{string}{Color.WHITE}"

def sha_2(string):
    return hashlib.sha2(string.encode()).hexdigest()

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


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <hash>")
    sys.exit(1)

hash_to_crack = sys.argv[1]

regex_to_function = {
    r"^\$2[ayb]\$.{56}$": bcrypt,
    r"^[A-Fa-f0-9]{32}$": md5,
    r"^[A-Fa-f0-9]{40}$": sha_1,
    r"^[A-Fa-f0-9]{56}$": sha_2,
    r"^[A-Fa-f0-9]{64}$": sha_256,
    r"^[A-Fa-f0-9]{128}$": sha_512
}

detected_hashing_algorithms = []

detected = False
for regex, function in regex_to_function.items():
    if re.match(regex, hash_to_crack):
        detected_hashing_algorithms.append(function)
        detected = True
        break

if not detected:
    print(f"Hashing algorithm not found for {hash_to_crack}")
    print("Supported algorithms: ", end="")
    for regex in regex_to_function.values():
        print(regex.__name__, end=" ")
    print()
    sys.exit(1)
else:
    print(f"{len(detected_hashing_algorithms)} hashing algorithm(s) detected")

    for hashing_function in detected_hashing_algorithms:
        print(f"Cracking hash: {hash_to_crack} using {hashing_function.__name__}...")
        worldists = get_wordlists()

        for wordlist in worldists:
            with open(wordlist, "r") as f:
                for line in f:
                    line = line.strip()
                    if hashing_function(line) == hash_to_crack:
                        print(f"Found: {in_color(Color.GREEN, line)} in {in_color(Color.YELLOW, wordlist)}")
                        sys.exit(0)

print("Wordlist ended, hash not found")
