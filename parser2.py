import xml.etree.ElementTree as ET
import threading
import time

DUPLICATE_OFFER_DELETE_MESSAGE = "Был удален фид с дублирующимся id: {:d}."
DUPLICATE_ELEMENT_DELETE_MESSAGE = "В предложении {:d} удалено дублирующееся поле <<{}>>."
DUPLICATE_PARAMETER_DELETE_MESSAGE = "В предложении {:d} удалено дублирующееся поле <<{}>>."
NOT_FILLED_FIELD_MESSAGE = "В предложении {:d} поле <<{}>> не заполнено."
INVALID_ELEMENT_VALUE_MESSAGE = "В предложении {:d} поле <<{}>> имеет недопустимое значение."
INVALID_PARAMETER_VALUE_MESSAGE = "В предложении {:d} поле <<{}>> имеет недопустимое значение."

def check_offer_fields(offers: ET.Element):
    """
    Проверяет атрибуты и параметры offers
    """
    for offer in offers:
        idx = offer.attrib['id']
        try:
            idx = int(idx)
        except ValueError:
            print("Поле <<id>> имеет недопустимое значение.")
        # all_fields_filled = True
        if id_check(idx, offer, id_set):
            tag_check(idx, offer)
            

        # if not all_fields_filled:
        #     pass

def id_check(offer_id: int, offer: ET.Element, id_set: set) -> bool:
    """
    Ищет дублирующиеся id и удаляет их
    """
    if offer_id in id_set:
        try:
            root.find('.//offers').remove(offer)
            print(DUPLICATE_OFFER_DELETE_MESSAGE.format(offer_id))
            return False
        except ValueError as e:
            print(e)
    else:
        id_set.add(offer_id)
    return True

def tag_check(idx: int, offer: ET.Element):
    """
    Проверяет поля тегов
    """
    tags_dict = dict()
    params = list()
    for element in offer:
        tag_name = element.tag
        tag_value = element.text.strip() if element.text is not None else ''
        
        if tag_name == 'param':
            params += element
            continue

        if tag_name in tags_dict.keys():
            offer.remove(element)
            print(DUPLICATE_ELEMENT_DELETE_MESSAGE.format(idx, tag_name))
            continue
        else:
            tags_dict[tag_name] = tag_value
        
        # Проверяем, заполнено ли поле
        if not tag_value:
            print(NOT_FILLED_FIELD_MESSAGE.format(idx, tag_name))
            all_fields_filled = False
        
        match tag_name:
            case 'price':
                try:
                    tag_value = float(tag_value)
                    # Код для корректировки цены по категории
                    # if tags['categoryId']
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "price"))
            case 'oldprice':
                try:
                    tag_value = float(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "oldprice"))
            case 'currencyId':
                try:
                    tag_value = str(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "currencyId"))
            case 'categoryId':
                try:
                    tag_value = int(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "categoryId"))
            case 'picture':
                try:
                    tag_value = str(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "picture"))
            case 'name':
                try:
                    tag_value = str(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "name"))
            case 'vendor':
                try:
                    tag_value = str(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "vendor"))
            case 'description':
                try:
                    tag_value = str(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "description"))
            case 'barcode':
                try:
                    tag_value = int(tag_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "barcode"))    
    param_check(idx, params)

def param_check(idx: int, params: ET.Element):
    """
    Проверяет поля параметров
    """
    params_dict = dict()
    for param in params:
        param_name = param.get('name')
        param_value = param.text.strip() if param.text is not None else ''
        params_dict[param_name] = param_value

        if param_name in params_dict.keys():
            params.remove(param)
            print(DUPLICATE_PARAMETER_DELETE_MESSAGE.format(idx, param_name))
            continue
        else:
            params_dict[param_name] = param_value

        if not param_value:
            print(NOT_FILLED_FIELD_MESSAGE.format(idx, param_name))
            all_fields_filled = False
            #print(event.is_set())
            #event.wait()

        match param_name:
            case 'Артикул':
                try:
                    param_value = str(param_value)
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Артикул"))
            case 'Рейтинг':
                try:
                    param_value = float(param_value)
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Рейтинг"))
            case 'Количество отзывов':
                try:
                    param_value = int(param_value)
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Количество отзывов"))
            case 'Скидка':
                try:
                    param_value = float(param_value)
                    if param_value > 100:
                        #param.tail =''
                        param.text = '0.0'
                        raise Exception("Скидка не может иметь значение больше 100. Значение обнулено.")
                    if param_value < 0:
                        param.text = '0.0'
                        raise Exception("Скидка не может иметь отрицательное значение. Значение обнулено.")
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Скидка"))
                except Exception as e:
                    print(e)
            case 'Новинка':
                try:
                    param_value = str(param_value)
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Новинка"))

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
id_set = set()
offers = root.findall('.//offer')
#root.remove(ET.Element(offers[0]))
# Проверяем поля

# event = threading.Event()
# check_thread = threading.Thread(target=check_offer_fields, args=[offers])
# bot_thread = threading.Thread(target=bot)
# check_thread.start()
# bot_thread.start()
# bot_thread.join()
# check_thread.join()
check_offer_fields(offers)
tree.write('output_feed.xml', encoding='utf-8', xml_declaration=True)