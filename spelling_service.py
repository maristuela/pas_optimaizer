import json
import requests
from requests.exceptions import HTTPError

API_ADDRESS = 'https://speller.yandex.net/services/spellservice.json/checkText'
LANGUAGE = 'ru'
OPTIONS = 526
FORMAT = 'html'
# CALLBACK = 'callback'

def spelling_check(raw_text: str) -> str:
    """Отправляет запрос для проверки орфографии
    """
    query_params = dict(
        text = raw_text,
        lang = LANGUAGE,
        options = OPTIONS,
        format = FORMAT,
        # callback = CALLBACK
    )
    try:
        response = requests.get(url=API_ADDRESS, params=query_params)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Ошибка подключения: {http_err}')
    except Exception as err:
        print(f'Неизвестная ошибка системы проверки орфографии: {err}')
    else:
        with open("response.json", "w", encoding='utf-8') as write_file:
            json.dump(response.json(), write_file, indent=4, ensure_ascii=False)
        return processing_spelling_errors(response.json(), raw_text)
        
    

def processing_spelling_errors(json_array: list, raw_text: str) -> str:
    """Обрабатывает орфографические ошибки
    """
    new_string = raw_text
    for spelling_error in json_array:
        while True:
            print(f"Рекомендуется исправить слово {spelling_error['word']} на {spelling_error['s']}")
            answer = input("Какой вариант вы выберете?[Номер предложенного варианта/Оставить/Другое]\n")
            if answer == 'Оставить':
                break
            if answer == 'Другое':
                user_value = input("Введите свой вариант: ")
                new_string = new_string.replace(spelling_error['word'], user_value)
                break
            if answer.isdigit():
                answer = int(answer)
                try:
                    if not answer:
                        raise IndexError
                    new_string = new_string.replace(spelling_error['word'], spelling_error['s'][answer-1])
                except IndexError:
                    print("Не найдено варианта с таким номером")
                    continue
                else:
                    break
            print("Неверный ввод")
                
    return new_string