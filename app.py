from flask import Flask, render_template, request
import sqlite3

conn = sqlite3.connect("DB_test.sqlite")
cursor = conn.cursor()

#запрос страны, с которой производится больше всего действий
most_country = cursor.execute(""" SELECT country, COUNT(country) AS cnt
                    FROM all_table
                    GROUP BY country
                    ORDER BY cnt DESC
                    """).fetchall()
#формирование списка категорий, с исключением путого поля из БД
category_list = cursor.execute(""" SELECT category
                    FROM all_table
                    WHERE category !=''
                    GROUP BY category
                    """).fetchall()
conn.close()
app = Flask(__name__)

#Запросы в sql не вынесены в отдельный файл, ввиду малости проекта.
@app.route('/', methods=['GET','POST'])
def index():
    conn = sqlite3.connect("DB_test.sqlite")
    cursor = conn.cursor()
    if request.method == 'GET':
        conn.close()
        return render_template('index.html', tmp=category_list)
    expression = request.form.get('expression')
    if request.form['btn'] == 'Узнать первое':
        result = 'Больше всего запросов поступило из страны: ' + str(most_country[0][0]) + ', с количеством запросов: ' + str(most_country[0][1])
        conn.close()
        return render_template('index.html', result1 = result, tmp=category_list)
    if request.form['btn'] == 'Узнать второе':
        category_name=request.form.get('list1')
        #Поиск по категориям, самой часто встречающейся страны
        find_country_category = cursor.execute("""  SELECT category, country, COUNT(country) AS cnt
                                                    FROM all_table
                                                    WHERE category LIKE ?
                                                    GROUP BY country
                                                    ORDER BY cnt DESC
                                                    """, (category_name,)).fetchall()
        out_str2 = 'Категорией ' + str(find_country_category[0][0]) + ' интересуются из страны: ' + str(
            find_country_category[0][1]) + ', с количеством запросов: ' + str(find_country_category[0][2])
        conn.close()
        return render_template('index.html', result2 = out_str2, tmp=category_list)
    if request.form['btn'] == 'Узнать третье':
        category_name=request.form.get('list2')
        #Поиск по категориям, день-ночь
        find_day_category = cursor.execute(""" SELECT category, "Times_of_day", COUNT("Times of day") AS cnt
                    FROM all_table
                    WHERE category LIKE ?
                    GROUP BY "Times_of_day"
                    ORDER BY cnt DESC
                """, (category_name,)).fetchall()
        out_str2 = 'Категорией ' + str(find_day_category[0][0]) + ' интересуются во время дня: ' + str(
            find_day_category[0][1]) + ', с количеством запросов: ' + str(find_day_category[0][2])
        conn.close()
        return render_template('index.html', result3 = out_str2, tmp=category_list)
if __name__ == '__main__':
    app.run()
