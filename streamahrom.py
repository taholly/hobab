import pandas as pd
import requests
from io import BytesIO
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import FactorRange

# ایجاد گزینه‌های انتخاب در نوار کناری
option = st.sidebar.radio("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", ("طلا", "اهرم"))

# انتخاب فایل بر اساس گزینه انتخاب شده
if option == "طلا":
    fi = "tala.xlsx"
else:
    fi = "ahromi"

# بارگذاری داده‌ها از URL
url = f'https://raw.githubusercontent.com/taholly/hobab/main/{fi}'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        df = pd.read_excel(file, engine='openpyxl')
        st.write("Dataframe loaded successfully:")
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.error(f"Failed to retrieve file: {response.status_code}")

# اصلاح نام ستون
df = df.rename(columns={'Unnamed: 0': "nemad"})
st.write(df)

# تابع برای ایجاد نمودار حباب
def make_hobab_plot():
    x = list(df['nemad'])
    y = df['hobab']

    p = figure(x_range=FactorRange(*x), height=350, title="حباب صندوق",
               toolbar_location=None, tools="", width=600)

    p.vbar(x=x, top=y, width=0.4, color="blue")

    p.xgrid.grid_line_color = None
    p.y_range.start = min(df['hobab'].min(), 0)
    p.xaxis.major_label_orientation = 1

    return p

# تابع برای ایجاد نمودار اهرم
def make_leverage_plot():
    x = list(df['nemad'])
    y = df['Leverage']
    
    p = figure(x_range=FactorRange(*x), height=350, title="اهرم صندوق",
               toolbar_location=None, tools="", width=600)
    p.vbar(x=x, top=y, width=0.4, color="green")

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
   
    return p

# نمایش عنوان و نمودارها با استفاده از Streamlit
st.write("برای به روز رسانی نمودار هر چند دقیقه یکبار گزینه 'Rerun' را بزنید.")

# ایجاد نمودارها
hobab_plot = make_hobab_plot()
st.bokeh_chart(hobab_plot, use_container_width=True)

# نمایش نمودار اهرم در صورت انتخاب فایل "اهرم"
if fi == "ahromi":
    leverage_plot = make_leverage_plot()
    st.bokeh_chart(leverage_plot, use_container_width=True)

st.write("Produced By Taha Sadeghizadeh")
