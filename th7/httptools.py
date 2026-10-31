import requests

BASE = "https://httpbin.org"

PATHS = [
    "/get",
    "/redirect/2",
    "/delay/1",
    "/status/404",
    "/delay/5"
]
# Partea 1: parametri în URL

def search(params):
    """Trimite parametrii către server și returnează răspunsul."""
    r = requests.get(BASE + "/get", params=params)
    return r.json()["args"]


def search_url(params):
    """Returnează adresa completă cu parametrii."""
    r = requests.get(BASE + "/get", params=params)
    return r.url

# Partea 2: anteturi

def fetch_with_agent(agent):
    """Returnează User-Agent-ul văzut de server."""
    r = requests.get(
        BASE + "/headers",
        headers={"User-Agent": agent}
    )
    return r.json()["headers"]["User-Agent"]


def default_agent():
    """Returnează User-Agent-ul implicit."""
    r = requests.get(BASE + "/headers")
    return r.json()["headers"]["User-Agent"]

# Partea 3: trimiterea datelor

def post_json(data):
    """Trimite date ca JSON și returnează răspunsul."""
    r = requests.post(BASE + "/post", json=data)
    return r.json()["json"]


def post_form(data):
    """Trimite date ca formular și returnează răspunsul."""
    r = requests.post(BASE + "/post", data=data)
    return r.json()["form"]

# Partea 4: coduri de stare

def describe_status(code):
    """Descrie codul de stare HTTP."""
    r = requests.get(BASE + "/status/" + str(code))

    if 200 <= r.status_code < 300:
        return "succes"
    elif 400 <= r.status_code < 500:
        return "eroare client"
    elif 500 <= r.status_code < 600:
        return "eroare server"


def is_ok(code):
    """Verifică dacă cererea a reușit."""
    try:
        r = requests.get(BASE + "/status/" + str(code))
        r.raise_for_status()
        return True
    except requests.HTTPError:
        return False

 # Partea 5: redirecționări

def count_redirects(n):
    """Returnează numărul redirecționărilor urmate."""
    r = requests.get(BASE + "/redirect/" + str(n))
    return len(r.history)


def final_url(n):
    """Returnează adresa finală după redirecționări."""
    r = requests.get(BASE + "/redirect/" + str(n))
    return r.url


def first_hop(n):
    """Returnează prima adresă de redirecționare."""
    r = requests.get(
        BASE + "/redirect/" + str(n),
        allow_redirects=False
    )
    return r.headers["Location"]   

# Partea 6: sesiuni și cookie-uri

def cookie_demo(name, value):
    """Setează și citește un cookie folosind o singură sesiune."""
    s = requests.Session()

    s.get(BASE + "/cookies/set", params={name: value})

    r = s.get(BASE + "/cookies")

    return r.json()["cookies"]


def no_session_demo(name, value):
    """Încearcă să citească un cookie fără să folosească sesiune."""
    requests.get(BASE + "/cookies/set", params={name: value})

    r = requests.get(BASE + "/cookies")

    return r.json()["cookies"]

# Partea 7: raportul final

def report(path):
    """Returnează un raport despre pagina solicitată."""

    try:
        r = requests.get(BASE + path, timeout=3)

        return {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": r.elapsed.total_seconds(),
            "content_type": r.headers.get("Content-Type")
        }

    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }


def check_login(user, password):
    """Verifică autentificarea HTTP Basic."""
    try:
        r = requests.get(
            BASE + "/basic-auth/admin/secret",
            auth=(user, password),
            timeout=3
        )
        return r.status_code == 200
    except requests.RequestException:
        return False