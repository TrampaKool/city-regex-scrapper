import re
import requests
from bs4 import BeautifulSoup

def scrape_city_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return f"Σφάλμα κατά τη σύνδεση: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    infobox = soup.find("table", {"class": "infobox"})
    if not infobox:
        return "Δεν βρέθηκε Infobox στη σελίδα."

    text = infobox.get_text(separator=" ", strip=True)

    # regex
    patterns = {
        "infobox_text": {
            "Πληθυσμός": r"(?:Πληθυσμός|Population)\s*([\d\.,\s]+)",
            "Έκταση": r"(?:Έκταση|Area)\s*([\d\.,\s]+)\s*(?:km²|χλμ²)",
            "Χώρα/Περιφέρεια": r"(?:Χώρα|Country|Περιφέρεια)\s*([A-Z\u0386-\u03AB][a-z\u03AC-\u03CE]+(?:\s[A-Z\u0386-\u03AB][a-z\u03AC-\u03CE]+)*)",
            "Συντεταγμένες": r"(\d{1,3}°\d{1,2}′(?:\d{1,2}″)?[NS]\s*\d{1,3}°\d{1,2}′(?:\d{1,2}″)?[EW])",
            "Υψόμετρο": r"(?:Υψόμετρο|Elevation)\s*([\d\.,\s]+)\s*?(?:m|μέτρα|meters)",
            "Ζώνη ώρας": r"((?:UTC|GMT)\s*[+-]\d{1,2})",
        },

        "first_heading_text": {
            "Όνομα": r"([A-Z\u0386-\u03AB][a-z\u03AC-\u03CE\s]+)",
        },

        "average_temperature_text": {
            "Θερμοκρασία (Μέση)": r"(\d{1,2}(?:\.\d)?)\s*(?:°C|°F)"
        },
    }

    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        results[key] = match.group(1).strip() if match else "Δεν βρέθηκε"

    return results


if __name__ == "__main__":
    user_url = input("Εισάγετε το URL της Wikipedia για μια πόλη: ")
    data = scrape_city_info(user_url)
    
    print("\n--- Αποτελέσματα Εξαγωγής ---")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print(data)