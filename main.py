import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

# Название
st.title('Заполняем пропуски')

# Описание
st.write('Загрузка CSV файла и заполнение пропусков')




## Шаг 1. Загрузить csv файл
uploaded_file = st.sidebar.file_uploader("Выберите файл", type='csv')



if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head(6))
else:
    st.stop()


## Шаг 2. Проверить наличие пропусков в файле
missed_values = df.isna().sum()
missed_values = missed_values[missed_values>0]
st.write(missed_values)

if len(missed_values) > 0:
    fig, ax = plt.subplots()
    sns.barplot(x=missed_values.index, y=missed_values.values)
    ax.set_title('Пропуски в столбцах')
    st.pyplot(fig)
else:
    st.write('Нет пропусков в таблице')
    st.stop()

## Шаг 3. Заполнить пропуски

if len(missed_values) != 0:
    button = st.sidebar.button('Заполнить пропуски')
    if button:
        df_filled = df[missed_values.index].copy()

        for col in df_filled.columns:
            if df_filled[col].dtype == 'object':
                mode = df_filled[col].mode()[0]
                df_filled[col] = df_filled[col].fillna(mode)
            else:
                median = df_filled[col].median()
                df_filled[col] = df_filled[col].fillna(median)

        st.write(df_filled)



## Шаг 4. Выгрузить заполненный от пропусков csv файл
if button:
    st.sidebar.download_button('Скачать файл без пропусков',
                    data=df_filled.to_csv(),
                    file_name=f'{uploaded_file.name[:-4]}filled.csv')