import xml.etree.ElementTree as ET

# Функция для проверки заполненности всех внутренних тегов offer
def check_offer_fields(offers):
    for idx, offer in enumerate(offers, start=1):
        try:
            int(idx)
        except ValueError:
            print("Поле <<id>> имеет недопустимое значение.")
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
                        print(f"В предложении {idx} поле <<цена>> имеет недопустимое значение.")
                case 'categoryId':
                    try:
                        tag_value = int(tag_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<id категории>> имеет недопустимое значение.")
                case 'barcode':
                    try:
                        tag_value = int(tag_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<штрихкод>> имеет недопустимое значение.")


        # Проверяем теги 'param'
        params = offer.findall('param')
        for param in params:
            param_name = param.get('name')
            param_value = param.text.strip() if param.text is not None else ''

            if not param_value:
                print(f"В предложении {idx} поле <<{param_name}>> не заполнено.")
                all_fields_filled = False
            
            match param_name:
                case 'Артикул':
                    try:
                        param_value = int(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Артикул>> имеет недопустимое значение.")
                case 'Рейтинг':
                    try:
                        param_value = float(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Рейтинг>> имеет недопустимое значение.")
                case 'Количество отзывов':
                    try:
                        param_value = int(param_value)
                    except ValueError:
                        print(f"В предложении {idx} поле <<Количество отзывов>> имеет недопустимое значение.")
                case 'Скидка':
                    try:
                        param_value = float(param_value)
                        if param_value > 100:
                            param_value = 0
                            raise Exception("Скидка не может иметь значение больше 100. Значение обнулено.")
                    except ValueError:
                        print(f"В предложении {idx} поле <<Скидка>> имеет недопустимое значение.")
                    except Exception as e:
                        print(e)
                        
        if not all_fields_filled:
            pass

tree = None
while tree == None:
    path = str(input("Введите путь к файлу: "))
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        print("Невозможно прочитать файл. Убедитесь, что файл имеет расширение xml и все теги определяются правильно.")
    except FileNotFoundError:
        print("Файл не найден по данному адресу")

root = tree.getroot()

# Находим все элементы offer
offers = root.findall('.//offer')

# Проверяем поля
check_offer_fields(offers)