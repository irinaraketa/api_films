import requests

URL_API = "https://kinopoiskapiunofficial.tech"
API_KEY = "14cc3ea4-5777-4de1-b893-673a60e3aaa4"


class Film:
    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        
    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}"

    def selection_films(self, api_choice)                                                                                                                                                                                                                                                                                                                                                                                                      ):
        response = requests.get(
            api_choice,
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

    def print_film(self, films):
        for film in films: print(f"{film}\n")

films = Film.selection_top_films(URL_API + '/api/v2.2/films/top')
Film.print_film(films)
