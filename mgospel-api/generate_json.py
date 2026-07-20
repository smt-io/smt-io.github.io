import csv
import json
import os
import urllib.request

# Google Sheet CSV URLs
URLS = {
    "songs": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=0&single=true&output=csv",
    "artists": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=151712368&single=true&output=csv",
    "albums": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=269740144&single=true&output=csv",
    "events": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=160527248&single=true&output=csv",
}

OUTPUT_DIR = "mgospel-api"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_and_convert():
    for name, url in URLS.items():
        print(f"Downloading {name}...")

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            with urllib.request.urlopen(req) as response:
                content = response.read().decode("utf-8")

            reader = csv.DictReader(content.splitlines())

            data = []

            for row in reader:
                cleaned = {
                    k.strip(): v.strip()
                    for k, v in row.items()
                    if k is not None
                }

                if any(cleaned.values()):
                    data.append(cleaned)

            filename = os.path.join(
                OUTPUT_DIR,
                f"{name}.json"
            )

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

            print(f"Created {filename}")

        except Exception as e:
            print(e)


if __name__ == "__main__":
    download_and_convert()
