import requests

URL_API = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
API_KEY = "14cc3ea4-5777-4de1-b893-673a60e3aaa4"


class Film:
    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        
    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}"

    def selection_top_films(self)                                                                                                                                                                                                                                                                                                                                                                                                      ):
        response = requests.get(
            URL_API,
            params={"page": 1},
            headers={
                "Content-type": "application/json",
                "X-API-KEY": API_KEY
            }
        ).json()

        count_pages = response["pagesCount"]
        for page in count_pages:
            films = []
            for film_hash in response["films"]:
                film = Film(film_hash)
                films.append(film)
            yield films

for film in Film.selection_top_films():
    print(f"{film}\n")
