#exercitiu 9
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org/get"
TIMEOUT = 10

#exercitiu 10
print("Verificam pagina principala...")

response = requests.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status()
print("Pagina principala functioneaza! Cod:", response.status_code)

time.sleep(1)

print("Verificam pagina inexistenta...")

try:
    response = requests.get(
        BASE_URL + "/this-page-does-not-exist",
        timeout=TIMEOUT
    )
    response.raise_for_status()
    print("Serverul nu a returnat o eroare HTTP.")
except requests.HTTPError:
    print("Pagina nu exista sau serverul a refuzat cererea.")
except requests.RequestException as e:
    print("Eroare de conexiune:", e)

#exercitiu 11
response = requests.get(BASE_URL, timeout=TIMEOUT)

for name, value in response.headers.items():

    print(f"{name}: {value}")

#exercitiu 12
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type:", response.headers.get("content-type", "lipsește"))

#exercitiu 13
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

numar = response.text.lower().count("cyber")
print("Cuvantul cyber apare de", numar, "ori.")

# Putem inlantui .lower() si .count() deoarece .lower()
# transforma textul in litere mici, iar .count() numara
# aparitiile cuvantului in textul transformat.

#exercitiu 14
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

start = response.text.find("<title>")
end = response.text.find("</title>")

if start != -1 and end != -1:
    titlu = response.text[start + len("<title>"):end].strip()
    print("Titlul paginii:", titlu)
else:
    print("Titlul paginii nu a fost gasit.")

#exercitiu 15
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

lines = response.text.splitlines()

print("Numarul de linii:", len(lines))

if lines:
    longest_line = max(lines, key=len)
    print("Lungimea celei mai lungi linii:", len(longest_line))
else:
    print("Pagina nu contine linii.")

#exercitiu 16
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")

#exercitiu 17
# Exercitiul 17
time.sleep(1)

response = requests.get("http://cybercor.org", timeout=TIMEOUT)

for redirect in response.history:
    print("Cod de stare:", redirect.status_code)
    print("URL:", redirect.url)

print("URL final:", response.url)

#exercitiu 18
time.sleep(1)

response_head = requests.head(BASE_URL, timeout=TIMEOUT)

time.sleep(1)

response_get = requests.get(BASE_URL, timeout=TIMEOUT)

print("Lungimea continutului HEAD:", len(response_head.content))
print("Lungimea continutului GET:", len(response_get.content))

# HEAD returneaza doar antetele, fara corpul paginii.
# GET returneaza antetele si continutul paginii HTML.

#exercitiu 19
time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat")

#exercitiu 20
time.sleep(1)

session = requests.Session()
session.headers.update({
    "User-Agent": "WebLab-Madalina-Bulat"
})

response = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)

print("Raspuns text:")
print(response.text)

print("Raspuns JSON:")
try:
    data = response.json()
    print(data)
    print("User-Agent trimis:", data.get("headers", {}).get("User-Agent", "Nu a fost gasit"))
except requests.exceptions.JSONDecodeError:
    print("Raspunsul primit nu este JSON valid.")
    
# response.text returneaza raspunsul ca text.
# response.json() transforma raspunsul JSON in obiecte Python.