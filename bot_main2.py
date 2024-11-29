import telebot
import os
import requests
from urllib.parse import urlencode

import pandas as pd
import xml.etree.ElementTree as ET
import sys
import zipfile
import yadisk


y = yadisk.YaDisk(token="y0_AgAAAABogsCFAAzdlQAAAAEaXuWrAADPRipOtMJIdarwjBAm_jMjcf2SYA")




keybred = 1

bot = telebot.TeleBot('7216725010:AAGgec15kB4cjSmIe3hlHouOiaYRqXe5EB4')

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton(text='Загрузить фид в формате XML', callback_data="new"))
key = " "


required_fields = [
    'price',
    'currencyId',
    'categoryId',
    'picture',
    'name',
    'vendor',
    'description',
    'barcode'
]


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)

    bot.send_message(message.chat.id, 'Привет, я твой персональный помошник в проферки твоих фидов.')
    menu(message.chat.id)



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global key
    if (call.data == "new"):
        bot.send_message(call.message.chat.id, 'Введите ссылку на яндекс диск')
        key = "url"



@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        project_directory = 'D:/exel_python/'
        # Создаем полный путь к файлу
        file_path = os.path.join(project_directory, message.document.file_name)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, str(e))



@bot.message_handler(content_types=['text'])
def text(message):
    print(message.text)
    if key == "url":
        try:
            public_key = message.text  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            response = requests.get(final_url)
            download_url = response.json()['href']
            print("Ожидайте, мы работаем с данными")
            bot.send_message(message.chat.id, "Ожидайте мы работаем с данными")
            # Загружаем файл и сохраняем его
            download_response = requests.get(download_url)
            print(download_response.content)
            with open('azz.xml', 'wb') as f:  # Здесь укажите нужный путь к файлу
                f.write(download_response.content)

            # Пример XML данных

            # Парсинг XML данных
            root = ET.fromstring(download_response.content)


            def check_required_fields(root, required_fields):
                errors = []

                for product in root.findall('product'):
                    for field in required_fields:
                        # Проверяем наличие обязательного поля
                        element = product.find(field)
                        if element is None or element.text is None or element.text.strip() == '':
                            errors.append(
                                f"Ошибка в элементе <product>: отсутствует или пусто обязательное поле '{field}'")

                return errors

            # Проверяем XML данные на наличие обязательных полей
            error_messages = check_required_fields(root, required_fields)

            # Обработка ошибок
            if error_messages:
                print("Найдены ошибки:")
                for error in error_messages:
                    print(f"- {error}")
            else:
                print("Все обязательные поля присутствуют и заполнены корректно.")

            # Загружаем XML
            tree = ET.parse('azz.xml')  # Убедитесь, что файл с данными называется 'azz.xml'
            root = tree.getroot()

            # Находим все элементы offer
            offers = root.findall('.//offer')
            #
            # Проверяем поля

            # Проверяем поля
            check_offer_fields(offers, message.chat.id, tree)

            process_offers(tree)
            # xml_file_path = 'azz_updated.xml'


            # send_file(message.chat.id)

            print('!!!!!!!!!'
                  '!!!!!!!!!!!!!!!!!!!!!!!!!!!', root.find('.//shop/name').text)
            try_file("azz_updated.xml", root.find('.//shop/name').text, message.chat.id)




            # Проверяем файл перед отправкой
            # if os.path.exists(xml_file_path) and os.path.getsize(xml_file_path) > 0:
            #     with open(xml_file_path, 'rb') as file:  # Открываем в режиме чтения
            #         bot.send_document(message.chat.id, file)  # Отправляем файл
            # else:
            #     bot.send_message(message.chat.id, "Ошибка: файл пуст или не существует.")


        except KeyError as e :
            bot.send_message(message.chat.id, "Введина не верная ссылка")
            print("Введина не верная ссылка")

        except ConnectionError as e:
            print("Не удалось установить соединение с сервером")


        except ET.ParseError:
            print(
                "Невозможно прочитать файл. Убедитесь, что файл имеет расширение xml и все теги определяются правильно.")
            bot.send_message(message.chat.id, "Фаил имеет не закрытые файлы.")
        except FileNotFoundError:
            print("Файл не найден по данному адресу")
            bot.send_message(message.chat.id, "Файл не найден по данному адресу")

        except ConnectionError as e:
            print("Ошибка подключения")


        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(f"An error occurred: {exc_value}")
            print(f"Exception type: {exc_type.__name__}")  # Выводим имя типа исключения



def menu(id):
    bot.send_message(id, text="Чем я могу помочь?", reply_markup=markup)


# Функция для проверки наличия ключевых полей в каждом offer
def check_offer_fields(offers, user_id, tree):
    global keybred
    # Сначала обрабатываем все предложения
    xml_file_path = 'azz_updated.xml'
    for idx, offer in enumerate(offers, start=1):
        for field in required_fields:
            element = offer.find(field)
            field_value = element.text.strip() if element is not None and element.text is not None else None

            # Проверяем, существует ли элемент
            if element is None:
                if keybred < 4:
                    print(f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")
                    bot.send_message(user_id, f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")
                    keybred = keybred + 1
                    # Запрашиваем у пользователя ввод значения для отсутствующего поля
                    user_input = input(f"Please enter value for '{field}': ")
                    # Создаем новый элемент и добавляем его в offer
                    new_element = ET.Element(field)
                    new_element.text = user_input
                    offer.append(new_element)
                    tree.write('azz_updated.xml', encoding='utf-8', xml_declaration=True)
                    print("Updated XML file has been saved as 'azz_updated.xml'.")

            # Проверяем, заполнено ли поле
            elif field_value is None or field_value == '':
                if keybred < 4:
                    keybred = keybred + 1
                    print(f"Warning: Offer ID '{offer.attrib.get('id')}' is missing '{field}' or it is empty.")
                    bot.send_message(user_id,
                                 f"Warning: Offer ID '{offer.attrib.get('id')}' is missing '{field}' or it is empty.")
                    # Запрашиваем у пользователя ввод значения для пустого поля
                    user_input = input(f"Please enter value for '{field}': ")
                    element.text = user_input
                    tree.write('azz_updated.xml', encoding='utf-8', xml_declaration=True)
                    print("Updated XML file has been saved as 'azz_updated.xml'.")

    # Записываем изменения в файл только один раз, после обработки всех предложений

    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
    print("Updated XML file has been saved as 'azz_updated.xml'.")



def process_offers(tree):
    # Получаем все предложения из дерева
    offers = tree.findall('.//offer')  # Используем XPath для нахождения всех offer
    all_fields_filled = True

    for idx, offer in enumerate(offers):
        params = offer.findall('param')

        # Проверка поля "Цена"
        price = offer.find('categoryId')
        price_value = price.text.strip() if price is not None else ''

        if not price_value:
            print(f"В предложении с id={offer.get('id')} поле <<Цена>> не заполнено.")
            all_fields_filled = False
        else:
            try:
                float_price = float(price_value)
                if float_price < 0:
                    price.text = '0'  # Обнуляем цену, если она отрицательная
                    print(f"Цена не может быть отрицательной. Значение обнулено в предложении с id={offer.get('id')}.")
            except ValueError:
                price.text = '0'  # Обнуляем цену в случае ошибки
                print(f"В предложении с id={offer.get('id')} поле <<Цена>> имеет недопустимое значение, заменено на 0.")

                # Проверка поля "Цена"
                price = offer.find('price')
                price_value = price.text.strip() if price is not None else ''

                if not price_value:
                    print(f"В предложении с id={offer.get('id')} поле <<Цена>> не заполнено.")
                    all_fields_filled = False
                else:
                    try:
                        float_price = float(price_value)
                        if float_price < 0:
                            price.text = '0'  # Обнуляем цену, если она отрицательная
                            print(
                                f"Цена не может быть отрицательной. Значение обнулено в предложении с id={offer.get('id')}.")
                    except ValueError:
                        price.text = '0'  # Обнуляем цену в случае ошибки
                        print(
                            f"В предложении с id={offer.get('id')} поле <<Цена>> имеет недопустимое значение, заменено на 0.")






        # Обработка других параметров!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!







        # Проверка остальных параметров (кроме "Новинка")
        for param in params:
            param_name = param.get('name')
            param_value = param.text.strip() if param.text is not None else ''

            if param_name == "Новинка":
                continue  # Пропустить поле "Новинка"

            if not param_value:
                print(f"В предложении с id={offer.get('id')} поле <<{param_name}>> не заполнено.")
                all_fields_filled = False

            # Проверка на числовой тип данных
            try:
                if param_value:  # Проверяем, что значение не пустое
                    float_value = float(param_value)

                    # Обработка полей для "Скидка"
                    if param_name == 'Скидка':
                        if float_value > 100 or float_value < 0:
                            param.text = '0'  # Обнуляем значение
                            print(
                                f"Скидка не может иметь значение больше 100 или меньше 0. Значение обнулено в предложении с id={offer.get('id')}.")
            except ValueError:
                param.text = '0'  # Обнуляем значение в случае ошибки
                print(
                    f"В предложении с id={offer.get('id')} поле <<{param_name}>> имеет недопустимое значение, заменено на 0.")

    # Сохранение изменений в новый XML-файл после обработки
    new_xml_file_path = 'azz_updated.xml'  # Имя файла для сохранения
    tree.write(new_xml_file_path, encoding='utf-8', xml_declaration=True)
    print(f"Измененный файл сохранен как '{new_xml_file_path}'.")









def try_file(local_file_path, name, id):
    # Проверяем, валиден ли токен
    bot.send_message(id, "Ожидайте, фаил с изменениями загружается на Яндекс диск")
    if not y.check_token():
        print("Токен недействителен!")
        return

    # Получаем общую информацию о диске
    disk_info = y.get_disk_info()
    print("Информация о диске:", disk_info)

    # Укажите путь к вашему XML-файлу и имя, под которым он будет сохранен на Яндекс Диск
    destination_file_path = "/" +name +".xml"  # Укажите имя файла на Яндекс Диске

    try:
        # Загружаем XML-файл на Яндекс Диск с перезаписью
        y.upload(local_file_path, destination_file_path, overwrite=True)
        print(f"Файл '{local_file_path}' успешно загружен на Яндекс Диск как '{destination_file_path}'.")

        # Получаем прямую ссылку на загруженный файл
        link = y.get_download_link(destination_file_path)
        print(f"Ссылка на файл: {link}")
        bot.send_message(id, f"Ссылка на файл: {link}")
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")








def save_xml_file(tree, xml_file_path):
    """Сохраняет XML-дерево в файл."""
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
    print(f"Updated XML file has been saved as '{xml_file_path}'.")





































def zip_file(input_file_path, output_zip_path):
    """Создает ZIP-архив из указанного файла."""
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_file_path, os.path.basename(input_file_path))

def create_xml():
    """Создает простое XML-дерево для демонстрации."""
    root = ET.Element("data")
    child = ET.SubElement(root, "item")
    child.text = "Пример содержимого"
    return ET.ElementTree(root)

def send_file(user_id):
    # Создаем XML-дерево
    tree = create_xml()

    # Путь к исходному XML-файлу
    xml_file_path = 'azz.xml'
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
    print("Updated XML file has been saved as 'azz_updated.xml'.")

    # Создаем ZIP-архив
    zip_file_path = 'azz.zip'
    zip_file(xml_file_path, zip_file_path)

    # Проверяем файл перед отправкой
    if os.path.exists(zip_file_path) and os.path.getsize(zip_file_path) > 0:
        try:
            with open(zip_file_path, 'rb') as file:  # Открываем ZIP-архив в режиме чтения
                bot.send_document(user_id, file)  # Отправляем файл
                print("ZIP-файл успешно отправлен.")
        except telebot.apihelper.ApiException as e:
            bot.send_message(user_id, f"Ошибка API: {e}")
        except ConnectionError:
            bot.send_message(user_id, "Ошибка: Нет соединения. Попробуйте позже.")
        except Exception as e:
            bot.send_message(user_id, f"Произошла ошибка при отправке файла: {e}")
    else:
        bot.send_message(user_id, "Ошибка: ZIP-файл пуст или не существует.")


bot.polling(none_stop=True)