# импортируем библиотеки, необходимые для парсинга
import re # модуль для записи регулярных выражений
import requests # пакет для отправки запроса на сайт
from bs4 import BeautifulSoup # пакет для парсинга сайта
import pandas as pd # пакет для работы с данными в DataFrame виде

# создаем пустой список. Будем наполнять его данными слой за слоем
rows = []
# т.к. сайт достаточно простой, то для обхода по каждой странице достаточно менять значение страницы по порядку,
# начиная с 1 и заканчивая 19. Решил сделать цикл for-in. Для простой задачи - простое решение
for i in range(1, 19):
    url = f'https://www.atomstroy.net/kvartiry?page={i}' # назначаем адрес сайта для url через f-строку. Значение i
    # меняется при каждом обходе по циклу
    # далее прописываем в переменную ответа функцию с url и User-Agent, для большей имитации реального запроса через
    # браузер человеком
    response = requests.get(url, headers={
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/127.0.0.0 Safari/537.36'})
    # при каждом новом цикле for-in, парсер скрейпит html-страницу и парсит ее через html.parser
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup.prettify()) - # это я смотрел красивый html-код в выводе IDE

    # создаю цикл for-in для записи в список rows спарсенных данных в формате словаря
    for row in soup.find_all('li', ('class', 'catalog-list__item catalog-list-item')):
        rows.append({
            'square': row.find('span', ('class', 'color color--red')).text[:-3],
            'price': row.find(string=re.compile("млн")).text[:-4],
            'floor': row.find('span', ('class', 'catalog-list-item__text')).text[:-5],
            'type': row.find(string=['Ст', '1к', '2к', '3к', '4+'])
        })

# создаю из списка rows DataFrame для более простого преобразования данных в табличном виде
df = pd.DataFrame(rows)
# и сохраняю все это в формате .csv с разделителем, дефолтным для Excel
df.to_csv(r'./apt_data-frame1.csv', sep=';', encoding='utf-8', index=False, header=True)
# print(len(rows), '\n', rows, '/n', df)