import os
import telebot
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from checking_service import check_offer_fields


bot = telebot.TeleBot('7216725010:AAGgec15kB4cjSmIe3hlHouOiaYRqXe5EB4')

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton(text='Загрузить фид в формате XML', callback_data="new"))
key = " "

@bot.message_handler(commands=['start'])
def start(message):
    # con = sqlite3.connect('SoftSkills.db')
    # cursorObj = con.cursor()
    # albums = (message.chat.id, 0, 0, 0, 0, 0, 0)
    # cursorObj.execute("INSERT INTO bot VALUES (?,?,?,?,?,?,?)", albums)
    # con.commit()
    print(message.chat.id)

    bot.send_message(message.chat.id, 'Привет, я твой персональный помощник в проверке твоих фидов.')
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
                                f"Ошибка в элементе <product>: отсутствует или пусто обязательное поле '{field}'.")

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
            print("Не верная ссылка.")


def menu(id):
    bot.send_message(id, text="Чем я могу помочь?", reply_markup=markup)