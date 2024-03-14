import argparse
import sys
import os

parser = argparse.ArgumentParser(description="Crack hashes using wordlists")
parser.add_argument("-H", "--hash", help="The hash to crack")
parser.add_argument("-f", "--file", help="A file containing hashes to crack")
parser.set_defaults(hash=None, file=None, threads=None)
args = parser.parse_args()

if args.hash and args.file:
    parser.error("[–] You can't specify both a hash and a file containing hashes to crack")
    sys.exit(1)

if not args.hash and not args.file:
    print("[-] You did not specify any input, defaulting to hash.txt...")
    args.file = "hash.txt"
