import datetime

import telebot
import os
import requests
from urllib.parse import urlencode
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import pandas as pd
import xml.etree.ElementTree as ET
import sys
import zipfile
import yadisk

import input_required
import parser2 as parse
import chek_price
import pluse
import services_controller
import services.spelling_service as sp



FILE_PATH = 'azz.xml'
y = yadisk.YaDisk(token="y0_AgAAAABogsCFAAzdlQAAAAEaXuWrAADPRipOtMJIdarwjBAm_jMjcf2SYA")





bot = telebot.TeleBot('7216725010:AAGgec15kB4cjSmIe3hlHouOiaYRqXe5EB4')
file_path_txt = 'example.txt'

# with open(file_path_txt, 'a', encoding='utf-8') as file:
#     file.write("В предложении с id= 2 поле price не заполнено.\n")

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton(text='Загрузить фид в формате XML', callback_data="new"))
markup.add(telebot.types.InlineKeyboardButton(text='История загрузки фидов', callback_data="history"))
markup.add(telebot.types.InlineKeyboardButton(text='Проверка орфографии фидов', callback_data="gramm"))
markup.add(telebot.types.InlineKeyboardButton(text='Ссылка на сайт', callback_data="site"))
key = " "


required_fields = [
    'price',
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




@bot.message_handler(commands=['menu'])
def mune(message):
    menu(message.chat.id)



@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


        print(type(result))
        if result == datetime.date(2024,11,30):
            print(result)
            bot.send_message(c.message.chat.id, "В 04.22 : " + "https://downloader.disk.yandex.ru/disk/aca1b5e310016766d5f3d40dc6f800df916067b1a299cb3f6772d145f155e074/674ad526/tsoSpLVsca5S2BkApoGJ1EXtqrPG_ePN8GuEWWWYYakj3IqMtZY6Q8N_gC1s5VnkLa4xeYKq-bQs9bIUOK6lpA%3D%3D?uid=1753399429&filename=Your%20Shop%20Name.xml&disposition=attachment&hash=&limit=0&content_type=text%2Fxml&owner_uid=1753399429&fsize=22088838&hid=53ebe01aac06e41c2b5995db5b91dbf7&media_type=document&tknv=v2&etag=091eb33a17bd418f436219e997c134f5")
            bot.send_message(c.message.chat.id,
                             "В 04.56 : " +"https://downloader.disk.yandex.ru/disk/7258fa3a3dc9fa80555ddfe26454015384c38ccb6a6cb46a78453a56e568ce09/674a8b4a/tsoSpLVsca5S2BkApoGJ1Fh85LjPMoylQohr7g0-w0E_uM_d8LjUtAgssR1LdMePUvLFH8pvSgaL1x8NWbHP4Q%3D%3D?uid=1753399429&filename=Your%20Shop%20Name.xml&disposition=attachment&hash=&limit=0&content_type=text%2Fxml&owner_uid=1753399429&fsize=22086799&hid=e1dace8e07b70020a06001b8680e069b&media_type=document&tknv=v2&etag=71573c08fe29a1d84aa32d6187564676")
            bot.send_message(c.message.chat.id,
                             "В 05.50 : " +"https://downloader.disk.yandex.ru/disk/d6d6a69b686b2d5669b52b630deaa9c35cf6071a4853ed76d267b554d5db7b1b/674a7b33/tsoSpLVsca5S2BkApoGJ1EaVDpJMoNqwzudx7_uPOfcfL1NwZSUpeLvEF8w4PP17gjnwt229SHGS-tVhyUC6Jw%3D%3D?uid=1753399429&filename=Your%20Shop%20Name.xml&disposition=attachment&hash=&limit=0&content_type=text%2Fxml&owner_uid=1753399429&fsize=22088679&hid=aacb8b9a97308fbd48b322def825ec02&media_type=document&tknv=v2&etag=442a0a3c7de8d760c09e2b2ef33142f1")
        # if (oneDate == 0000-00-00):
        #     oneDate = result
        #     bot.edit_message_text("Выберите дату окончания периода",
        #                           c.message.chat.id,
        #                           c.message.message_id)
        #     date(c.message)
        # else:
        #     twoDate = result
        #     sqlite_select = f"""SELECT * FROM manager WHERE tg = {c.message.chat.id}"""
        #     con = sqlite3.connect('BdTrainingCenter.db')
        #     cursor = con.cursor()
        #     cursor.execute(sqlite_select)
        #     division = 0
        #     for row in cursor:
        #         division = row[2]


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global key
    if (call.data == "new"):
        bot.send_message(call.message.chat.id, 'Введите ссылку на яндекс диск')
        key = "url"
    if (call.data == "history"):
        bot.send_message(call.message.chat.id, 'Введите дату за которую нужно прислать обновленные файлы')
        bot.send_message(call.message.chat.id, 'Выберите дату начала периода')
        date(call.message)
        key = "date"
    if (call.data == "gramm"):
        bot.send_message(call.message.chat.id, 'Введите ссылку на яндекс диск')
        key = "gram_url"
    if (call.data == "site"):
        bot.send_message(call.message.chat.id, 'Ссылка на сайт - https://feedoptimizer.tilda.ws/')



@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    global key
    bot.send_message(message.chat.id, "Файл обрабатывается")
    try:
        print("dsokppffkfjfjvjfvfj")

        if key == 'plus':
            # Сначала получаем информацию о файле
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            project_directory = 'D:/проекты питон/МПИТ/'
            # Создаем полный путь к файлу
            file_path = os.path.join(project_directory, message.document.file_name)

            # Записываем загруженный файл
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Вызываем вашу функцию для обновления основного файла
            # Предполагаем, что 'new_fillings.xml' - это файл, полученный от пользователя
            pluse.update_xml_with_new_data('azz.xml', file_path)

            # Сообщаем пользователю об успешном обновлении
            bot.send_message(message.chat.id, "Файл успешно обновлён.")
            tree = ET.parse('azz.xml')  # Загружаем основной файл XML
            root = tree.getroot()
            bot.send_message(message.chat.id, "Обработка данных")
            if chek_price.check_offer_fields_and_create_new_xml(tree, root) > 0:
                send_xml_file(message.chat.id, 'new_fillings.xml')
                key = "plus"
            else:
                key = "two"
                offers = root.findall('.//offer')
                bot.send_message(message.chat.id, "Все обязательные поля заполнены")
                # Проверяем поля
                parse.check_offer_fields(offers, tree, root)

                # Проверяем поля
                check_offer_fields(offers, message.chat.id, tree)

                # chek_price.check_price_increase_from_file(tree, root, message.chat.id)  # Укажите путь к вашему XML файлу
                process_offers(tree, message.chat.id)

                print('!!!!!!!!!'
                      '!!!!!!!!!!!!!!!!!!!!!!!!!!!', root.find('.//shop/name').text)
                try_file("azz_updated.xml", root.find('.//shop/name').text, message.chat.id)



    except Exception as e:
        bot.reply_to(message, str(e))



@bot.message_handler(content_types=['text'])
def text(message):
    global key
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
            if (key == "url"):
                # check_offer_fields(offers, message.chat.id, tree)
                if chek_price.check_offer_fields_and_create_new_xml(tree,  root) > 0:
                    send_xml_file(message.chat.id, 'new_fillings.xml')
                    key = "plus"
                else:
                    # Проверяем поля
                    parse.check_offer_fields(offers, tree, root)

                    # Проверяем поля
                    check_offer_fields(offers, message.chat.id, tree)


                    # chek_price.check_price_increase_from_file(tree, root, message.chat.id)  # Укажите путь к вашему XML файлу
                    process_offers(tree, message.chat.id)

                    print('!!!!!!!!!'
                  '!!!!!!!!!!!!!!!!!!!!!!!!!!!', root.find('.//shop/name').text)
                    try_file("azz_updated.xml", root.find('.//shop/name').text, message.chat.id)

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


    elif key == "gram_url":
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
        key = "number"
        services_controller.service_startup()


    elif key == "number":
        print(message.text)



def menu(id):
    bot.send_message(id, text="Чем я могу помочь?", reply_markup=markup)


# Функция для проверки наличия ключевых полей в каждом offer
def check_offer_fields(offers, user_id, tree):
    # Сначала обрабатываем все предложения
    xml_file_path = 'azz_updated.xml'
    for idx, offer in enumerate(offers, start=1):
        for field in required_fields:
            element = offer.find(field)
            field_value = element.text.strip() if element is not None and element.text is not None else None

            # Проверяем, существует ли элемент
            if element is None:
                print(f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")
                bot.send_message(user_id, f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")
                with open(file_path_txt, 'a', encoding='utf-8') as file:  # Открываем файл в режиме добавления
                    file.write(f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.\n")
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


import xml.etree.ElementTree as ET

def process_offers(tree, id):
    # Получаем все предложения из дерева
    offers = tree.findall('.//offer')  # Используем XPath для нахождения всех offer
    all_fields_filled = True

    for idx, offer in enumerate(offers):
        params = offer.findall('param')

        # Проверка поля "categoryId"
        category_id = offer.find('categoryId')
        category_id_value = category_id.text.strip() if category_id is not None else ''

        if not category_id_value:
            print(f"В предложении с id={offer.get('id')} поле <<categoryId>> не заполнено.")
            bot.send_message(id, f"В предложении с id={offer.get('id')} поле <<categoryId>> не заполнено.")
            try:
                with open(file_path_txt, 'w', encoding='utf-8') as file:
                    file.write("В предложении с id={offer.get('id')} поле <<categoryId>> не заполнено.\n")
            except Exception as e:
                print(f"Ошибка при записи в файл: {e}")
            all_fields_filled = False
            category_id.text = '0'  # Обнуляем, если поле пустое
        else:
            try:
                float_category_id = float(category_id_value)
                if float_category_id < 0:
                    category_id.text = '0'  # Обнуляем, если значение отрицательное
                    print(f"Попытка установить отрицательное значение в поле <<categoryId>>. Значение обнулено в предложении с id={offer.get('id')}.")
            except ValueError:
                category_id.text = '0'  # Обнуляем при ошибке
                print(f"В предложении с id={offer.get('id')} поле <<categoryId>> имеет недопустимое значение, заменено на 0.")

        # Проверка поля "price"
        price = offer.find('price')
        price_value = price.text.strip() if price is not None else ''

        if not price_value or price_value.upper() == 'N/A':  # Проверка на пустоту и 'N/A'
            print(f"В предложении с id={offer.get('id')} поле <<Цена>> не заполнено или имеет значение 'N/A'.")
            all_fields_filled = False
            price.text = '0'  # Обнуляем, если поле пустое или 'N/A'
        else:
            try:
                float_price = float(price_value)
                if float_price < 0:
                    price.text = '0'  # Обнуляем, если оно отрицательное
                    print(f"Цена не может быть отрицательной. Значение обнулено в предложении с id={offer.get('id')}.")
            except ValueError:
                price.text = '0'  # Обнуляем при ошибке
                print(f"В предложении с id={offer.get('id')} поле <<Цена>> имеет недопустимое значение, заменено на 0.")

        # Обработка других параметров
        for param in params:
            param_name = param.get('name')
            param_value = param.text.strip() if param.text is not None else ''

            if param_name == "Новинка":
                continue  # Пропустить поле "Новинка"нение изменений в новый XML-файл после обработки
    new_xml_file_path = 'azz_updated.xml'  # Имя файла для сохранения
    tree.write(new_xml_file_path, encoding='utf-8', xml_declaration=True)
    print(f"Измененный файл сохранен как '{new_xml_file_path}'.")

    # Пример использования
    # tree = ET.parse('azz.xml')  # Загрузите ваш исходный XML файл
    # process_offers(tree)


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
        send_file(id)
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")


def send_file(id):
    file_path = 'example.txt'  # Путь к файлу, который вы хотите отправить
    with open(file_path, 'rb') as file:
        bot.send_document(id, file)
    bot.send_message(id, "Файл был отправлен!")





def save_xml_file(tree, xml_file_path):
    """Сохраняет XML-дерево в файл."""
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
    print(f"Updated XML file has been saved as '{xml_file_path}'.")


























def send_xml_file(chat_id, file_path):
    # Создаем экземпляр бота

    try:
        # Отправляем файл
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=chat_id, document=file)
        print(f"Файл '{file_path}' успешно отправлен в чат с ID: {chat_id}.")
    except Exception as e:
        print(f"Ошибка при отправке файла: {e}")











# не нужно
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

# def send_file(user_id):
#     # Создаем XML-дерево
#     tree = create_xml()
#
#     # Путь к исходному XML-файлу
#     xml_file_path = 'azz.xml'
#     tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
#     print("Updated XML file has been saved as 'azz_updated.xml'.")
#
#     # Создаем ZIP-архив
#     zip_file_path = 'azz.zip'
#     zip_file(xml_file_path, zip_file_path)
#
#     # Проверяем файл перед отправкой
#     if os.path.exists(zip_file_path) and os.path.getsize(zip_file_path) > 0:
#         try:
#             with open(zip_file_path, 'rb') as file:  # Открываем ZIP-архив в режиме чтения
#                 bot.send_document(user_id, file)  # Отправляем файл
#                 print("ZIP-файл успешно отправлен.")
#         except telebot.apihelper.ApiException as e:
#             bot.send_message(user_id, f"Ошибка API: {e}")
#         except ConnectionError:
#             bot.send_message(user_id, "Ошибка: Нет соединения. Попробуйте позже.")
#         except Exception as e:
#             bot.send_message(user_id, f"Произошла ошибка при отправке файла: {e}")
#     else:
#         bot.send_message(user_id, "Ошибка: ZIP-файл пуст или не существует.")






















@bot.message_handler(commands=['date'])
def date(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)



bot.polling(none_stop=True)