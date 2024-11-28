import requests
from urllib.parse import urlencode
from io import BytesIO

import telebot
import sqlite3
import os
import requests
from urllib.parse import urlencode
import requests
from urllib.parse import urlencode

import pandas as pd
import xml.etree.ElementTree as ET






bot = telebot.TeleBot('7216725010:AAGgec15kB4cjSmIe3hlHouOiaYRqXe5EB4')

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton(text='Загрущить фид в формате XML', callback_data="new"))
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
    # con = sqlite3.connect('SoftSkills.db')
    # cursorObj = con.cursor()
    # albums = (message.chat.id, 0, 0, 0, 0, 0, 0)
    # cursorObj.execute("INSERT INTO bot VALUES (?,?,?,?,?,?,?)", albums)
    # con.commit()
    print(message.chat.id)

    bot.send_message(message.chat.id, 'Привет, я твой персональный помошник в проферки твоих фидов.')
    menu(message.chat.id)
    # bot.send_message(message.chat.id, text="Чем я могу помочь?", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global key
    if (call.data == "new"):
        bot.send_message(call.message.chat.id, 'Введите ссылку на яндекс диск')
        key = "url"
    # elif (call.data == "memo"):
    #     bot.send_message(call.message.chat.id, "Укажите номер месяца за, на который необходимо сформировать документы",
    #                      reply_markup=test_quition)



@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Укажите путь к директории вашего проекта
        project_directory = 'D:/exel_python/'
        # Создаем полный путь к файлу
        file_path = os.path.join(project_directory, message.document.file_name)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, str(e))


#
# @bot.message_handler(content_types=['text'])
# def text(message):
#     print(message.text)
#     if key == "url":
#         try:
#             print("Проверяем ссылку")
#             public_key = message.text  # Сюда вписываете вашу ссылку
#             # Получаем загрузочную ссылку
#             final_url = base_url + urlencode(dict(public_key=public_key))
#             print("Ожидайте мы работаем с данными")
#             response = requests.get(final_url)
#             download_url = response.json()['href']
#
#             # Загружаем файл и сохраняем его
#
#
#             download_response = requests.get(download_url)
#             print(download_response.content)
#             download_response = requests.get(download_url)
#             with open('azz.xlsx', 'wb') as f:  # Здесь укажите нужный путь к файлу
#                 f.write(download_response.content)
#
#
#         except Exception:
#             print("Не верная ссылка")





@bot.message_handler(content_types=['text'])
def text(message):
    print(message.text)
    if key == "url":
        try:
            print("Проверяем ссылку")
            public_key = message.text  # Сюда вписываете вашу ссылку
            # Получаем загрузочную ссылку
            final_url = base_url + urlencode(dict(public_key=public_key))
            print("Ожидайте мы работаем с данными")
            response = requests.get(final_url)
            download_url = response.json()['href']

            # Загружаем файл и сохраняем его


            download_response = requests.get(download_url)
            print(download_response.content)
            with open('azz.xml', 'wb') as f:  # Здесь укажите нужный путь к файлу
                f.write(download_response.content)








            # Пример XML данных

            # Парсинг XML данных
            root = ET.fromstring(download_response.content)

            # Определяем обязательные поля
            required_fields = ['id', 'name', 'price']

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



            # parse()

            # Загружаем XML
            tree = ET.parse('azz.xml')  # Убедитесь, что файл с данными называется 'azz.xml'
            root = tree.getroot()

            # Находим все элементы offer
            offers = root.findall('.//offer')

            # Проверяем поля

            # Проверяем поля
            check_offer_fields(offers, message.chat.id, tree)

            # check_offer_fieldstt(offers, message.chat.id, tree)




        except Exception:
            print("Не верная ссылка")




def menu(id):
    bot.send_message(id, text="Чем я могу помочь?", reply_markup=markup)



def parse():
    EXCEL_TABLE_PATH = 'azz.xml'
    # dataFlow = pd.read_excel(EXCEL_TABLE_PATH)

    # dataFlow = pd.read_xml(EXCEL_TABLE_PATH)
    # Парсинг XML
    """
    tree = etree.parse(EXCEL_TABLE_PATH)
    root = tree.getroot()
    for offer in root['offers']:
        print(offer['price'])
    """

    # Список для хранения информации о товарах
    offers_list = []

    # Получение предложений
    try:
        root = ET.parse(EXCEL_TABLE_PATH)
        offers = root.find('.//offers')
        for offer in offers.findall('offer'):
            offer_params = list(offer.findall('param'))
            params = dict()
            for i in range(len(offer.findall('param'))):
                params[offer.findall('param')[i].attrib['name']] = offer.findall('param')[i].text
            offer_data = {
                'id': offer.get('id'),
                'available': offer.get('available'),
                'name': offer.find('name').text,
                'price': float(offer.find('price').text),
                'currencyId': offer.find('currencyId').text,
                'vendor': offer.find('vendor').text,
                'description': offer.find('description').text,
                'barcode': offer.find('barcode').text,
                **params
            }
            offers_list.append(offer_data)
        # Создание DataFrame
        df = pd.DataFrame(offers_list)

        # Вывод DataFrame
        print(df)


    except ET.ParseError:
        print("Невозможно прочитать файл")



# Функция для проверки наличия ключевых полей в каждом offer
def check_offer_fields(offers, id, tree):
    for idx, offer in enumerate(offers, start=1):
        for field in required_fields:
            element = offer.find(field)
            field_value = element.text.strip() if element is not None and element.text is not None else None
            # Проверяем, существует ли элемент
            if element is None:
                print(f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")
                bot.send_message(id,f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")

                # Запрашиваем у пользователя ввод значения для отсутствующего поля
                user_input = input(f"Please enter value for '{field}': ")
                # Создаем новый элемент и добавляем его в offer
                new_element = ET.Element(field)
                new_element.text = user_input
                offer.append(new_element)
                tree.write('azz_updated.xml', encoding='utf-8', xml_declaration=True)
                print("Updated XML file has been saved as 'azz_updated.xml'.")



            # Проверяем, заполнено ли поле
            else:
                if field_value is None or field_value == '':
                    print(f"Warning: Offer ID '{offer.attrib.get('id')}' is missing '{field}' or it is empty.")
                    bot.send_message(id, f"Warning: Offer ID '{offer.attrib.get('id')}' is missing '{field}' or it is empty.")
                    # Запрашиваем у пользователя ввод значения для пустого поля
                    user_input = input(f"Please enter value for '{field}': ")
                    element.text = user_input
                    tree.write('azz_updated.xml', encoding='utf-8', xml_declaration=True)
                    print("Updated XML file has been saved as 'azz_updated.xml'.")

            # Сохраняем изменения в XML файл
        # bot.send_document(id, 'azz_updated.xml', encoding='utf-8', xml_declaration=True)





# Функция для проверки заполненности всех внутренних тегов offer
def check_offer_fieldstt(offers, id, tree):
    for idx, offer in enumerate(offers, start=1):
        try:
            int(idx)
        except ValueError:
            print("Поле <<id>> имеет недопустимое значение")
        all_fields_filled = True

        # Перебираем все дочерние элементы текущего offer
        for child in offer:
            tag_name = child.tag
            tag_value = child.text.strip() if child.text is not None else ''

            # Проверяем, заполнено ли поле
            if not tag_value:
                print(f"В предложении {idx} поле <<{tag_name}>> не заполнено.")
                all_fields_filled = False

            match tag_name:
                case 'price':
                    try:
                        tag_value = float(tag_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<цена>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<цена>> имеет недопустимое значение")
                case 'categoryId':
                    try:
                        tag_value = int(tag_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<id категории>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<id категории>> имеет недопустимое значение")
                case 'barcode':
                    try:
                        tag_value = int(tag_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<штрихкод>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<штрихкод>> имеет недопустимое значение")

        # Проверяем теги 'param'
        params = offer.findall('param')
        for param in params:
            param_name = param.get('name')
            param_value = param.text.strip() if param.text is not None else ''

            if not param_value:
                print(f"В предложении {idx} поле <<{param_name}>> не заполнено")
                all_fields_filled = False

            match param_name:
                case 'Артикул':
                    try:
                        param_value = int(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Артикул>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<Артикул>> имеет недопустимое значение")
                case 'Рейтинг':
                    try:
                        param_value = float(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Рейтинг>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<Рейтинг>> имеет недопустимое значение")
                case 'Количество отзывов':
                    try:
                        param_value = int(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Количество отзывов>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<Количество отзывов>> имеет недопустимое значение")
                case 'Скидка':
                    try:
                        param_value = float(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Скидка>> имеет недопустимое значение")
                        bot.send_message(id, f"В предложении {idx} поле <<Скидка>> имеет недопустимое значение")

        if not all_fields_filled:
            pass



bot.polling(none_stop=True)