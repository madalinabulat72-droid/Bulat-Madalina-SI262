#a1
import argparse
import json
from pathlib import Path

def citeste_linii(cale):
    """Citeste liniile din fisier, ignorand liniile goale si comentariile."""
    with open(cale, "r", encoding="utf-8") as f:
        return [
            linie.strip()
            for linie in f
            if linie.strip() and not linie.strip().startswith("#")
        ]


def nume(cale):
    """Extrage numele fisierului din cale."""
    return cale.rsplit("/", 1)[-1]


GTFO = {
    "find",
    "vim.basic",
    "vim",
    "nmap",
    "cp",
    "bash",
    "less",
    "awk",
    "python3",
    "perl",
}

#a2
def suid_constatari(cale):
    """Identifica fisierele SUID si nivelul lor de risc."""
    linii = citeste_linii(cale)
    cai_unice = sorted(set(linii))

    rezultate = []

    for cale_fisier in cai_unice:
        nume_fisier = nume(cale_fisier)

        rezultate.append({
            "cale": cale_fisier,
            "nume": nume_fisier,
            "risc": "mare" if nume_fisier in GTFO else "normal"
        })

    return rezultate

#a3
def suid_constatari(cale):
    """Identifica fisierele SUID si nivelul lor de risc."""
    linii = citeste_linii(cale)
    cai_unice = sorted(set(linii))

    rezultate = []

    for cale_fisier in cai_unice:
        nume_fisier = nume(cale_fisier)

        rezultate.append({
            "cale": cale_fisier,
            "nume": nume_fisier,
            "risc": "mare" if nume_fisier in GTFO else "normal"
        })

    return rezultate

#a4
def sudo_constatari(cale):
    """Identifica regulile SUDO si nivelul lor de risc."""
    linii = citeste_linii(cale)
    rezultate = []

    for linie in linii:
        utilizator, drept = linie.split(" : ", 1)

        rezultate.append({
            "user": utilizator,
            "drept": drept,
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })

    return rezultate
def cron_constatari(cale):
    """Identifica sarcinile CRON."""
    linii = citeste_linii(cale)
    rezultate = []

    for linie in linii:
        campuri = linie.split()

        rezultate.append({
            "user": campuri[5],
            "comanda": " ".join(campuri[6:]),
            "risc": "normal"
        })

    return rezultate
def enumereaza(d):
    """Grupeaza toate constatarile intr-un dictionar."""
    return {
        "suid": suid_constatari(d / "suid.txt"),
        "sudo": sudo_constatari(d / "sudo.txt"),
        "cron": cron_constatari(d / "crontab.txt")
    }
#a5
def main():
    parser = argparse.ArgumentParser(
        description="Inventar SUID, SUDO si CRON"
    )

    parser.add_argument("capturi", type=Path)
    parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    rezultate = enumereaza(args.capturi)

    if args.json:
        print(json.dumps(rezultate, indent=4, ensure_ascii=False))
    else:
        for categorie, lista in rezultate.items():
            risc_mare = sum(
                1 for element in lista
                if element.get("risc") == "mare"
            )
            print(
                f"{categorie}: {len(lista)} gasite, "
                f"{risc_mare} cu risc mare"
            )

        utilizatori = {
            element["user"]
            for categorie in ("sudo", "cron")
            for element in rezultate[categorie]
        }

        print("utilizatori implicati:", ", ".join(sorted(utilizatori)))

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(rezultate, f, indent=4, ensure_ascii=False)

    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
