import xml.etree.ElementTree as ET


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


# Пример использования
xml_file_path = 'sale.xml'  # Замените на путь к вашему XML-файлу
tree = ET.parse(xml_file_path)
process_offers(tree)
