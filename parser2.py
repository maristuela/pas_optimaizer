import xml.etree.ElementTree as ET
import threading
import time



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
            params = offer.findall('param')
            param_check(idx, params)

        # if not all_fields_filled:
        #     pass

def id_check(offer_id, offer: ET.Element, id_set) -> bool:
    """
    Ищет дублирующиеся id и удаляет их
    """
    if offer_id in id_set:
        # Блок для удаления дублирующихся карточек
        try:
            root.find('.//offers').remove(offer)
            return False
        except ValueError as e:
            print(e)
    else:
        id_set.add(offer_id)
    return True

def tag_check(idx, offer):
    """
    Проверяет поля тегов
    """
    tags = dict()
    for child in offer:
        tag_name = child.tag
        tag_value = child.text.strip() if child.text is not None else ''
        tags[tag_name] = tag_value
        #category_id = int
        # Проверяем, заполнено ли поле
        if not tag_value:
            print(f"В предложении {idx} поле <<{tag_name}>> не заполнено.")
            all_fields_filled = False
        
        match tag_name:
            case 'price':
                try:
                    tag_value = float(tag_value)
                    #if tags['categoryId'] 
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

def param_check(idx, params):
    """
    Проверяет поля параметров
    """
    for param in params:
        param_name = param.get('name')
        param_value = param.text.strip() if param.text is not None else ''

    if not param_value:
        print(f"В предложении {idx} поле <<{param_name}>> не заполнено.")
        all_fields_filled = False
        #print(event.is_set())
        #event.wait()

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





def bot():
    """
    Тестовая функция
    """
    for i in range(10):
        print(i)
        time.sleep(5)
        #event.set()

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

print()
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
tree.write('output_feed.xml')