import requests
import re

API_URL = "https://www.lidl.se/q/api/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*"
}

def _extract_restriction(data_dict: dict) -> str:
    """Extraherar datum/giltighetstid för erbjudandet."""
    stock_avail = data_dict.get("stockAvailability", {})
    if isinstance(stock_avail, dict):
        badges = stock_avail.get("badgeInfo", {}).get("badges", [])
        if badges and isinstance(badges, list):
            text = badges[0].get("text", "")
            if text:
                return text
        badges_v2 = stock_avail.get("badgeInfoV2", [])
        if isinstance(badges_v2, list) and badges_v2:
            inner_badges = badges_v2[0].get("badges", [])
            if inner_badges and isinstance(inner_badges, list):
                text = inner_badges[0].get("text", "")
                if text:
                    return text
    ribbons = data_dict.get("ribbons")
    if isinstance(ribbons, list) and ribbons:
        if isinstance(ribbons[0], dict):
            text = ribbons[0].get("text", "")
            if text:
                return text
        elif isinstance(ribbons[0], str):
            return ribbons[0]
    stickers = data_dict.get("stickers")
    if isinstance(stickers, list) and stickers:
        if isinstance(stickers[0], dict):
            text = stickers[0].get("text", "")
            if text:
                return text
        elif isinstance(stickers[0], str):
            return stickers[0]
    return ""

def get_offers() -> list[dict]:
    """Hämtar Lidl-erbjudanden via sök-API:et."""
    parsed_offers = []
    try:
        # q/api/search kräver version=1 för att undvika 400 Bad Request
        params = {
            "offset": "0",
            "fetchsize": "200",
            "locale": "sv_SE",
            "assortment": "SE",
            "category.id": "10068374",
            "version": "1"
        }
        
        response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        
        for item in items:
            gridbox = item.get("gridbox", {})
            if not gridbox:
                continue
            data_dict = gridbox.get("data", {})
            if not data_dict:
                continue
                
            # 1. store
            store = "Lidl"
            
            # 2. product
            product = data_dict.get("fullTitle") or data_dict.get("title") or "Okänd produkt"
            
            # 3. brand
            brand_obj = data_dict.get("brand", {})
            brand = ""
            if isinstance(brand_obj, dict):
                brand = brand_obj.get("name", "")
            elif isinstance(brand_obj, str):
                brand = brand_obj
                
            # 4. discount & price & description (packaging)
            price_dict = data_dict.get("price", {})
            price_num = price_dict.get("price") if isinstance(price_dict, dict) else None
            normal_price_num = price_num  # Spara originalpriset
            
            discount = ""
            original_price = ""
            discount_percentage = 0
            lidl_plus = data_dict.get("lidlPlus")
            if lidl_plus and isinstance(lidl_plus, list):
                discount = "Lidl Plus"
                # Om ordinarie pris saknas, använd Lidl Plus-priset
                if price_num is None and len(lidl_plus) > 0:
                    lp_price_dict = lidl_plus[0].get("price", {})
                    price_num = lp_price_dict.get("price")
                    price_dict = lp_price_dict
                
                # Extrahera rabattprocent från highlightText (t.ex. "KUPONG -23%")
                if len(lidl_plus) > 0:
                    highlight = lidl_plus[0].get("highlightText", "")
                    pct_match = re.search(r'(\d+)\s*%', highlight)
                    if pct_match:
                        discount_percentage = int(pct_match.group(1))
                    
                    # Beräkna procent från normal pris vs Lidl Plus-pris om highlight saknas
                    if discount_percentage == 0 and normal_price_num is not None:
                        lp_price = lidl_plus[0].get("price", {}).get("price")
                        if lp_price is not None:
                            try:
                                orig = float(normal_price_num)
                                deal = float(lp_price)
                                if orig > 0 and deal < orig:
                                    discount_percentage = round((1 - deal / orig) * 100)
                            except (ValueError, TypeError, ZeroDivisionError):
                                pass
                    
                    # Sätt originalpris-strängen om vi har ett normalpris
                    if normal_price_num is not None:
                        try:
                            orig_val = float(normal_price_num)
                            if orig_val.is_integer():
                                original_price = f"{int(orig_val)}:- kr"
                            else:
                                original_price = f"{orig_val:.2f} kr".replace(".", ",")
                        except (ValueError, TypeError):
                            pass
                    
            if price_num is not None:
                try:
                    price_val = float(price_num)
                    if price_val.is_integer():
                        price_str = f"{int(price_val)}:-"
                    else:
                        price_str = f"{price_val:.2f}".replace(".", ",")
                        if price_str.endswith(",00"):
                            price_str = price_str.replace(",00", ":-")
                        else:
                            price_str = price_str + "/st"
                except Exception:
                    price_str = str(price_num)
            else:
                price_str = "Se pris i butik"
                
            description = price_dict.get("packaging", {}).get("text", "") if isinstance(price_dict, dict) else ""
            
            # 5. image_url
            image_url = data_dict.get("image", "")
            
            # 6. category
            category = ""
            
            # 7. restriction
            restriction = _extract_restriction(data_dict)
            
            parsed_offers.append({
                "store": store,
                "product": product,
                "brand": brand,
                "price": price_str,
                "discount": discount,
                "description": description,
                "image_url": image_url,
                "category": category,
                "restriction": restriction,
                "original_price": original_price,
                "discount_percentage": discount_percentage,
            })
            
    except Exception as e:
        print(f"Fel vid hämtning av Lidl-erbjudanden: {e}")
        
    return parsed_offers
