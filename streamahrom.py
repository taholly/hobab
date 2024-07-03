import pandas as pd
import requests
from io import BytesIO
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d

# بارگذاری داده‌ها از URL
url = 'https://raw.githubusercontent.com/taholly/hobab/main/ahromi'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        df = pd.read_excel(file, engine='openpyxl')
        st.write("Dataframe loaded successfully:")
        st.write(df.head())  # چاپ چند ردیف اول برای بررسی
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
else:
    st.error(f"Failed to retrieve file: {response.status_code}")

# اصلاح نام ستون
df = df.rename(columns={'Unnamed: 0': "nemad"})

# تابع برای ایجاد نمودار با استفاده از Bokeh
def make_plot():
    x = df['nemad']
    y1 = df['hobab']
    y2 = df['Leverage']

    p = figure(x_range=x, height=350, title="حباب صندوق و اهرم کلاسیک",
               toolbar_location=None, tools="", width=600)

    # اضافه کردن میله‌های عمودی برای هر دو ستون
    p.vbar(x=[i - 0.2 for i in range(len(x))], top=y1, width=0.4, color="blue", legend_label="Hobab", y_range_name='y1')
    p.vbar(x=[i + 0.2 for i in range(len(x))], top=y2, width=0.4, color="green", legend_label="Leverage", y_range_name='y2')

    # تنظیم محور y اصلی
    p.y_range = Range1d(start=0, end=max(y1.max(), y2.max()) * 1.1)
    p.extra_y_ranges = {"y2": Range1d(start=0, end=max(y2) * 1.1)}
    
    # اضافه کردن محور y ثانویه
    p.add_layout(LinearAxis(y_range_name='y2', axis_label="Leverage"), 'right')

    # تنظیمات اضافی
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    return p

# نمایش عنوان و نمودار با استفاده از Streamlit
st.title("محاسبه ی حباب صندوق های اهرمی و ضریب اهرمی صندوق ها")
st.write("را بزنید rerun برای به روز رسانی نمودار هر چند دقیقه یکبار گزینه ی ")

# ایجاد نمودار و نمایش آن
plot = make_plot()
st.bokeh_chart(plot, use_container_width=True)

st.write("Produced By Taha Sadeghizadeh")
