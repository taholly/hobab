import asyncio
import nest_asyncio
import streamlit as st
from tsetmc.instruments import Instrument
import pandas as pd

# اجرای nest_asyncio برای حل مشکلات مربوط به حلقه رویداد
nest_asyncio.apply()

async def fetch_data(fund_list):
    dictdf = {}
    for fund in fund_list:
        inst = await Instrument.from_search(fund)
        live = await inst.live_data()
        price = live['pl']
        nav = live['nav']
        time = live['nav_datetime']
        dictdf[fund] = [fund, price, nav, time] 

    df = pd.DataFrame(dictdf, index=["nemad", 'Price', 'NAV', "Time"])
    df = df.T.assign(hobab=(df.T["Price"] - df.T["NAV"]) / df.T["NAV"])
    return df

async def main(option):
    if option == "ETF":
        etf_funds = ["آتیمس", "آساس", "تاراز", "آوا", "ارزش", "نارین", "افق ملت", "الماس", "پیروز", "انار", 
                     "اوج", "بازبیمه", "بهین رو", "پتروآبان", "پتروداریوش", "پتروصبا", "پتروما", "سمان", 
                     "پتروآگاه", "متال", "رویین", "تخت گاز", "استیل", "فلزفارابی", "آذرین", "بذر", 
                     "پادا", "پالایش", "پرتو", "کاردان", "ترمه", "اطلس", "ثروتم", "ثمین", "داریوش", 
                     "ثهام", "هامون", "هیوا", "جاودان", "برلیان", "دریا", "رماس", "زرین", "ثنا", 
                     "سرو", "سلام", "آبنوس", "ویستا", "اکسیژن", "بیدار", "توان", "جهش", "شتاب", 
                     "اهرم", "موج", "نارنج اهرم", "سپینود", "تیام", "ثروت ساز", "کاریس", "هوشیار", 
                     "فیروزه", "آرام", "وبازار", "صدف", "فراز", "فارما کیان", "درسا", "هم وزن", "خلیج", 
                     "مدیر", "مروارید", "تکپاد", "عقیق", "آگاس", "دارا یکم"]
        df = await fetch_data(etf_funds)
    elif option == "اهرم":
        leveraged_funds = ["اهرم", "توان", "موج", "نارنج اهرم", "شتاب", "جهش", "بیدار"]
        df = await fetch_data(leveraged_funds)
    else:
        gold_funds = ["طلا", "آلتون", "تابش", "جواهر", "زر", "زرفام", "عیار", "کهربا", "گنج", "گوهر", "مثقال", "ناب", "نفیس", "نفیس"]
        df = await fetch_data(gold_funds)

    return df

def get_data(option):
    return asyncio.run(main(option))

def streamlit_main():
    st.title('بررسی حباب صندوق‌ها')

    option = st.selectbox("انتخاب نوع صندوق", ["ETF", "اهرم", "طلا"])

    # اجرای تابع async با استفاده از asyncio.run
    df = get_data(option)
    
    if df is not None:
        st.write(df)

if __name__ == '__main__':
    streamlit_main()
