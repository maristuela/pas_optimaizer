import os
import telebot
import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
from services.technical_service import check_offers


bot = telebot.TeleBot('7216725010:AAGgec15kB4cjSmIe3hlHouOiaYRqXe5EB4')

base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton(text='Загрузить фид в формате XML', callback_data="new"))
key = " "

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
    
bot.polling(none_stop=True)
