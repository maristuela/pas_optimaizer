import xml.etree.ElementTree as ET
from services.technical_service import *

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

def file_to_tree(path: str) -> ET.ElementTree:
    """Парсит xml-файл
    
    :param path: Путь к файлу
    :return: :class:`Дерево элементов <ElementTree>`
    :rtype: ElementTree
    """
    tree = None
    tree = ET.parse(path)
    return tree

def check_offers(root: ET.Element):
    """Проверяет атрибуты и параметры offers
    """
    id_set = set()
    
    offers = root.findall('.//offer')
    for offer in offers:
        idx = offer.attrib['id']
        try:
            idx = int(idx)
        except ValueError:
            print("Поле <<id>> имеет недопустимое значение.")
        for field in REQUIRED_FIELDS:
            element = offer.find(field)
            field_value = element.text.strip() if element is not None and element.text is not None else None
        if id_check(root, offer, idx, id_set):
            element_check(offer, idx)

def parser():
    try:
        tree = file_to_tree(file_path)
    except ET.ParseError:
        print("Невозможно прочитать файл. "\
            "Убедитесь, что файл имеет расширение xml и все теги определяются правильно.")
    except FileNotFoundError:
        print("Файл не найден по данному адресу")
    else:
        root = tree.getroot()
        check_offers(root)
        tree.write('output_feed.xml', encoding='utf-8', xml_declaration=True)