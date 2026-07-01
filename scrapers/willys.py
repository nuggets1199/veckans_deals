def get_offers():
    """
    Hämtar erbjudanden för Willys.
    Detta är initialt mock-data.
    """
    return [
        {
            "store": "Willys",
            "product": "Garant Ekologisk Banan",
            "price": "21,90 kr/kg",
            "discount": "Willys Plus",
            "image_url": "https://images.unsplash.com/photo-1571501715214-368297b8bb5a?auto=format&fit=crop&w=300&q=80",
            "brand": "Garant"
        },
        {
            "store": "Willys",
            "product": "Fryst Kycklingbröstfilé",
            "price": "89,00 kr/kg",
            "discount": "Veckans kampanj",
            "image_url": "https://images.unsplash.com/photo-1604503468506-a8da13d82791?auto=format&fit=crop&w=300&q=80",
            "brand": "Kronfågel"
        },
        {
            "store": "Willys",
            "product": "Pasta Penne",
            "price": "14,90 kr/st",
            "discount": "Klipp!",
            "image_url": "https://images.unsplash.com/photo-1551462147-ff29053bfc14?auto=format&fit=crop&w=300&q=80",
            "brand": "Barilla"
        }
    ]
