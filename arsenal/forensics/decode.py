import re
import base64
import hashlib
import argparse
import json
from pathlib import Path

#a1

s = "Salut"

b = s.encode()

print(b, b[0])

print(b.hex())

b2 = bytes.fromhex(b.hex())

print(b2)

#a2

import re

def ghici_strat(s):
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"

    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"

    return "necunoscut"


print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))

#a3

import base64
from urllib.parse import unquote

def desfa(s):
    strat = ghici_strat(s)

    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)

    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        rezultat = s.encode()

    return strat, rezultat


print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%2Fetc"))

#a4

def citibil(b):
    return all(32 <= c < 127 for c in b)


val = "NTM1OTU3NTk="

for _ in range(8):
    strat, b = desfa(val)

    print("Strat:", strat)

    if citibil(b):
        print("Mesaj decodat:", b.decode())
        break

    val = b.decode()

#a5

date = open("probe/xor.bin", "rb").read()

for k in range(256):
    clar = bytes(b ^ k for b in date)

    if b"FLAG{" in clar and b"}" in clar:
        print("Cheie:", k)
        print("Mesaj:", clar.decode())
        break

#a6
import hashlib

tinta = open("probe/hashuri.txt").readline().strip()

if len(tinta) == 32:
    algoritm = hashlib.md5
elif len(tinta) == 40:
    algoritm = hashlib.sha1
elif len(tinta) == 64:
    algoritm = hashlib.sha256
else:
    print("Algoritm necunoscut")
    algoritm = None

if algoritm:
    print("Algoritm:", algoritm().name)

    for cuv in open("probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()

        if algoritm(cuv.encode()).hexdigest() == tinta:
            print("Gasit:", cuv)
            break

#a7
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        continut = Path(a.intrare).read_bytes()
        intrare = continut.decode("latin1")
    else:
        intrare = a.intrare

    strat, rezultat = desfa(intrare)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.hex()
    }

    cale = Path(__file__).parent / "fisa.json"

    with open(cale, "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)

    print("Strat:", strat)
    print("Rezultat:", rezultat)
    print("Fișa a fost salvată:", cale)