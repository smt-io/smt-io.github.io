import csv
import json
import urllib.request

# Google Sheet CSV URLs (your links)
URLS = {
    "cumtumyanmar": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTpuroWI-gl-l77Rg2YBLgbXGpoudQawRZ0SWI_s1f58C-C9BAqSzkIO1ZX-f_aynkSTChXJfBncede/pub?gid=0&single=true&output=csv",
    "myanmarcumtu": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTpuroWI-gl-l77Rg2YBLgbXGpoudQawRZ0SWI_s1f58C-C9BAqSzkIO1ZX-f_aynkSTChXJfBncede/pub?gid=1456915011&single=true&output=csv"
}

def download_and_convert():
    for name, url in URLS.items():
        print(f"Downloading {name} CSV...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
            # Parse CSV
            reader = csv.DictReader(content.splitlines())
            data_list = []
            for row in reader:
                # Clean up keys and values (strip whitespaces)
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                # Skip empty rows
                if any(cleaned_row.values()):
                    data_list.append(cleaned_row)
            
            # Save to JSON file
            filename = f"{name}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=2)
            print(f"Successfully created {filename} with {len(data_list)} entries.")
            
        except Exception as e:
            print(f"Error processing {name}: {e}")

if __name__ == "__main__":
    download_and_convert()
