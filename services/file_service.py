import zipfile
import yadisk

from bot import *

REQUIRED_FIELDS = [
    'price',
    'currencyId',
    'categoryId',
    'picture',
    'name',
    'vendor',
    'description',
    'barcode'
]

y = yadisk.YaDisk(token="y0_AgAAAABogsCFAAzdlQAAAAEaXuWrAADPRipOtMJIdarwjBAm_jMjcf2SYA")
keybred = 1

def check_offer_fields(offers, user_id, tree):
    global keybred
    # Сначала обрабатываем все предложения
    xml_file_path = 'azz_updated.xml'
    for idx, offer in enumerate(offers, start=1):
        for field in REQUIRED_FIELDS:
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