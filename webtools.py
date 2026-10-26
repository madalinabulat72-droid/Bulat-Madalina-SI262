import requests
import re

TIMEOUT = 10

def fetch(url):
    return requests.get(url, timeout=TIMEOUT)

def get_status(url):
    response = fetch(url)
    return response.status_code

def get_title(html):
    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        html,
        re.IGNORECASE | re.DOTALL
    )
    return match.group(1).strip() if match else "Titlu negăsit"

def security_headers(url):
    response = fetch(url)
    headers = response.headers

    required = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy"
    ]

    return {
        header: header in headers
        for header in required
    }

#exercitiu 46
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))

#exercitiu 47
DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Madalina"
}
def fetch(url):
    return requests.get(
        url,
        headers=DEFAULT_HEADERS,
        timeout=TIMEOUT
    )

#exercitiu 49
import csv
from datetime import datetime

def check_paths(url):
    paths = ["/", "/robots.txt", "/admin", "/private"]
    results = []

    for path in paths:
        full_url = url.rstrip("/") + path

        try:
            response = fetch(full_url)
            status = response.status_code
        except requests.RequestException:
            status = "ERROR"

        results.append({
            "path": path,
            "status": status,
            "checked_at": datetime.now().isoformat()
        })

    return results

def save_csv(results, filename="report.csv"):
    with open(
        filename, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["path", "status", "checked_at"]
        )

        writer.writeheader()
        writer.writerows(results)

# Exercițiul 50

import json
import urllib.parse


def site_report(url):
    response = fetch(url)
    response.raise_for_status()

    host = urllib.parse.urlparse(response.url).hostname
    domain = urllib.parse.urlparse(response.url).netloc

    headers = security_headers(response.url)
    links = extract_links(response.text)

    internal, external = split_links(
        links, domain, response.url
    )

    try:
        ip = resolve(host)
    except OSError:
        ip = "Indisponibil"

    try:
        days = cert_days_left(host)
    except (OSError, ValueError, KeyError):
        days = None

    redirects = [
        {"status": r.status_code, "url": r.url}
        for r in response.history
    ]

    report = {
        "status": response.status_code,
        "final_url": response.url,
        "title": get_title(response.text),
        "ip": ip,
        "redirects": redirects,
        "security_score": f"{sum(headers.values())}/5",
        "certificate_days": days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": get_disallowed_paths(response.url)
    }

    print("=== Raport site:", url, "===")

    for key, value in report.items():
        print(f"{key}: {value}")

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("Salvat în report.json")

    return report      
import re
import socket
import ssl
import requests
import urllib.parse
from datetime import datetime
def extract_links(html):
    return re.findall(
        r'href=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE
    )


def split_links(links, domain, base_url):
    internal = []
    external = []

    for link in links:
        full_url = urllib.parse.urljoin(base_url, link)
        parsed = urllib.parse.urlparse(full_url)

        if parsed.scheme not in ("http", "https"):
            continue

        if parsed.netloc.lower() == domain.lower():
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


def resolve(host):
    return socket.gethostbyname(host)


def cert_days_left(host):
    context = ssl.create_default_context()

    with socket.create_connection((host, 443), timeout=10) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_sock:
            cert = secure_sock.getpeercert()

    expiry_date = datetime.strptime(
        cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
    )

    return (expiry_date - datetime.utcnow()).days


def get_disallowed_paths(url):
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    try:
        response = requests.get(robots_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []

    paths = []

    for line in response.text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()

            if path:
                paths.append(path)

    return paths