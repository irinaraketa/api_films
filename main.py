import requests
import inspect

URL_API = "https://kinopoiskapiunofficial.tech"
API_KEY = "14cc3ea4-5777-4de1-b893-673a60e3aaa4"


class Film:
    @staticmethod
    def get_films(all_films):
        return [Film(film_hash) for film_hash in all_films]

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        self.rating = film_hash["rating"]
        
    def __str__(self):
        return inspect.cleandoc(f"""Название: {self.title} 
                Год: {self.year}
                Рейтинг: {self.rating}""")

class Cinema:
    def __init__(self, all_films):
        self.all_films = all_films

    def sort_films(self, sorting_criteria: str):
        return self.all_films.sort(key=lambda x: x[sorting_criteria])

    def search_name(self, name_film: str) -> dict:
        return list(filter(lambda x: x['nameRu'] == name_film, self.all_films))

class ConsoleInterface:
    def print_films(films):
        for film_hash in films: print(f"{film_hash}\n")

    def print_type_films(array, type_film):
        for i in array: print(i[type_film])

    def print_pages(films, number_films_on_page):
        total_films = len(films)
        for film_hash in films[0 : number_films_on_page]: 
            print(f"{film_hash}\n")
        current_number = number_films_on_page - 1  # номер элемента в 
        # массиве на котором находимся
        while True:
            if number_films_on_page - 1 < current_number < total_films:
                print(inspect.cleandoc("""1.Предыдущая страница
                                          2.Следующая страница
                                          3.Выход"""))
                choice_print = input()
            elif current_number >= total_films:
                choice_print = input("1.Предыдущая страница\n3.Выход\n")
            else:
                choice_print = input("2.Следующая страница\n3.Выход\n")
            if choice_print == '3':
                return
            elif choice_print == '1':
                for film_hash in films[current_number - 
                        number_films_on_page * 2 + 1: 
                        current_number - number_films_on_page + 1]: 
                    print(f"{film_hash}\n")
                current_number -= number_films_on_page
            else:
                for film_hash in films[current_number + 1: 
                        min(current_number + number_films_on_page + 1, 
                        total_films + 1)]: print(f"{film_hash}\n")
                current_number += number_films_on_page


def send_request(choice_api: str, parameters: dict):
    return requests.get(
        URL_API + choice_api,
        params=parameters,
        headers={
            "Content-type": "application/json",
            "X-API-KEY": API_KEY
        }
    ).json()

def get_films_response(choice_api: str, parameters: dict):
    pages_number = 1
    all_films = []
    while True:
        parameters |= {"page": pages_number}
        response = send_request(choice_api, parameters)
        all_films.extend(response['films']) 
        if pages_number == response["pagesCount"]:  # последняя страница
            break
        pages_number +=1
    return all_films


print(inspect.cleandoc("""Что хотите посмотреть?
                       1. ТОП фильмов
                       2. Выбрать фильмы по жанру
                       3. Поиск ТОП фильма по названию"""))
choice_show = input()

if choice_show == '1':
    all_films = get_films_response('/api/v2.2/films/top', {})
    cinema = Cinema(all_films)
    cinema.sort_films('year')
    films = Film.get_films(all_films)
    ConsoleInterface.print_films(films)

elif choice_show == '2':
    response = send_request('/api/v2.1/films/filters', {})
    genres = response['genres']
    print('В нашем списке фильмов есть следующие жанры:')
    ConsoleInterface.print_type_films(genres, 'genre')
    choice_genre = input('Какой жанр хотите посмотреть? ')

    try:  # поиск по жанру
        parameter_id = list(filter(lambda x: x['genre'] == choice_genre, 
                       genres))[0]['id']
    except IndexError:
        print('Такого жанра в нашем списке нет')
        raise SystemExit

    all_films = get_films_response('/api/v2.1/films/search-by-filters', 
                          {"genre": parameter_id})
    cinema = Cinema(all_films)
    cinema.sort_films('rating')
    films = Film.get_films(all_films)
    if len(films) > 5:
        ConsoleInterface.print_pages(films, 5)
    else:
        ConsoleInterface.print_films(films)

elif choice_show == '3':
    name_film = input('Введите название фильма: ')
    all_films = get_films_response('/api/v2.2/films/top', {})
    cinema = Cinema(all_films)
    found_film = cinema.search_name(name_film)
    if found_film:
        found_film = Film.get_films(found_film)
        ConsoleInterface.print_films(found_film)
    else:
        print('Такого фильма нет')
