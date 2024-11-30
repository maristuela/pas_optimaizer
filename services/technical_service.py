import xml.etree.ElementTree as ET
from services.spelling_service import *

DUPLICATE_OFFER_DELETE_MESSAGE = "Был удален фид с дублирующимся id: {:d}."
DUPLICATE_ELEMENT_DELETE_MESSAGE = "В предложении {:d} удалено дублирующееся поле <<{}>>."
DUPLICATE_PARAMETER_DELETE_MESSAGE = "В предложении {:d} удалено дублирующееся поле <<{}>>."
NOT_FILLED_FIELD_MESSAGE = "В предложении {:d} поле <<{}>> не заполнено."
INVALID_ELEMENT_VALUE_MESSAGE = "В предложении {:d} поле <<{}>> имеет недопустимое значение."
INVALID_PARAMETER_VALUE_MESSAGE = "В предложении {:d} поле <<{}>> имеет недопустимое значение."

file_path = 'yandex_feed.xml'

def id_check(root: ET.Element, offer: ET.Element, offer_id: int, id_set: set) -> bool:
    """Ищет дублирующиеся id и удаляет их
    """
    if offer_id in id_set:
        root.find('.//offers').remove(offer)
        print(DUPLICATE_OFFER_DELETE_MESSAGE.format(offer_id))
        return False
    else:
        id_set.add(offer_id)
    return True

def element_check(offer: ET.Element, idx: int):
    """Проверяет поля тегов
    """
    elements_dict = dict()
    params = list()
    for element in offer:
        element_name = element.tag
        element_value = element.text.strip() if element.text is not None else ''
        
        if element_name == 'param':
            params += element
            continue

        if element_name in elements_dict.keys():
            offer.remove(element)
            print(DUPLICATE_ELEMENT_DELETE_MESSAGE.format(idx, element_name))
            continue
        else:
            elements_dict[element_name] = element_value
        
        if not element_value:
            print(NOT_FILLED_FIELD_MESSAGE.format(idx, element_name))
        
        match element_name:
            case 'price':
                try:
                    element_value = float(element_value)
                    # Код для корректировки цены по категории
                    # if elements['categoryId']
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "price"))
            case 'oldprice':
                try:
                    element_value = float(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "oldprice"))
            case 'currencyId':
                try:
                    element_value = str(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "currencyId"))
            case 'categoryId':
                try:
                    element_value = int(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "categoryId"))
            case 'picture':
                try:
                    element_value = str(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "picture"))
            case 'name':
                try:
                    element_value = str(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "name"))
            case 'vendor':
                try:
                    element_value = str(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "vendor"))
            case 'description':
                try:
                    element_value = str(element_value)
                    description_string = spelling_check(element_value)
                    if description_string != '0':
                        element.text = description_string
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "description"))
            case 'barcode':
                try:
                    element_value = int(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "barcode"))    
    param_check(params, idx)

def param_check(params: ET.Element, idx: int):
    """Проверяет поля параметров
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
                        param.text = '0.0'
                        raise Exception("Скидка не может иметь значение больше 100. Значение обнулено.")
                    if param_value < 0:
                        param.text = '0.0'
                        raise Exception("Скидка не может иметь отрицательное значение. Значение обнулено.")
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Скидка"))
                except Exception as e:
                    print(e)
                else:
                    # Добавить поле oldprice
                    pass
            case 'Новинка':
                try:
                    param_value = str(param_value)
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Новинка"))
