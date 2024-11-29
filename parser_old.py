def parse():
    EXCEL_TABLE_PATH = 'azz.xml'
    # Список для хранения информации о товарах
    offers_list = []

    # Получение предложений
    try:
        root = ET.parse(EXCEL_TABLE_PATH)
        offers = root.find('.//offers')
        for offer in offers.findall('offer'):
            offer_params = list(offer.findall('param'))
            params = dict()
            for i in range(len(offer.findall('param'))):
                params[offer.findall('param')[i].attrib['name']] = offer.findall('param')[i].text
            offer_data = {
                'id': offer.get('id'),
                'available': offer.get('available'),
                'name': offer.find('name').text,
                'price': float(offer.find('price').text),
                'currencyId': offer.find('currencyId').text,
                'vendor': offer.find('vendor').text,
                'description': offer.find('description').text,
                'barcode': offer.find('barcode').text,
                **params
            }
            offers_list.append(offer_data)
        # Создание DataFrame
        df = pd.DataFrame(offers_list)

        # Вывод DataFrame
        print(df)


    except ET.ParseError:
        print("Невозможно прочитать файл")