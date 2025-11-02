import abc

AWARDS = {
    '3 Stars': '⭐⭐⭐',
    'Selected Restaurants': 'Selected Restaurants',
    '1 Star': '⭐',
    '2 Stars': '⭐⭐',
    'Bib Gourmand': 'Bib Gourmand (value-for-money award)',
}

FILTERS = [
    'Green Star 💚',
    'Premiação 🏆',
    # 'Preço 💰',
    'Lugar 🗺️',
    'Cozinha 🧑‍🍳',
    'Serviços 🥤'
]

class Filter(abc.ABC):
    def get_query_line(self) -> tuple[str, tuple]:
        """
        First item in return should be like: `AND Stars = '?'\n`
        Second item in return should be the value to be safely interpolated by SQL`
        """
        pass

class GreenStarFilter(Filter):
    def get_query_line(self) -> tuple[str, tuple]:
        return 'AND GreenStar = 1\n', ()

class AwardFilter(Filter):
    def __init__(self, award: str):
        self.award = award

    def get_query_line(self) -> tuple[str, tuple]:
        return f'AND Award = {self.award}\n', ()

class PriceFilter(Filter):
    def __init__(self, price: int):
        self.price = price

    def get_query_line(self) -> tuple[str, tuple]:
        return f'AND LENGTH(Price) <= {self.price}\n', ()

class LocationFilter(Filter):
    def __init__(self, location: str):
        self.location = location

    def get_query_line(self) -> tuple[str, tuple]:
        return f'AND Location LIKE ?\n', (f'%{self.location}%',)

class CuisineFiler(Filter):
    def __init__(self, cuisine: str):
        self.cuisine = cuisine

    def get_query_line(self) -> tuple[str, tuple]:
        return f'AND Cuisine LIKE ?\n', (f'%{self.cuisine}%',)

class ServicesFilter(Filter):
    def __init__(self, services: str):
        self.services = services

    def get_query_line(self) -> tuple[str, tuple]:
        return f'AND FacilitiesAndServices LIKE ?\n', (f'%{self.services}%',)