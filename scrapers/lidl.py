def get_offers():
    """
    Hämtar erbjudanden för Lidl.
    Detta är initialt mock-data.
    """
    return [
        {
            "store": "Lidl",
            "product": "Äpple Gala",
            "price": "19,90 kr/kg",
            "discount": "Superklipp",
            "image_url": "https://images.unsplash.com/photo-1560806887-1e4cd0b6fac6?auto=format&fit=crop&w=300&q=80",
            "brand": "Svenska"
        },
        {
            "store": "Lidl",
            "product": "Toalettpapper 8-pack",
            "price": "35,00 kr/förp",
            "discount": "Lidl Plus",
            "image_url": "https://images.unsplash.com/photo-1584556812952-905ffd0c611a?auto=format&fit=crop&w=300&q=80",
            "brand": "Floralys"
        },
        {
            "store": "Lidl",
            "product": "Grillkorv",
            "price": "29,90 kr/förp",
            "discount": "Helgkampanj",
            "image_url": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?auto=format&fit=crop&w=300&q=80",
            "brand": "Dulano"
        }
    ]
