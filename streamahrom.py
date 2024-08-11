import pandas as pd
import plotly.graph_objs as go
import streamlit as st
import asyncio
from tsetmc.instruments import Instrument

# توابع هم‌روند برای دریافت داده‌ها

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

# تابع اصلی برای مدیریت داده‌ها و نمودارها
def main():
    st.title('بررسی حباب صندوق‌ها')
    
    # انتخاب نوع صندوق توسط کاربر
    option = st.selectbox("انتخاب نوع صندوق", ["ETF", "اهرم", "طلا"])

    # اجرای تابع هم‌روند و نمایش داده‌ها
    df = None
    if option == "ETF":
        df = asyncio.run(hobab_ETF())
    elif option == "اهرم":
        df = asyncio.run(hobab_ahrom())
    else:
        df = asyncio.run(hobab_tala())

    if df is not None:
        # نمایش داده‌ها
        st.write(df)
        
        # ایجاد نمودار حباب
        def create_hobab_plot(df):
            trace = go.Bar(
                x=df.index,
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
                x=df.index,
                y=df['Leverage'],  # اطمینان حاصل کنید که ستون 'Leverage' در df موجود است
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

        df2 = df.iloc[:, 1:].round(3)
        st.write(df2)

        # نمایش نمودار حباب
        hobab_plot = create_hobab_plot(df)
        st.plotly_chart(hobab_plot)

        # نمایش نمودار اهرم و پراکندگی در صورت انتخاب گزینه 'اهرم'
        if option == "اهرم" and 'Leverage' in df.columns:
            leverage_plot = create_leverage_plot(df)
            st.plotly_chart(leverage_plot)

    st.write("Produced By Taha Sadeghizadeh")

if __name__ == "__main__":
    main()
