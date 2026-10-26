import webtools

BASE_URL = "https://cybercor.org"

response = webtools.fetch(BASE_URL)
title = webtools.get_title(response.text)

print("Titlu:", title)
print("Cod de stare:", webtools.get_status(BASE_URL))

#exercitiu 45
from webtools import fetch, get_title, security_headers

BASE_URL = "https://cybercor.org"

response = fetch(BASE_URL)

print("Titlu:", get_title(response.text))
print("Antete de securitate:", security_headers(BASE_URL))

#exercitiu 47
from webtools import DEFAULT_HEADERS, fetch

print("Antete implicite:", DEFAULT_HEADERS)

response = fetch("https://cybercor.org")
print("Cod de stare:", response.status_code)

#exercitiu 48
import argparse
import webtools

def main():
    parser = argparse.ArgumentParser(
        description="Analizează o pagină web"
    )

    parser.add_argument(
        "url",
        help="URL-ul site-ului de analizat"
    )

    args = parser.parse_args()
    url = args.url

    response = webtools.fetch(url)

    print("Cod de stare:", response.status_code)
    print("URL final:", response.url)
    print("Titlu:", webtools.get_title(response.text))

if __name__ == "__main__":
    main()

#exercitiu 49
from webtools import check_paths, save_csv

results = check_paths("https://cybercor.org")
save_csv(results)

print("Raport salvat în report.csv")

#exercitiu 50
from webtools import site_report

site_report("https://cybercor.org")