import csv
import json
import os
import urllib.request

# Organize by app -> {sheet_name: csv_url}
APPS = {
    "gospel-songs": {
        "songs": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=0&single=true&output=csv",
        "artists": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=151712368&single=true&output=csv",
        "albums": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=269740144&single=true&output=csv",
        "events": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmoASBLW5ypa93xt-gIMFYuILZrBgMgAL60ZUjrdXrL9mFwrduS0ZwsUsFyldN-qKj_4iFvGSf0X5O/pub?gid=160527248&single=true&output=csv"
    },
}

def download_and_convert():
    for app_name, sheets in APPS.items():
        os.makedirs(app_name, exist_ok=True)
        for sheet_name, url in sheets.items():
            print(f"Downloading {app_name}/{sheet_name} CSV...")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    content = response.read().decode('utf-8')

                reader = csv.DictReader(content.splitlines())
                data_list = []
                for row in reader:
                    cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                    if any(cleaned_row.values()):
                        data_list.append(cleaned_row)

                filepath = os.path.join(app_name, f"{sheet_name}.json")
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data_list, f, ensure_ascii=False, indent=2)
                print(f"Successfully created {filepath} with {len(data_list)} entries.")
            except Exception as e:
                print(f"Error processing {app_name}/{sheet_name}: {e}")

if __name__ == "__main__":
    download_and_convert()
