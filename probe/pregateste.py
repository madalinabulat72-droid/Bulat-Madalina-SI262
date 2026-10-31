
from pathlib import Path
import base64
import hashlib
import io
import urllib.parse
import zipfile
from PIL import Image
import piexif

DOSAR = Path(__file__).resolve().parent
DOSAR.mkdir(exist_ok=True)

mesaj = "Mesajul secret al laboratorului 6"
strat_url = urllib.parse.quote(mesaj)
strat_hex = strat_url.encode().hex()
strat_base64 = base64.b64encode(strat_hex.encode()).decode()

(DOSAR / "mesaj.txt").write_text(strat_base64, encoding="utf-8")

mesaj_xor = b"FLAG{xor_a_fost_descoperit}"
cheie = 42
date_xor = bytes(octet ^ cheie for octet in mesaj_xor)
(DOSAR / "xor.bin").write_bytes(date_xor)

parole = ["parola123", "admin", "secret", "python"]
algoritmi = [hashlib.md5, hashlib.sha1, hashlib.sha256]

with open(DOSAR / "hashuri.txt", "w", encoding="utf-8") as f:
    for algoritm, parola in zip(algoritmi, parole[:3]):
        f.write(algoritm(parola.encode()).hexdigest() + "\n")

with open(DOSAR / "wordlist.txt", "w", encoding="utf-8") as f:
    for parola in parole:
        f.write(parola + "\n")

img = Image.new("RGB", (300, 200), color=(100, 150, 200))

gps = {
    piexif.GPSIFD.GPSLatitudeRef: "N",
    piexif.GPSIFD.GPSLatitude: ((47, 1), (0, 1), (0, 1)),
    piexif.GPSIFD.GPSLongitudeRef: "E",
    piexif.GPSIFD.GPSLongitude: ((28, 1), (50, 1), (0, 1)),
}

exif = {
    "0th": {
        piexif.ImageIFD.Make: b"Laborator",
        piexif.ImageIFD.Model: b"Forensics",
    },
    "Exif": {},
    "GPS": gps,
    "1st": {},
    "thumbnail": None,
}

exif_bytes = piexif.dump(exif)
img.save(DOSAR / "foto.jpg", "jpeg", exif=exif_bytes)

img_png = Image.new("RGB", (200, 150), color=(80, 180, 120))
cale_png = DOSAR / "ascuns.png"
img_png.save(cale_png, "PNG")

continut_zip = io.BytesIO()

with zipfile.ZipFile(continut_zip, "w") as arhiva:
    arhiva.writestr("mesaj_ascuns.txt", "Felicitari! Ai gasit fisierul ascuns.")

with open(cale_png, "ab") as f:
    f.write(continut_zip.getvalue())

print("Pregatirea laboratorului 6 s-a terminat!")

for fisier in sorted(DOSAR.iterdir()):
    if fisier.is_file():
        print("-", fisier.name)
