import pandas as pd
import geoip2.database
import sqlite3

# Создаём БД
conn = sqlite3.connect("DB_test.sqlite")
cur = conn.cursor()

# создаем датафрейм с разделителем "один и более пробелов"
df = pd.read_csv('logs.txt', sep='\s+',
                 names=['shop_api', '|', 'Date', 'Time', 'ID', 'INFO:', 'IP', 'URL'])
# убираем лишние столбцы, которые не пригодятся в дальнейшем
df = df.drop(['shop_api', '|', 'ID', 'INFO:'], axis=1)
# подсоединяем базу данных стран для определения страны, которой принадлежит IP-адрес
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')


# Функция определения страны по IP
def country_name(ip):
    try:
        return reader.country(ip).country.name
    except:
        return 'Unknown country'


# Функция определения времени суток - день (09:00-21:00) или ночь (21:00-09:00).
# При необходимости можно задать более точное определение времени суток (утро, обед и т.д.)
def day_or_night(time, type=str):
    s = time.split(':')
    if (s[0] > '09') and (s[0] < '21'):
        return 'Day'
    else:
        return 'Night'


# Функция определения категории товара из URL
def set_category(link, type=str):
    if (link.find('success_pay') > 0) or (link.find('?') > 0) or (link == ' ') or (
            link == 'https://all_to_the_bottom.com/'):
        return ''
    else:
        return link.split('/')[3]


# Функция определения User_ID из URL
def user_id(link, type=str):
    if link.find('user_id') > 0:
        s = link.split('user_id=')
        return s[1].split('&')[0]
    else:
        return '0'


# Функция определения Cart_ID из URL
def cart_id(link, type=str):
    if link.find('cart_id') > 0:
        s = link.split('cart_id=')
        return s[1]
    else:
        return '0'


# Формируем столбцы датафрейма для последующего переноса его в БД
df['Country'] = df.apply(lambda x: country_name(x['IP']), axis=1)
df['Category'] = df.apply(lambda x: set_category(x['URL']), axis=1)
df['Times_of_day'] = df.apply(lambda x: day_or_night(x['Time']), axis=1)
df['Succes_pay'] = df.apply(lambda x: x['URL'].find('success_pay') > 0, axis=1)
df['Cart_ID'] = df.apply(lambda x: cart_id(x['URL']), axis=1)
df['User_ID'] = df.apply(lambda x: user_id(x['URL']), axis=1)

# Переносим датафрейм в созданную БД
df.to_sql('all_table', conn, if_exists='replace')
cur.close()
conn.close()