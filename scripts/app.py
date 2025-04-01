import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Функция загрузки данных
def load_data():
    conn = sqlite3.connect("shelf_life.db")
    df = pd.read_sql("SELECT * FROM medicines", conn)
    conn.close()
    return df

# Интерфейс
st.title("💊 Отслеживание сроков годности лекарств")

df = load_data()
df["expiration_date"] = pd.to_datetime(df["expiration_date"])  # Преобразуем в datetime

# Фильтр по сроку годности
expiration_filter = st.date_input("Показать лекарства, срок годности до:", pd.to_datetime("2025-12-31"))
filtered_df = df[df["expiration_date"] <= pd.to_datetime(expiration_filter)]

# Поиск по названию
search_term = st.text_input("🔎 Поиск лекарства:")
if search_term:
    filtered_df = filtered_df[filtered_df["name"].str.contains(search_term, case=False, na=False)]

# Таблица
st.dataframe(filtered_df)


# 📊 Гистограмма по месяцам
st.subheader("📊 Количество лекарств по месяцам")
df["month"] = df["expiration_date"].dt.strftime("%Y-%m")  # Преобразуем в строку
month_count = df.groupby("month").size().reset_index(name="count")
fig1 = px.bar(month_count, x="month", y="count", title="Распределение лекарств по месяцам", color="count",
              labels={"month": "Месяц", "count": "Количество"})
fig1.update_layout(xaxis=dict(tickangle=-45))  # Поворот подписей оси X
st.plotly_chart(fig1)

# 📈 Линейный график срока годности
st.subheader("📈 Динамика истечения срока годности")
df["expiration_date_only"] = df["expiration_date"].dt.date  # Только дата без времени
df["expiration_date_only"] = df["expiration_date"].dt.floor("D")
df["expiration_month"] = df["expiration_date"].dt.strftime("%Y-%m")
time_series = df.groupby("expiration_month").size().reset_index(name="count")
time_series = df.groupby("expiration_date_only").size().reset_index(name="count")
fig3 = px.line(time_series, x="expiration_date_only", y="count",
               title="Динамика истечения срока годности",
               labels={"expiration_date_only": "Дата", "count": "Количество"},
               line_shape="spline")  # Делаем линии плавными

fig3 = px.line(time_series, x="expiration_date_only", y="count", title="Динамика истечения срока годности",
               labels={"expiration_date_only": "Дата", "count": "Количество"})
fig3.update_traces(mode="lines+markers")  # Добавляем точки к линии
st.plotly_chart(fig3)
