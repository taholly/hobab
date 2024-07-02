import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import matplotlib.pyplot as plt


url = 'https://raw.githubusercontent.com/taholly/hobab/main/ahromi.xlsx'
response = requests.get(url)

if response.status_code == 200:
    file = BytesIO(response.content)
    try:
        df = pd.read_excel(file, engine='openpyxl')
        print(Mrepo.head())  # چاپ چند ردیف اول برای بررسی
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
    y = df['hobab']

    
    p = figure(x_range=x, outer_height=350, title="Fruit Counts",
               toolbar_location=None, tools="")

    p.vbar(x=x, top=y, width=0.5)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    return p


# In[20]:


plot = make_plot()


# In[21]:


st.title("محاسبه ی حباب صندوق های اهرمی  ")

st.write(df)

st.bokeh_chart(plot, use_container_width=True)


st.write("Produced By Taha Sadeghizadeh")
