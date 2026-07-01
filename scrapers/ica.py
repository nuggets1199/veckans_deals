import requests
from bs4 import BeautifulSoup
import re
import json


# ICA butiker att hämta erbjudanden för
STORES = {
    "ICA Nära Råbyvägen": "https://www.ica.se/erbjudanden/ica-nara-rabyvagen-1003963/",
    "ICA Supermarket Torgkassen": "https://www.ica.se/erbjudanden/ica-supermarket-torgkassen-1003821/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "sv-SE,sv;q=0.9",
}


def _parse_initial_data(html: str) -> dict | None:
    """Extrahera window.__INITIAL_DATA__ från HTML och parsa till dict."""
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", string=re.compile(r"window\.__INITIAL_DATA__"))
    if not script or not script.string:
        return None

    match = re.search(r"window\.__INITIAL_DATA__\s*=\s*(\{.*\});?", script.string)
    if not match:
        return None

    json_str = match.group(1)
    if json_str.endswith(";"):
        json_str = json_str[:-1]

    # Fixa JavaScript-specifika värden som inte är giltig JSON
    json_str = re.sub(r":\s*undefined", ":null", json_str)
    json_str = re.sub(r"new\s+Map\(\[.*?\]\)", "{}", json_str)

    return json.loads(json_str)


def _parse_offer(offer: dict, store_name: str) -> dict:
    """Konvertera ett ICA-erbjudande till vårt standardformat."""
    details = offer.get("details", {})
    mechanics = offer.get("parsedMechanics", {})
    stores = offer.get("stores", [])
    eans = offer.get("eans", [])

    # Bygg prissträng
    price_parts = []
    if mechanics.get("value1"):
        price_parts.append(mechanics["value1"])
    if mechanics.get("value2"):
        price_parts.append(mechanics["value2"])
    price_str = " ".join(price_parts)
    if mechanics.get("unitSign"):
        price_str += mechanics["unitSign"]
    if mechanics.get("value3"):
        price_str += mechanics["value3"]

    # Ordinarie pris
    regular_price = ""
    if stores:
        regular_price = f"Ord.pris {stores[0].get('regularPrice', '')} kr"

    # Bild-URL
    image_url = ""
    if eans:
        image_url = eans[0].get("image", "")

    return {
        "store": store_name,
        "product": details.get("name", "Okänd produkt"),
        "brand": details.get("brand", ""),
        "price": price_str or "Se butik",
        "discount": regular_price,
        "description": details.get("packageInformation", ""),
        "image_url": image_url,
        "category": offer.get("category", {}).get("articleGroupName", ""),
        "restriction": offer.get("restriction", ""),
    }


def get_offers() -> list[dict]:
    """Hämtar veckans erbjudanden från alla konfigurerade ICA-butiker."""
    all_offers = []

    for store_name, url in STORES.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            data = _parse_initial_data(response.text)
            if not data:
                continue

            weekly_offers = data.get("offers", {}).get("weeklyOffers", [])

            for offer in weekly_offers:
                parsed = _parse_offer(offer, store_name)
                all_offers.append(parsed)

        except Exception as e:
            print(f"Fel vid hämtning av ICA-erbjudanden ({store_name}): {e}")

    return all_offers
