import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.graph_objs as go
import streamlit as st
import asyncio
from tsetmc.instruments import Instrument
import pandas as pd
import streamlit as st
import asyncio
import nest_asyncio
from tsetmc.instruments import Instrument
import pandas as pd

# استفاده از nest_asyncio برای تنظیم حلقه‌های هم‌روند
nest_asyncio.apply()

async def hobab_tala():
    dictdf = {}
    gold_funds = ["طلا", "آلتون", "تابش", "جواهر", "زر", "زرفام", "عیار", "کهربا", "گنج", "گوهر", "مثقال", "ناب", "نفیس", "نفیس"]
    for fund in gold_funds:
        inst = await Instrument.from_search(fund)
        live = await inst.live_data()
        price = live['pl']
        nav = live['nav']
        time = live['nav_datetime']
        dictdf[fund] = [fund, price, nav, time] 
        
    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df

async def hobab_ahrom():
    dictdf = {}
    leveraged_funds = ["اهرم", "توان", "موج", "نارنج اهرم", "شتاب", "جهش", "بیدار"]
    for fund in leveraged_funds:
        inst = await Instrument.from_search(fund)
        live = await inst.live_data()
        price = live['pl']
        nav = live['nav']
        time = live['nav_datetime']
        dictdf[fund] = [fund, price, nav, time] 
        
    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df

async def hobab_ETF():
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
        inst = await Instrument.from_search(fund)
        live = await inst.live_data()
        price = live['pl']
        nav = live['nav']
        time = live['nav_datetime']
        dictdf[fund] = [fund, price, nav, time] 
        
    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df

def run_async_function(coro):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # اگر حلقه هم‌روند در حال اجراست، از `asyncio.create_task` استفاده می‌کنیم
        task = asyncio.create_task(coro)
        return loop.run_until_complete(task)
    else:
        # اگر حلقه هم‌روند در حال اجرا نیست، از `loop.run_until_complete` استفاده می‌کنیم
        return loop.run_until_complete(coro)




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

# اجرای تابع هم‌روند بر اساس گزینه انتخابی و نمایش داده‌ها
if option == "ETF":
    df = run_async_function(hobab_ETF())
elif option == "اهرم":
    df = run_async_function(hobab_ahrom())
else:
    df = run_async_function(hobab_tala())





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
