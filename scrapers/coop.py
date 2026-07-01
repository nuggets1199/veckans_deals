def get_offers():
    """
    Hämtar erbjudanden för Coop.
    Detta är initialt mock-data.
    """
    return [
        {
            "store": "Coop",
            "product": "Änglamark Ekologiska Ägg",
            "price": "34,90 kr/förp",
            "discount": "Medlemspris",
            "image_url": "https://images.unsplash.com/photo-1587486913049-53fc88980cfc?auto=format&fit=crop&w=300&q=80",
            "brand": "Änglamark"
        },
        {
            "store": "Coop",
            "product": "Färsk Laxfilé",
            "price": "199,00 kr/kg",
            "discount": "Veckans klipp",
            "image_url": "https://images.unsplash.com/photo-1499125562588-29fb8a56b5d5?auto=format&fit=crop&w=300&q=80",
            "brand": "Fiskdisken"
        },
        {
            "store": "Coop",
            "product": "Kaffe Mellanrost",
            "price": "39,90 kr/st",
            "discount": "Medlemspris",
            "image_url": "https://images.unsplash.com/photo-1559525839-b184a4d698c7?auto=format&fit=crop&w=300&q=80",
            "brand": "Gevalia"
        }
    ]
