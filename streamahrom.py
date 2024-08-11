import pandas as pd
import requests
from io import BytesIO
import plotly.graph_objs as go
import streamlit as st
from tsetmc.instruments import Instrument
import asyncio
import nest_asyncio

import streamlit as st
import requests
import pandas as pd
from tsetmc.instruments import Instrument

# توابع غیرهم‌روند برای دریافت داده‌ها

def fetch_data(fund):
    # تغییر تابع برای استفاده از توابع غیرهم‌روندی
    inst = Instrument.from_search_sync(fund)
    live = inst.live_data_sync()
    price = live['pl']
    nav = live['nav']
    time = live['nav_datetime']
    return fund, price, nav, time

def hobab_tala():
    dictdf = {}
    gold_funds = ["طلا", "آلتون", "تابش", "جواهر", "زر", "زرفام", "عیار", "کهربا", "گنج", "گوهر", "مثقال", "ناب", "نفیس", "نفیس"]
    for fund in gold_funds:
        fund, price, nav, time = fetch_data(fund)
        dictdf[fund] = [fund, price, nav, time] 
        
    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df

def hobab_ahrom():
    dictdf = {}
    leveraged_funds = ["اهرم", "توان", "موج", "نارنج اهرم", "شتاب", "جهش", "بیدار"]
    for fund in leveraged_funds:
        fund, price, nav, time = fetch_data(fund)
        dictdf[fund] = [fund, price, nav, time] 
        
    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df

def hobab_ETF():
    dictdf = {}
    etf_funds = ["آتیمس", "آساس", "تاراز", "آوا", "ارزش", "نارین", "افق ملت", "الماس", "پیروز", "انار", 
                 "اوج", "بازبیمه", "بهین رو", "پتروآبان", "پتروداریوش", "پتروصبا", "پتروما", "سمان", 
                 "پتروآگاه", "متال", "رویین", "تخت گاز", "استیل", "فلزفارابی", "آذرین", "بذر", 
                 "پادا", "پالایش", "پرتو", "کاردان", "ترمه", "اطلس", "ثروتم", "ثمین", "داریوش", 
                 "ثهام", "هامون", "هیوا", "جاودان", "برلیان", "دریا", "رماس", "زرین", "ثنا", 
                 "سرو", "سلام", "آبنوس", "ویستا", "اکسیژن", "بیدار", "توان", "جهش", "شتاب", 
                 "اهرم", "موج", "نارنج اهرم", "سپینود", "تیام", "ثروت ساز", "کاریس", "هوشیار", 
                 "فیروزه", "آرام", "وبازار", "صدف", "فراز", "فارما کیان", "درسا", "هم وزن", "خلیج", 
                 "مدیر", "مروارید", "تکپاد", "عقیق", "آگاس", "دارا یکم"]
    for fund in etf_funds:
        fund, price, nav, time = fetch_data(fund)
        dictdf[fund] = [fund, price, nav, time] 
        
    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df




# ایجاد نمودار حباب
def create_hobab_plot(df):
    trace = go.Bar(
        x=df['nemad'],
        y=df['hobab'],
        marker=dict(color='blue'),
        name='حباب صندوق'
    )

    layout = go.Layout(
        title='حباب صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='حباب', tickformat='.2%')  # قالب‌بندی درصدی با دو رقم اعشار
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig

# ایجاد نمودار اهرم
def create_leverage_plot(df):
    trace = go.Bar(
        x=df['nemad'],
        y=df['Leverage'],
        marker=dict(color='green'),
        name='اهرم صندوق'
    )

    layout = go.Layout(
        title='اهرم صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='اهرم', tickformat='.2f')  # قالب‌بندی درصدی بدون اعشار
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig


# انتخاب نوع صندوق توسط کاربر
option = st.selectbox("انتخاب نوع صندوق", ["ETF", "اهرم", "طلا"])

# اجرای تابع و نمایش داده‌ها
if option == "ETF":
    df = hobab_ETF()
elif option == "اهرم":
    df = hobab_ahrom()
else:
    df = hobab_tala()

# نمایش داده‌ها در Streamlit
st.write(df)



df2 = df.iloc[:,1:]
if df2 is not None:
    df2 = df2.round(3)
    st.write(df2)

    # نمایش نمودار حباب
    hobab_plot = create_hobab_plot(df)
    st.plotly_chart(hobab_plot)

    # نمایش نمودار اهرم و پراکندگی در صورت انتخاب گزینه 'اهرم'
    if option == "اهرم":
        leverage_plot = create_leverage_plot(df)
        st.plotly_chart(leverage_plot)



st.write("Produced By Taha Sadeghizadeh")
