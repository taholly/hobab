import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.express as px

# بارگذاری داده‌ها از URL
def load_data(option):
    if option == "طلا":
        file_name = "tala.xlsx"
    elif option == "اهرم":
        file_name = "ahromi.xlsx"
        file_name2 = "AHROMCOMB.xlsx"
    else:
        file_name = "ETF.xlsx"

    # بارگذاری فایل اصلی
    url = f'https://raw.githubusercontent.com/taholly/hobab/main/{file_name}'
    response = requests.get(url)
    
    if response.status_code == 200:
        file = BytesIO(response.content)
        try:
            df = pd.read_excel(file, engine='openpyxl')
            if option == "طلا":
                df.pop("Unnamed: 0")
                df = df.sort_values(by="real_hobab")
                df.drop(columns=['نماد', "hobab_gold", "hobab_coin", "p_of_others", "p_of_coin", "p_of_gold"], inplace=True)
            else:
                df.pop("nemad")
                df = df.rename(columns={"Unnamed: 0": "nemad"})

            # اگر اهرم انتخاب شود، فایل دوم را بارگذاری کنید
            if option == "اهرم":
                url2 = f'https://raw.githubusercontent.com/taholly/hobab/main/{file_name2}'
                response2 = requests.get(url2)
                if response2.status_code == 200:
                    file2 = BytesIO(response2.content)
                    df1 = pd.read_excel(file2, engine='openpyxl')
                    return df, df1  # بازگشت دو دیتا فریم برای اهرم
                else:
                    st.error(f"دریافت فایل دوم شکست خورد: {response2.status_code}")
                    return df, None  # در صورت خطا، فقط df را بازگردانید

            return df
        except Exception as e:
            st.error(f"خطا در خواندن فایل Excel: {e}")
            return None
    else:
        st.error(f"دریافت فایل شکست خورد: {response.status_code}")
        return None

# ایجاد نمودار پای‌چارت برای یک سطر
def create_pie_chart(row, labels):
    values = row.values
    fig = px.pie(values=values, names=labels, title='نمودار پای‌چارت برای سطر انتخابی')
    return fig

# رابط کاربری Streamlit
st.sidebar.markdown(
    "<style>.sidebar .sidebar-content { background: #2C3E50; color: blue; }</style>",
    unsafe_allow_html=True
)
option = st.sidebar.radio("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", ("ETF", "طلا", "اهرم"))
st.title(f"محاسبه ی حباب صندوق‌های {option}")

# بارگذاری داده‌ها
if option == "اهرم":
    df, df1 = load_data(option)
else:
    df = load_data(option)

if df is not None:
    df = df.round(3)
    
    # نمایش جدول اصلی
    st.dataframe(df)

    # نمایش نمودار حباب یا نمودارهای اضافی در صورت انتخاب "اهرم"
    if option == "اهرم" and df1 is not None:
        # لیست صندوق‌ها برای انتخاب
        funds = ["اهرم", "توان", "موج", "نارنج اهرم", "شتاب", "جهش", "بیدار"]
        
        # انتخاب صندوق توسط کاربر
        selected_fund = st.selectbox("یکی از صندوق‌ها را انتخاب کنید:", funds)
        
        # فیلتر سطر مربوطه از df1
        selected_row = df1[df1['صندوق'] == selected_fund]
        
        if not selected_row.empty:
            selected_row = selected_row.iloc[0]
            labels = df1.columns.drop('صندوق')  # فرض می‌کنیم ستون اول نام صندوق است و بقیه ستون‌ها درصد هستند

            # رسم نمودار پای چارت
            pie_chart = create_pie_chart(selected_row[labels], labels)
            st.plotly_chart(pie_chart)
        else:
            st.warning(f"صندوق {selected_fund} یافت نشد.")

st.write("Produced By Taha Sadeghizadeh")
