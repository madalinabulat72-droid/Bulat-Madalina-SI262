#exercitiu 21
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org/get"
TIMEOUT = 10


# Exercitiul 21
def fetch(url):
    """Returneaza obiectul raspuns pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response


response = fetch(BASE_URL)
print("Cod de stare:", response.status_code)

# Exercitiul 22
def get_status(url):
    """Returneaza codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


status1 = get_status(BASE_URL + "/")
print("Pagina principala:", status1)

time.sleep(1)

status2 = get_status(BASE_URL + "/robots.txt")
print("Robots.txt:", status2)

time.sleep(1)

status3 = get_status(BASE_URL + "/sitemap.xml")
print("Sitemap.xml:", status3)

# Exercitiul 23
def fetch(url, timeout=10):
    """Returneaza obiectul raspuns pentru adresa url."""
    response = requests.get(url, timeout=timeout)
    return response


# Apel cu valoarea implicita timeout=10
response1 = fetch(BASE_URL)
print("Cod de stare (timeout implicit):", response1.status_code)

time.sleep(1)

# Apel cu timeout=3
response2 = fetch(BASE_URL, timeout=3)
print("Cod de stare (timeout=3):", response2.status_code)


# Exercitiul 24
def get_title(html):
    """Extrage titlul din codul HTML."""
    start = html.find("<title>")
    end = html.find("</title>")

    if start != -1 and end != -1:
        title = html[start + len("<title>"):end].strip()
        return title

    return None


# Apelarea functiei
response = fetch(BASE_URL)
title = get_title(response.text)
print("Titlul paginii:", title)

# Exercitiul 25
def get_title(html):
    """Extrage si returneaza titlul paginii din codul HTML."""
    start = html.find("<title>")
    end = html.find("</title>")

    if start != -1 and end != -1:
        return html[start + len("<title>"):end].strip()

    return None


# Afisarea documentatiei functiei
help(get_title)

# Exercitiul 26
def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


# Apel normal
print("Cod de stare:", get_status(BASE_URL))

time.sleep(1)

# Apel cu un argument de tip gresit
try:
    print("Rezultat pentru 123:", get_status(123))
except requests.RequestException as e:
    print("Eroare la cerere:", e)
except Exception as e:
    print("Eroare:", e)

    # Exercitiul 27
def page_exists(url: str) -> bool:
    """Verifica daca pagina poate fi accesata."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


# Apel pentru o pagina existenta
print("Pagina principala exista:", page_exists(BASE_URL))

time.sleep(1)

# Apel pentru un domeniu inexistent
print(
    "Domeniul de test exista:",
    page_exists("https://this-domain-does-not-exist.invalid")
)

# Exercitiul 28
def check_paths(base: str, paths: list) -> dict:
    """Verifica mai multe cai si returneaza codurile HTTP."""
    results = {}

    for path in paths:
        url = base.rstrip("/") + "/" + path.lstrip("/")
        results[path] = get_status(url)
        time.sleep(1)

    return results


# Apelarea functiei
paths = ["/", "/robots.txt", "/sitemap.xml"]
results = check_paths(BASE_URL, paths)

print("Rezultatele verificarilor:")
print(results)

# Exercitiul 29
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returneaza valoarea unui antet HTTP."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)


# Apel cu argumente cu nume
header = get_header(BASE_URL, name="Server")
print("Antetul Server:", header)

# Exercitiul 30
def security_headers(url: str) -> dict:
    """Verifica prezenta a cinci antete de securitate."""
    response = requests.get(url, timeout=TIMEOUT)

    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    results = {}

    for header in headers_to_check:
        results[header] = header in response.headers

    return results


# Apelarea functiei
results = security_headers(BASE_URL)
print("Antete de securitate:")
print(results)

# Exercitiul 31
def score_headers(results: dict) -> str:
    """Calculeaza scorul antetelor de securitate prezente."""
    total = len(results)
    found = sum(results.values())
    return f"{found}/{total}"


# Apelarea celor doua functii impreuna
score = score_headers(security_headers(BASE_URL))
print("Scorul antetelor de securitate:", score)


# Exercitiul 32
def fetch_robots(base: str):
    """Returneaza continutul robots.txt sau None daca lipseste."""
    url = base.rstrip("/") + "/robots.txt"

    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Returneaza lista cailor indicate prin Disallow:."""
    paths = []

    if robots_text is None:
        return paths

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:
                paths.append(path)

    return paths


# Apelarea functiilor
robots_text = fetch_robots(BASE_URL)
print("Continut robots.txt:", robots_text)

paths = disallowed_paths(robots_text)
print("Cai interzise:", paths)

# Verificam si cazul in care fisierul lipseste
print("Test cu None:", disallowed_paths(None))

# Exercitiul 33
def response_times(*urls) -> dict:
    """Returneaza timpul de raspuns pentru fiecare URL."""
    results = {}

    for url in urls:
        try:
            response = requests.get(url, timeout=TIMEOUT)
            results[url] = response.elapsed.total_seconds()
        except requests.RequestException:
            results[url] = None

        time.sleep(1)

    return results


# Apelarea functiei cu doua URL-uri
times = response_times(
    BASE_URL,
    ECHO_URL
)

print("Timpii de raspuns:")
print(times)

# Exercitiul 34
BASE_URL = "https://cybercor.org"

def log(message, **details):
    print(message, end="")

    for key, value in details.items():
        print(f" | {key}={value}", end="")

    print()


log("verificat", url=BASE_URL, status=200)
