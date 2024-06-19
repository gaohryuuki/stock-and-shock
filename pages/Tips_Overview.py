import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

from datetime import datetime

from io import BytesIO

st.title('Приложение для визуализации данных о чаевых')

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

uploaded_file = st.sidebar.file_uploader("Выберите файл данных о чаевых", type='csv')

if uploaded_file is not None:
    # Загружаем файл
    tips = load_data(uploaded_file)
    # Какие у нас данные?
    dtypes_df =pd.DataFrame(tips.dtypes, columns=['Тип данных']).reset_index()
    st.write('Формат принятых данных:')
    st.dataframe(dtypes_df)

    # Выбирает даты для гененрации дня заказа
    beginning_date = datetime.strptime('2014-1-01', '%Y-%m-%d')
    ending_date = datetime.strptime('2023-12-31', '%Y-%m-%d')

    d = st.sidebar.date_input(
        "Выберите даты для случайной генерации",
        (beginning_date, ending_date),
        beginning_date,
        ending_date,
        format="MM-DD-YYYY",
    )

    # Добавляем эти даты в таблицу
    tips['time_order'] = pd.Series(np.random.choice(pd.date_range(start=d[0], end=d[1]), len(tips)), dtype='datetime64[ns]')

    st.write('Загруженные данные:')
    st.dataframe(tips)
    
    # График динамики чаевых
    st.write('Линейный график динамики чаевых')
    plt.figure(figsize=(18,6))
    sns.lineplot(x='time_order', y='tip', data=tips, label='Чаевые')
    plt.title('Динамика чаевых во времени')
    plt.xlabel('Даты')
    plt.ylabel('Чаевые в USD')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()
    fig1= plt.gcf()

    

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    fig1.savefig(buffer, format='png')
    buffer.seek(0)

    st.sidebar.download_button(
        label="Линейный график",
        data=buffer,
        file_name="linear.png",
        mime="image/png"
    )

    st.pyplot(fig1)
    plt.clf()

    # Гистограмма общего счёт
    st.write('Гистограмма общего счёта')
    plt.figure(figsize=(18,6))
    sns.barplot(data=tips, x='time_order', y='total_bill', color='skyblue')
    plt.title('Общий счёт в разрезе времени')
    plt.xlabel('Даты')
    plt.ylabel('Общий счёт в USD')
    plt.xticks(rotation=90)
    plt.tight_layout()
    fig2= plt.gcf()

    # Save the plot to a BytesIO object
    fig2.savefig(buffer, format='png')
    buffer.seek(0)

    st.sidebar.download_button(
        label="Гистограмма",
        data=buffer,
        file_name="histogram.png",
        mime="image/png"
    )

    st.pyplot(fig2)
    plt.clf()

    # Скаттер влияния Сарумана на Мордор
    st.write('Скаттер плот влияние чаевых на общий счёт размером в кол-во клиентов')
    plt.figure(figsize=(18,6))
    ax = sns.scatterplot(x='tip', y='total_bill',size='size', data=tips)
    plt.title('Как чаевые влияют на количество людей')
    plt.xlabel('Чаевые')
    plt.ylabel('Обший счёт')
    plt.grid(True)
    ax.legend(title='Кол-во людей')
    fig3= plt.gcf()

    # Save the plot to a BytesIO object
    fig3.savefig(buffer, format='png')
    buffer.seek(0)

    st.sidebar.download_button(
        label="Скаттер плот",
        data=buffer,
        file_name="scatterplot.png",
        mime="image/png"
    )

    st.pyplot(fig3)
    plt.clf()

else:
    st.stop()

