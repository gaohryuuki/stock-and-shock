import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime

st.write("""
# Приложение для просмотра динамики акций компании Apple c начала 2014 по конец 2023 года

Ниже показаны графики ***цены закрытия*** и ***объёма*** акций компании Apple.
         
         """)


tickerSymbol = 'AAPL'
tickerData = yf.Ticker(tickerSymbol)

beginning_date = datetime.strptime('2014-1-01', '%Y-%m-%d')
ending_date = datetime.strptime('2023-12-31', '%Y-%m-%d')

d = st.sidebar.date_input(
    "Выберите даты для поиска",
    (beginning_date, ending_date),
    beginning_date,
    ending_date,
    format="MM-DD-YYYY",
)


start_date = d[0].strftime('%Y-%m-%d')
end_date = d[1].strftime('%Y-%m-%d')

tickerDf = tickerData.history(period='1mo', start=start_date, end=end_date)

st.write(f"""
### Цена закрытия {tickerSymbol}
""")
st.line_chart(tickerDf.Close)

st.write(f"""
### Объём {tickerSymbol}
""")
st.line_chart(tickerDf.Volume)