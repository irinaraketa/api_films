import requests
import inspect

URL_API = "https://kinopoiskapiunofficial.tech"
API_KEY = "14cc3ea4-5777-4de1-b893-673a60e3aaa4"


class Film:
    @staticmethod
    def films_to_output_format(all_films):
        return [Film(film_hash) for film_hash in all_films]

    @staticmethod
    def print_films(films_iter, number_films: int) -> bool:
        # Распечатать number_films фильмов. 
        # Есои иттерация завершиться, вернет False
        for i in range(number_films):
            try:
                print(f"{next(films_iter)}\n")
            except StopIteration:
                return False
        return True

    def __init__(self, film_hash):
        self.title = film_hash["nameRu"]
        self.year = film_hash["year"]
        
    def __str__(self):
        return f"Название: {self.title}\nГод: {self.year}"


def selection_from_films(choice_api: str, parameters: dict, flag: bool):
    pages_number = 1
    all_films = []
    while True:
        response = requests.get(
            URL_API + choice_api,
            params=parameters | {"page": pages_number},
            headers={
                "Content-type": "application/json",
                "X-API-KEY": API_KEY
            }
        ).json()
        if flag:
            return response
        all_films.extend(response['films']) 
        if pages_number == response["pagesCount"]: 
            break # вывели последнюю страницу
        pages_number +=1
    return all_films

print(inspect.cleandoc("""Что хотите посмотреть?
                       1. ТОП фильмов
                       2. Выбрать фильмы по жанру"""))
choice_show = input()

if choice_show == '1':
    all_films = selection_from_films('/api/v2.2/films/top', {}, False)
elif choice_show == '2':
    response = selection_from_films('/api/v2.1/films/filters', {}, True)
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

    all_films = selection_from_films('/api/v2.1/films/search-by-filters', 
                                     {"genre": parameter_id}, False)

films = Film.films_to_output_format(all_films)
films_iter = iter(films)

flag = True
while flag:
    flag = Film.print_films(films_iter, 5)
    if not flag:
        print('Больше фильмов нет')
        break
    choice_print = input("Вывести следующую страницу?\n1.Да\n2.Нет\n")
    if choice_print == "2":
        break
