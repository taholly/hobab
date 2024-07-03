import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import matplotlib.pyplot as plt


url = 'https://raw.githubusercontent.com/taholly/hobab/main/ahromi'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        df = pd.read_excel(file, engine='openpyxl')
        print(df.head())  # چاپ چند ردیف اول برای بررسی
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
else:
    print(f"Failed to retrieve file: {response.status_code}")

import streamlit as st
from bokeh.plotting import figure , show
from bokeh.models import ColumnDataSource
import pandas as pd


# In[4]:



# In[7]:


df = df.rename(columns={'Unnamed: 0' : "nemad"})


# In[8]:


df.set_index(df['nemad'])


# In[13]:


def make_plot():
    x = df['nemad']
    y1 = df['hobab']
    y2 = df['Leverage']

    # ایجاد نمودار با استفاده از Bokeh
    p = figure(x_range=x, height=350, title="حباب صندوق و اهرم کلاسیک",
               toolbar_location=None, tools="", width=600)

    # اضافه کردن میله‌های عمودی برای هر دو ستون
    p.vbar(x=[i for i in range(len(x))], top=y1, width=0.4, color="blue", legend_label="Hobab")
    p.vbar(x=[i + 0.4 for i in range(len(x))], top=y2, width=0.4, color="green", legend_label="Leverage")


    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
    p.legend.location = "top_left"

# In[20]:


plot = make_plot()


# In[21]:


st.title("محاسبه ی حباب صندوق های اهرمی  و ضریب اهرمی صندوق ها ")
st.write("را بزنید rerun برای به روز رسانی نمودار هر چند دقیقه یکبار گزینه ی ")

st.write(df)

st.bokeh_chart(plot, use_container_width=True)

st.write("Produced By Taha Sadeghizadeh")
