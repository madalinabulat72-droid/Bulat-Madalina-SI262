#b1

def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex()


print(tip_real("probe/foto.jpg"))

#b2

import re

def extrage_text(cale):
    with open(cale, "rb") as f:
        date = f.read()

    for m in re.findall(rb"[ -~]{4,}", date):
        print(m.decode())


print("\n--- B2: TEXT EXTRAS ---")
extrage_text("probe/ascuns.png")

#b3

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extrage_exif(cale):
    img = Image.open(cale)
    exif = img.getexif()

    for id, val in exif.items():
        print(TAGS.get(id, id), "=", val)

    gps = exif.get_ifd(34853) if 34853 in exif else {}
    gps = {GPSTAGS.get(k, k): v for k, v in gps.items()}

    if "GPSLatitude" in gps and "GPSLongitude" in gps:
        lat = gps["GPSLatitude"]
        lon = gps["GPSLongitude"]

        latitudine = float(lat[0]) + float(lat[1]) / 60 + float(lat[2]) / 3600
        longitudine = float(lon[0]) + float(lon[1]) / 60 + float(lon[2]) / 3600

        if gps.get("GPSLatitudeRef") == "S":
            latitudine = -latitudine

        if gps.get("GPSLongitudeRef") == "W":
            longitudine = -longitudine

        print("Latitudine:", latitudine)
        print("Longitudine:", longitudine)
    else:
        print("Coordonate GPS inexistente")


print("\n--- B3: METADATE EXIF ---")
extrage_exif("probe/foto.jpg")

#b4

def extrage_zip(cale):
    with open(cale, "rb") as f:
        date = f.read()

    i = date.find(b"PK\x03\x04")

    if i != -1:
        with open("gasit.zip", "wb") as f:
            f.write(date[i:])

        print("Arhiva extrasa de la octetul", i)
    else:
        print("Arhiva ZIP nu a fost gasita")


print("\n--- B4: FILE CARVING ---")
extrage_zip("probe/ascuns.png")

#b5

from PIL import Image

img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())

mesaj = b"FLAG{ascuns_in_pixeli}\0"
biti = "".join(f"{x:08b}" for x in mesaj)

if len(biti) > len(px) * 3:
    raise ValueError("Imaginea nu are suficienti pixeli")

px_nou = []

for i, (r, g, b) in enumerate(px):
    canale = [r, g, b]

    for j in range(3):
        poz = i * 3 + j
        if poz < len(biti):
            canale[j] = (canale[j] & ~1) | int(biti[poz])

    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")

print("Mesajul a fost ascuns cu succes!")
print("Imagine salvata: stego.png")

#b6

print("\n--- B6: MESAJ DEZVALUIT ---")

px = list(Image.open("stego.png").convert("RGB").getdata())

biti = ""

for (r, g, b) in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

octeti = []

for i in range(0, len(biti) - 7, 8):
    octet = int(biti[i:i+8], 2)

    if octet == 0:
        break

    octeti.append(octet)

mesaj = bytes(octeti).decode("utf-8")

print("Mesaj recuperat:", mesaj)

