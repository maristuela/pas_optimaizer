import xml.etree.ElementTree as ET
from services.technical_service import *
from services.spelling_service import *

FILE_PATH = 'yandex_feed.xml'
TECH_CORRECT_FILE_PATH = 'tech_correct_feed.xml'

def file_to_tree(path: str) -> ET.ElementTree:
    """Парсит xml-файл
    
    :param path: Путь к файлу
    :return: :class:`Дерево элементов <ElementTree>`
    :rtype: ElementTree
    """
    tree = None
    tree = ET.parse(path)
    return tree

def parser(file_path) -> ET.ElementTree:
    try:
        tree = file_to_tree(file_path)
    except ET.ParseError:
        print("Невозможно прочитать файл. "\
            "Убедитесь, что файл имеет расширение xml и все теги определяются правильно.")
    except FileNotFoundError:
        print("Файл не найден по данному адресу")
    return tree

def service_startup():
    tree = parser(FILE_PATH)
    root = tree.getroot()
    check_offers(root)
    tree.write(TECH_CORRECT_FILE_PATH, encoding='utf-8', xml_declaration=True)
    tree = parser(TECH_CORRECT_FILE_PATH)
    root = tree.getroot()
    descriptions_enumeration(root)
    tree.write('output_feed.xml', encoding='utf-8', xml_declaration=True)