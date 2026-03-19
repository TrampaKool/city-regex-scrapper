import re
import requests
from bs4 import BeautifulSoup

def scrape_city_info(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        return f"error: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    coords_span = soup.find('span', id='coordinates')
    coords_text = None

    if coords_span:
        coords_text = coords_span.get_text(strip=True)
    
    infobox = soup.find("table", {"class": "infobox"})
    if not infobox:
        return "infobox not found"
    

    infobox_text = infobox.get_text(separator=" ", strip=True)

    # find temperature table
    average_temperature_text = None
    tables = soup.find_all('table', {'class': 'wikitable'})

    climate_table = None

    for table in tables:
        if "Κλιματικά δεδομένα" in table.get_text():
            climate_table = table
            break

    if climate_table:

        rows = climate_table.find_all('tr')

        for row in rows:
            header_cell = row.find('th')

            if header_cell and "Μέση Μηνιαία" in header_cell.get_text():
                row_cells = row.find_all('td')

                last_cell = row_cells[-1] if row_cells else None
                if last_cell:
                    average_temperature_text = last_cell.get_text(strip=True)
    else:
        print("climate table not found.")

    #find first heading text
    first_heading = soup.find('h1', {'id': 'firstHeading'})
    first_heading_text = first_heading.get_text(strip=True) if first_heading else "Not found"

    patterns = {
        "infobox_text": {
            "Πληθυσμός": r"(?:Πληθυσμός|Population).*?(?:Municipality|Δήμος)*\s*([\d,\.]+)",
            "Έκταση": r"(?:Έκταση|Area).*?(?:Municipality|Δήμος)*\s*([\d\.,\s]+(?:km\s*[²2]|χλμ\s*[\s²2]))",
            "Χώρα/Περιφέρεια": r"(?:Χώρα|Country|Περιφέρεια)\s*([A-Z\u0386-\u03AB][a-z\u03AC-\u03CE\s]{1,20})",
            "Υψόμετρο": r"(?:Υψόμετρο|Elevation|Lowest elevation).*?([\d\.,\s]+(?:m|μέτρα|meters|μ\.?))",
            "Ζώνη ώρας": r"((?:UTC|GMT)\s*[+-]\d{1,2})",
        },

        "first_heading_text": {
            "Όνομα": r"([A-Z\u0386-\u03AB][a-z\u03AC-\u03CE\s]+)",
        },

        "average_temperature_text": {
            "Θερμοκρασία (Μέση)": r"(\d{1,2}(?:\.\d)?)\s*(?:°C|°F)"
        },

        "coords_text": {
            "Συντεταγμένες": r"(\d{1,3}°\d{1,2}′(?:\d{1,2}″)?[NS]\s*\d{1,3}°\d{1,2}′(?:\d{1,2}″)?[EW])",
        }
    }

    results = {}
    for key, pattern_dict in patterns.items():
        text = locals().get(key)
        if text:
            for label, pattern in pattern_dict.items():
                match = re.search(pattern, text)
                if match:
                    results[label] = match.group(1).strip()
                else:
                    results[label] = "Not found"
        else:
            for label in pattern_dict.keys():
                results[label] = "Not found"

    return results


if __name__ == "__main__":
    user_url = input("Εισάγετε το URL της Wikipedia για μια πόλη: ")
    data = scrape_city_info(user_url)
    
    print("\n--- Αποτελέσματα ---")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print(data)