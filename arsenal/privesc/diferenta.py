#b1
from arsenal.privesc.enum import citeste_linii, nume, GTFO


def cai(fisier):
    """Returneaza multimea cailor din fisier."""
    return set(citeste_linii(fisier))

#b2
def compara(acum, baza):
    """Identifica fisierele SUID noi fata de baza."""
    noi = acum - baza
    return noi

#b3
def analizeaza(acum, baza):
    """Clasifica fisierele SUID noi dupa nivelul de risc."""
    noi = compara(acum, baza)

    risc = {
        nume(c): "mare" if nume(c) in GTFO else "normal"
        for c in noi
    }

    periculoase = [
        c for c in noi
        if nume(c) in GTFO
    ]

    return risc, periculoase

#b4
def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}

    assert acum - baza == {"c"}