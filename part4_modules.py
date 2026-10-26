import requests
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime, timezone

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

#exercitiu 35
import urllib.parse

def parse_url():
    url = "https://cybercor.org/path?x=1#top"
    result = urllib.parse.urlparse(url)

    print("Scheme:", result.scheme)
    print("Domeniu:", result.netloc)
    print("Cale:", result.path)
    print("Query:", result.query)
    print("Fragment:", result.fragment)

parse_url()

#exercitiu 36
import urllib.parse

BASE_URL = "https://cybercor.org"

def join_urls():
    links = ["/about", "contact.html", "../index.html"]

    for link in links:
        full_url = urllib.parse.urljoin(BASE_URL + "/", link)
        print(full_url)

join_urls()

#exercitiu 37
import re

def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))

html = '''
<a href="/about">Despre</a>
<a href="/contact">Contact</a>
<a href="/about">Despre din nou</a>
'''

print(extract_links(html))

#exercitiu 38
import urllib.parse

BASE_URL = "https://cybercor.org"

def split_links(links, domain):
    internal = []
    external = []

    for link in links:
        full_url = urllib.parse.urljoin(BASE_URL + "/", link)
        netloc = urllib.parse.urlparse(full_url).netloc

        if netloc == domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external

links = [
    "/about",
    "https://cybercor.org/contact",
    "https://google.com",
    "https://example.com"
]

internal, external = split_links(links, "cybercor.org")

print("Interne:", internal)
print("Externe:", external)

#exercitiu 39
from html.parser import HTMLParser

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src:
                self.images.append(src)


test_html = """
<html><body>
<img src="/logo.png" alt="Logo">
<IMG SRC="poza.jpg">
<img alt="imagine fără src">
<img src="https://cdn.example.com/banner.webp" />
<a href="/despre">Despre</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)

print(finder.images)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
], "Parserul nu a găsit exact imaginile așteptate"

print("Testul a trecut!")

response = requests.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status()

finder = ImageFinder()
finder.feed(response.text)

print(len(finder.images), "imagini găsite")

for src in finder.images:
    print(src)

print("Apariții ale tagului img:",
      response.text.lower().count("<img"))

#exercitiu 40
import requests
import hashlib

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    return hashlib.sha256(response.content).hexdigest()

first = page_fingerprint(BASE_URL)
second = page_fingerprint(BASE_URL)

print("Prima amprentă:", first)
print("A doua amprentă:", second)
print("Sunt identice:", first == second)

#exercitiu 41
import requests
import hashlib

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

def page_fingerprint(url):
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    return hashlib.sha256(response.content).hexdigest()

first = page_fingerprint(BASE_URL)
second = page_fingerprint(BASE_URL)

print("Prima amprentă:", first)
print("A doua amprentă:", second)
print("Sunt identice:", first == second)

#exercitiu 42
import socket

def resolve(hostname):
    return socket.gethostbyname(hostname)

ip = resolve("cybercor.org")
print("Adresa IP:", ip)

#exercitiu 43
import socket
import ssl
from datetime import datetime, timezone

def cert_days_left(hostname):
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443), timeout=10
    ) as sock:
        with context.wrap_socket(
            sock, server_hostname=hostname
        ) as secure_sock:
            cert = secure_sock.getpeercert()

    expiry_timestamp = ssl.cert_time_to_seconds(
        cert["notAfter"]
    )

    expiry_date = datetime.fromtimestamp(
        expiry_timestamp, timezone.utc
    )

    now = datetime.now(timezone.utc)
    remaining = expiry_date - now

    return remaining.days

days = cert_days_left("cybercor.org")
print("Zile până la expirarea certificatului:", days)