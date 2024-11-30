import json
import requests
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError

API_ADDRESS = 'https://speller.yandex.net/services/spellservice.json/checkText'
LANGUAGE = 'ru'
OPTIONS = 526
FORMAT = 'html'

def descriptions_enumeration(root: ET.Element):
    """Цикл по элементам
    """
    offers = root.findall('.//offer')
    for offer in offers:
        idx = offer.attrib['id']
        try:
            idx = int(idx)
        except ValueError:
            print("Поле <<id>> имеет недопустимое значение.")
        description = offer.find('description').text
        spelling_check(description)

def spelling_check(raw_text: str) -> str:
    """Отправляет запрос для проверки орфографии
    """
    query_params = dict(
        text = raw_text,
        lang = LANGUAGE,
        options = OPTIONS,
        format = FORMAT,
    )
    while True:
        try:
            response = requests.get(url=API_ADDRESS, params=query_params)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'Ошибка подключения: {http_err}')
            continue
        except Exception as err:
            print(f'Неизвестная ошибка системы проверки орфографии: {err}')
            continue
        else:
            json_array = response.json()
            if json_array:
                print(raw_text)
                return processing_spelling_errors(json_array, raw_text)
            return '0'
        
    
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