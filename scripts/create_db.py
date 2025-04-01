import sqlite3
import pandas as pd

# Подключаемся к базе
conn = sqlite3.connect("shelf_life.db")
cursor = conn.cursor()

# Создаём таблицу (если её нет)
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    name TEXT,
    expiration_date TEXT,
    price REAL
);
""")

# Загружаем данные из CSV
df = pd.read_csv("D:/Рабочий стол/shelf life tracking system/scripts/output_utf8.csv")

# Если в CSV нет колонки 'expiration_date', добавим фиктивную дату
if "expiration_date" not in df.columns:
    df["expiration_date"] = "2025-12-31"  # Заглушка, потом заменим

# Оставляем нужные столбцы
df = df[["CODEPST", "NAME", "expiration_date", "p277015928"]]
df.columns = ["code", "name", "expiration_date", "price"]

# Записываем в базу
df.to_sql("medicines", conn, if_exists="replace", index=False)

# Закрываем соединение
conn.commit()
conn.close()

print("✅ Данные загружены в SQLite!")
