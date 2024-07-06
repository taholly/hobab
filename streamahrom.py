import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.graph_objs as go

# بارگذاری داده‌ها از URL
def load_data(option):
    if option == "طلا":
        fi = "tala.xlsx"
    elif option == "اهرم":
        fi = "ahromi"
    else:
        fi = "ETF.xlsx"

    url = f'https://raw.githubusercontent.com/taholly/hobab/main/{fi}'
    response = requests.get(url)

    if response.status_code == 200:
        file = BytesIO(response.content)
        try:
            df = pd.read_excel(file, engine='openpyxl')
            df = df.rename(columns={'Unnamed: 0': "nemad"})
            return df
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return None
    else:
        st.error(f"Failed to retrieve file: {response.status_code}")
        return None
#df = df.reindex(df['nemad'])
#df = df.pop(df['nemad'])
# ایجاد نمودار حباب
def create_hobab_plot(df):
    min_value = min(df['hobab'].min() , 0)

    trace = go.Bar(
        x=df['nemad'],
        y=df['hobab'],
        marker=dict(color='blue'),
        name='حباب صندوق'
    )

    layout = go.Layout(
        title='حباب صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='حباب', range=[min_value, df['hobab'].max()])
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_yaxes(tickformat='.2f')
    return fig

# ایجاد نمودار اهرم
def create_leverage_plot(df):
    min_value = min(df['Leverage'].min() , 0)

    trace = go.Bar(
        x=df['nemad'],
        y=df['Leverage'],
        marker=dict(color='green'),
        name='اهرم صندوق'
    )

    layout = go.Layout(
        title='اهرم صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='اهرم', range=[min_value, df['Leverage'].max()])
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_yaxes(tickformat='.0f')
    return fig

# رابط کاربری Streamlit
st.title("محاسبه ی حباب صندوق های اهرمی و ضریب اهرمی صندوق ها")
option = st.sidebar.radio("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", ("ETF" ,"طلا", "اهرم"))

df = load_data(option)
df = df.round(3)
if df is not None:
    st.write(df)

    # نمایش نمودار حباب
    hobab_plot = create_hobab_plot(df)
    st.plotly_chart(hobab_plot)

    # نمایش نمودار اهرم در صورت انتخاب گزینه 'اهرم'
    if option == "اهرم":
        leverage_plot = create_leverage_plot(df)
        st.plotly_chart(leverage_plot)

st.write("Produced By Taha Sadeghizadeh")
