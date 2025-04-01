import sqlite3
from dbfread import DBF

# Подключаем базу данных
conn = sqlite3.connect("medicines_life.db")
cursor = conn.cursor()

# Создаём таблицу, если её нет
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        batch TEXT,
        expiration_date TEXT
    )
""")

# Указываем путь к файлу
dbf_file_path = r"D:\Рабочий стол\shelf life tracking system\scripts\medicines.dbf"

# Загружаем данные из DBF
dbf = DBF(dbf_file_path, encoding='cp1251', char_decode_errors='ignore')

for record in dbf:
    cursor.execute("INSERT INTO products (name, batch, expiration_date) VALUES (?, ?, ?)",
                   (record["NAME"], record["BATCH"], record["EXP_DATE"]))

conn.commit()
conn.close()
print("✅ Данные успешно загружены в базу!")
