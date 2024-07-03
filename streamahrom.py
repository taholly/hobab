import pandas as pd
import requests
from io import BytesIO
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d



option = st.sidebar.radio("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
("طلا","اهرم"))

if option == "طلا":
    fi = "tala.xlsx"
else:
    fi = "ahromi"

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


def make_hobab_plot():
    x = df['nemad']
    y = df['hobab]

    p = figure(x_range=x, height=350, title="حباب صندوق",
               toolbar_location=None, tools="", width=600)

    p.vbar(x=[i for i in range(len(x))], top=y, width=0.4, color="blue")

    p.xgrid.grid_line_color = None
    p.y_range.start = min(df['hobab].min() , 0)
    p.xaxis.major_label_orientation = 1
   

    return p


def make_leverage_plot():
    x = df['nemad']
    y = df['Leverage']
    
    p = figure(x_range=x, height=350, title="اهرم صندوق",
               toolbar_location=None, tools="", width=600)
    p.vbar(x=[i for i in range(len(x))], top=y, width=0.4, color="green")

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
   
    return p

# نمایش عنوان و نمودارها با استفاده از Streamlit
#st.title("محاسبه ی حباب صندوق های اهرمی و ضریب اهرمی صندوق ها")
st.write("را بزنید rerun برای به روز رسانی نمودار هر چند دقیقه یکبار گزینه ی ")

# ایجاد نمودارها
hobab_plot = make_hobab_plot()


st.bokeh_chart(hobab_plot, use_container_width=True)

if fi == "ahromi":
    leverage_plot = make_leverage_plot()
    st.bokeh_chart(leverage_plot, use_container_width=True)

st.write("Produced By Taha Sadeghizadeh")
