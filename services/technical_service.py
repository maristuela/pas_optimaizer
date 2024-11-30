import xml.etree.ElementTree as ET
from services.spelling_service import *

FILE_PATH = 'yandex_feed.xml'
DUPLICATE_OFFER_DELETE_MESSAGE = "Был удален фид с дублирующимся id: {:d}."
DUPLICATE_ELEMENT_DELETE_MESSAGE = "В предложении {:d} удалено дублирующееся поле <<{}>>."
DUPLICATE_PARAMETER_DELETE_MESSAGE = "В предложении {:d} удалено дублирующееся поле <<{}>>."
NOT_FILLED_FIELD_MESSAGE = "В предложении {:d} поле <<{}>> не заполнено."
INVALID_ELEMENT_VALUE_MESSAGE = "В предложении {:d} поле <<{}>> имеет недопустимое значение."
INVALID_PARAMETER_VALUE_MESSAGE = "В предложении {:d} поле <<{}>> имеет недопустимое значение."
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

def pricing(offer: ET.ElementTree, elements_dict: dict, oldprice: float, param_value: float):
    price = oldprice * (100-param_value) / 100
    offer.find('price').text = str(price)
    currency_id = elements_dict['currencyId']
    offer.find('currencyId').text = currency_id

def element_check(offer: ET.Element, idx: int):
    """Проверяет поля тегов
    """
    elements_dict = dict()
    fields_list = list()
    all_fields = False
    params = list()
    for element in offer:
        element_name = element.tag
        element_value = element.text.strip() if element.text is not None else ''

        if element_name == 'param':
            params += [element]
            continue

        if element_name in elements_dict.keys():
            offer.remove(element)
            print(DUPLICATE_ELEMENT_DELETE_MESSAGE.format(idx, element_name))
            continue
        else:
            elements_dict[element_name] = element_value
        
        fields_list.append(element_name)
        
        if len(REQUIRED_FIELDS) == len(fields_list):
            all_fields = True
            

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
                    # description_string = spelling_check(element_value)
                    # if description_string != '0':
                    #     element.text = description_string
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "description"))
            case 'barcode':
                try:
                    element_value = int(element_value)
                except ValueError:
                    print(INVALID_ELEMENT_VALUE_MESSAGE.format(idx, "barcode"))    
    param_check(offer, elements_dict, params, idx)

def param_check(offer: ET.Element, elements_dict: dict, params: ET.Element, idx: int):
    """Проверяет поля параметров
    """
    params_dict = dict()
    for param in params:
        param_name = param.get('name')
        param_value = param.text.strip() if param.text is not None else ''

        if param_name in params_dict.keys():
            params.remove(param)
            print(DUPLICATE_PARAMETER_DELETE_MESSAGE.format(idx, param_name))
            continue
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
                        param_value = 0
                        param.text = '0.0'
                        raise Exception("Скидка не может иметь значение больше 100. Значение обнулено.")
                    if param_value < 0:
                        param_value = 0
                        param.text = '0.0'
                        raise Exception("Скидка не может иметь отрицательное значение. Значение обнулено.")
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Скидка"))
                except Exception as e:
                    print(e)

                oldprice = float(elements_dict['price'])
                if not 'oldprice' in elements_dict and param_value > 0:
                    element_price = ET.Element('oldprice')
                    element_price.text = str(oldprice)
                    offer.insert(1, element_price)
                    pricing(offer, elements_dict, oldprice, param_value)
                if param_value > 0:
                    pricing(offer, elements_dict, oldprice, param_value)
            case 'Новинка':
                try:
                    param_value = str(param_value)
                except ValueError:
                    print(INVALID_PARAMETER_VALUE_MESSAGE.format(idx, "Новинка"))

