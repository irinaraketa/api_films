import requests
import inspect

URL_API = "https://kinopoiskapiunofficial.tech"
API_KEY = "14cc3ea4-5777-4de1-b893-673a60e3aaa4"


class Film:
    @staticmethod
    # get_films название смотрится получше
    def films_to_output_format(all_films):
        return [Film(film_hash) for film_hash in all_films]

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        
    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}"

class ConsoleInterface:
    def print_films(films):
        for film_hash in films: print(f"{film_hash}\n")

    def print_type_films(array, type_film):
        for i in array: print(i[type_film])


def get_requests(choice_api: str, parameters: dict):
    return requests.get(
        URL_API + choice_api,
        params=parameters,
        headers={
            "Content-type": "application/json",
            "X-API-KEY": API_KEY
        }
    ).json()

def get_films(choice_api: str, parameters: dict):
    pages_number = 1
    all_films = []
    while True:
        parameters |= {"page": pages_number}
        response = get_requests(choice_api, parameters)
        all_films.extend(response['films']) 
        if pages_number == response["pagesCount"]:  # последняя страница
            break
        pages_number +=1
    return all_films


print(inspect.cleandoc("""Что хотите посмотреть?
                       1. ТОП фильмов
                       2. Выбрать фильмы по жанру"""))
choice_show = input()

if choice_show == '1':
    all_films = get_films('/api/v2.2/films/top', {})
elif choice_show == '2':
    response = get_requests('/api/v2.1/films/filters', {})
    genres = response['genres']
    print('В нашем списке фильмов есть следующие жанры:')
    ConsoleInterface.print_type_films(genres, 'genre')
    choice_genre = input('Какой жанр хотите посмотреть? ')
    for genre in genres:
        if genre['genre'] == choice_genre:
            parameter_id = genre['id']
            break
    else:
        print('Такого жанра в нашем списке нет')
        raise SystemExit

    all_films = get_films('/api/v2.1/films/search-by-filters', 
                          {"genre": parameter_id})

films = Film.films_to_output_format(all_films)
ConsoleInterface.print_films(films)
