import requests


# Willys butik att hämta erbjudanden för
# Uppsala Björkgatan store code is 2110
STORE_ID = "2110"
STORE_NAME = "Willys"

API_URL = "https://www.willys.se/axfood/rest/v1/search/campaigns/offline"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

IMAGE_BASE = "https://assets.axfood.se/image/upload/f_auto,t_200/"


def _parse_offer(item: dict) -> dict:
    """Konvertera ett Willys-erbjudande till vårt standardformat."""
    promos = item.get("potentialPromotions", [])

    # Bygg prissträng från kampanjinfo
    price_str = item.get("price", "")
    condition = ""
    if promos:
        promo = promos[0]
        reward = promo.get("rewardLabel", "")
        cond = promo.get("conditionLabelFormatted", "") or promo.get("conditionLabel", "")
        if cond and reward:
            price_str = f"{cond} {reward}"
        elif reward:
            price_str = reward

        condition = promo.get("campaignType", "")

    # Bild-URL
    image_url = ""
    img = item.get("image") or item.get("thumbnail")
    if img:
        img_url = img.get("url", "")
        if img_url.startswith("http"):
            image_url = img_url
        elif img_url.startswith("/"):
            image_url = f"https://www.willys.se{img_url}"

    return {
        "store": STORE_NAME,
        "product": item.get("name", "Okänd produkt"),
        "brand": item.get("manufacturer", ""),
        "price": price_str,
        "discount": condition,
        "description": item.get("displayVolume", ""),
        "image_url": image_url,
        "category": "",
        "restriction": "",
    }


def get_offers() -> list[dict]:
    """Hämtar veckans erbjudanden från Willys via kampanj-API:et."""
    all_offers = []
    page = 0
    page_size = 100

    try:
        while True:
            params = {
                "q": STORE_ID,
                "type": "PERSONAL_GENERAL",
                "page": page,
                "size": page_size,
            }

            response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            if not results:
                break

            for item in results:
                parsed = _parse_offer(item)
                all_offers.append(parsed)

            # Kolla om det finns fler sidor
            pagination = data.get("pagination", {})
            total_pages = pagination.get("numberOfPages", 1)

            page += 1
            if page >= total_pages:
                break

    except Exception as e:
        print(f"Fel vid hämtning av Willys-erbjudanden: {e}")

    return all_offers
