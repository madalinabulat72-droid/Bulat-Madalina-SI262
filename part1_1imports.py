print("Salut! Python functioneaza!")
#exercitiu 1
import requests
import urllib.request
import time
print("Versiunea requests:", requests.__version__)

#exercitiu 2
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Primul stil - Cod de stare:", response.status_code)

time.sleep(1)
from requests import get

response = get(BASE_URL, timeout=TIMEOUT)
print("Al doilea stil - Cod de stare:", response.status_code)

#exerctitiu 3
import requests as req

response = req.get(BASE_URL, timeout=TIMEOUT)
print ("Cod de stare:", response.status_code)

#execrcițiu 4
import urllib.request

req = urllib.request.Request(
    BASE_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
    print("Cod de stare:", response.status)
    body = response.read().decode("utf-8")
    print("Primele 200 de caractere:")
    print(body[:200])

#exercitiu 5
print(dir(requests))

# get este o functie.
# Session este o clasa.
# exceptions este un modul.

#exercitiu 6
help(requests.get)

response = requests.get(BASE_URL, timeout=10)
print("Cod de stare:", response.status_code)

#exercitiu 7
import time

start = time.perf_counter()

response = requests.get(BASE_URL, timeout=TIMEOUT)

end = time.perf_counter()

print("Timp total:", end - start, "secunde")
print("Timp response.elapsed:", response.elapsed.total_seconds())

#exercitiu 8
try:

    import bs4

except ImportError:

    print("Instalați modulul cu: pip install beautifulsoup4")