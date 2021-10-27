import requests
import inspect

URL_API = "https://kinopoiskapiunofficial.tech"
API_KEY = "14cc3ea4-5777-4de1-b893-673a60e3aaa4"


class Film:
    @staticmethod
    def films_to_output_format(response):
        return [Film(film_hash) for film_hash in response["films"]]

    @staticmethod
    def print_films(films):
        for film_hash in films: print(f"{film_hash}\n")

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        
    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}"

    def print_film(self, films):
        for film in films: print(f"{film}\n")


def selection_from_films(choice_api: str, parameters: dict):
    response = requests.get(
        URL_API + choice_api,
        params=parameters,
        headers={
            "Content-type": "application/json",
            "X-API-KEY": API_KEY
        }
    ).json()
    return response

def film_show(choice_api: str, parameters: dict):
    global pages_number
    while True:
        response = selection_from_films(choice_api, parameters)
        films = Film.films_to_output_format(response)
        Film.print_films(films)
        if pages_number == response["pagesCount"]: break  # вывели последнюю страницу
        choice_print = input("Вывести следующую страницу?\n1.Да\n2.Нет\n")
        if choice_print == "2":
            return
        pages_number +=1

print(inspect.cleandoc("""Что хотите посмотреть?
                       1. ТОП фильмов
                       2. Выбрать фильмы по жанру"""))
choice_show = input()

if choice_show == '1':
    pages_number = 1
    film_show('/api/v2.2/films/top', {"page": pages_number})

elif choice_show == '2':
    response = selection_from_films('/api/v2.1/films/filters', {})
    genres = response['genres']
    print('В нашем списке фильмов есть следующие жанры:')
    for i in genres: print(i['genre'])
    choice_genre = input('Какой жанр хотите посмотреть? ')
    for genre in genres:
        if genre['genre'] == choice_genre:
            parameter_id = genre['id']
            break
    else:
        print('Такого жанра в нашем списке нет')
        raise SystemExit

    pages_number = 1
    film_show('/api/v2.1/films/search-by-filters', 
              {"page": pages_number, "genre": parameter_id})
