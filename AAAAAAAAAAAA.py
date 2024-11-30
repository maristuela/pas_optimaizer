import xml.etree.ElementTree as ET

# Пример списка требуемых полей

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

# Функция для проверки наличия и обновления ключевых полей в каждом offer
def check_offer_fields(offers, user_id, tree):
    for idx, offer in enumerate(offers, start=1):
        for field in required_fields:
            # Поиск элемента по полю
            element = offer.find(field)

            # Проверяем, существует ли элемент
            if element is None:
                print(f"Error: Offer ID '{offer.attrib.get('id')}' is missing '{field}'.")
                # Запрашиваем у пользователя ввод значения для отсутствующего поля
                user_input = input(f"Please enter value for '{field}': ")
                # Создаем новый элемент и добавляем его в offer
                new_element = ET.Element(field)
                new_element.text = user_input
                offer.append(new_element)  # Добавление нового элемента в offer
                print(f"Added new element '{field}' with value: '{user_input}'")

            else:
                # Проверяем заполнено ли поле
                if element.text is None or element.text.strip() == '':
                    print(f"Warning: Offer ID '{offer.attrib.get('id')}' is missing '{field}' or it is empty.")
                    # Запрашиваем у пользователя ввод значения для пустого поля
                    user_input = input(f"Please enter value for '{field}': ")
                    element.text = user_input  # Обновление текста существующего элемента
                    print(f"Updated element '{field}' with value: '{user_input}'")

    # Проверка, что изменения записаны
    new_xml_file_path = 'updated.xml'
    try:
        tree.write(new_xml_file_path, encoding='utf-8', xml_declaration=True)
        print(f"Измененный файл сохранен как '{new_xml_file_path}'.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

if __name__ == "__main__":
    # Загружаем XML и извлекаем offers
    try:
        tree = ET.parse('azz.xml')  # Замените на ваше имя файла
        root = tree.getroot()
        offers = root.findall('.//offer')  # Обратите внимание на путь
        user_id = 'example_user_id'  # Замените на актуальный идентификатор пользователя

        check_offer_fields(offers, user_id, tree)

    except ET.ParseError as e:
        print(f"Ошибка при парсинге XML: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
