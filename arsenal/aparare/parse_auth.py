
#a1
import re
from collections import Counter

TIPAR = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+) port"
)


def esec(linie):
    m = TIPAR.search(linie)

    if m is None:
        return None

    return (m.group(1), m.group(2))


#a2
def citeste_esecuri(cale):
    esecuri = []

    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri

    with f:
        for linie in f:
            r = esec(linie)

            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})

    return esecuri


#a3
def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)


#a4
def main():
    cale = "arsenal/aparare/start/auth.log"

    esecuri = citeste_esecuri(cale)
    print("esecuri:", len(esecuri))

    counts = pe_ip(esecuri)

    print("Incercari grupate dupa IP:")
    for ip, n in counts.most_common():
        print(f"{ip}: {n}")


if __name__ == "__main__":
    main()

