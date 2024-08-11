import asyncio
import pandas as pd
import streamlit as st
from tsetmc.instruments import Instrument
from aiohttp import ClientError

# تابع هم‌روند برای دریافت داده‌ها
async def fetch_data(fund_list):
    dictdf = {}
    for fund in fund_list:
        try:
            inst = await Instrument.from_search(fund)
            live = await inst.live_data()
            price = live.get('pl', None)
            nav = live.get('nav', None)
            time = live.get('nav_datetime', None)
            dictdf[fund] = [fund, price, nav, time]
        except ClientError as e:
            print(f"Error fetching data for {fund}: {e}")
            dictdf[fund] = [fund, None, None, None]
        
    df = pd.DataFrame.from_dict(dictdf, orient='index', columns=['nemad', 'Price', 'NAV', 'Time'])
    df['hobab'] = (df['Price'] - df['NAV']) / df['NAV']
    return df

# تابع اصلی برای مدیریت داده‌ها
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

# تابع برای اجرای توابع هم‌روند و نمایش داده‌ها در Streamlit
def get_data(option):
    return asyncio.run(main(option))

# تابع برای نمایش Streamlit
def streamlit_main():
    st.title('بررسی حباب صندوق‌ها')

    # انتخاب نوع صندوق توسط کاربر
    option = st.selectbox("انتخاب نوع صندوق", ["ETF", "اهرم", "طلا"])

    # اجرای تابع هم‌روند و نمایش داده‌ها
    try:
        df = get_data(option)
        st.write(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    streamlit_main()
