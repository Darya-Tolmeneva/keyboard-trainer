import sqlite3

# Подключение к БД
con = sqlite3.connect("data/profils_db.sqlite")

# Создание курсора
cur = con.cursor()
n = 1
# Выполнение запроса и получение всех результатов
result = cur.execute("""SELECT * FROM profils
            WHERE id = n""").fetchall()

# Вывод результатов на экран
for elem in result:
    print(elem)

con.close()