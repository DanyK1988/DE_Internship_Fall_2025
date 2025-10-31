from pymongo import MongoClient
from datetime import datetime, timedelta
from pprint import pprint
import json

# Подключение к MongoDB, остается без изменений
client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]
collection = db["user_events"]

# Устанавливаем дату в ручную для задания, но для реального скрипта нужно использовать datetime.today()
today = datetime(2024, 2, 4, 12, 0, 0)

# Создаем запрос, для меня основная сложность была провалиться в registration_date, но оказалось можно через точку
# Дальше язык очень похож на bash-скрипт, $ - указывает на оператор, lt - less that, меньше чем
# Мне показалось удобно что не надо указывать логические операторы, просто через запятую
query = {
    "user_info.registration_date": {"$lt": today - timedelta(days=30)},
    "event_time": {"$lt": today - timedelta(days=14)},
}

# Используем метод find, где первый аргумент - это запрос, второй, какие поля мы хотим получить _id всегда идет по умолчанию, поэтому его отключаем
# По заданию нам кроче user_id ничего не надо, поэтому легче идти через включающие проекции
# и включаем только user_id. Тк на выходе мы получаем курсор(итератор), то переводим его в список
results = list(collection.find(query, {"_id": 0, "user_id": 1}))

# Формируем итоговую коллекцию
archived_clients = {
    "date": today,
    "archived_users_count": len(results),
    "archived_users_ids": [result["user_id"] for result in results],
}

# Сохраняем в json файл. Тк мы используем кастомную дату, то в сохранение идут ненужные по заданию часы, минуты и секунды
# конкретно в этом заданиии избавимся от этого в ручную, на реальном скрипте с datetime.today() такой проблемы не будет
today_str = today.strftime("%Y-%m-%d")
with open(f"{today_str}.json", "w") as f:
    json.dump(archived_clients, f, default=str, indent=4)

# Файл сохраняется локально, я посмотрел как напряму записать файл в контейнер, выглядит запутанно и наверно выходит за рамки задания
# Можно в терминали прописать команду из урока для копирования в контейнер
# docker cp 2024-02-04.json mongo_db:/data/2024-02-04.json
# Можно улучшить и создать bash-скрипт, который будет получать текушую дату, искать файл и отправлять в контейнер
# Я пока в bash не силен, поэтому туда не идут, плюс по заданию это не надо, но так можно автоматизировать процесс

# Возможно я неправильно понял задание. Если нам нужно напряму загружать данные в таблицу в Mongo db, то нужно добавить

new_collection = db['archived_clients']

if archived_clients:
    new_collection.insert_many(archived_clients)
    print('Клиенты внесены в базу archived_clients')

# При первом переносе клиентов, таблица будет создана, в дальнейшем будет дописываться




