import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.graph_objs as go


# بارگذاری داده‌ها از URL
def load_data(option):
    if option == "طلا":
        file_name = "tala.xlsx"
    elif option == "اهرم":
        file_name = "ahromi"
    else:
        file_name = "ETF.xlsx"

    url = f'https://raw.githubusercontent.com/taholly/hobab/main/{file_name}'
    response = requests.get(url)

    if response.status_code == 200:
        file = BytesIO(response.content)
        try:
            df = pd.read_excel(file, engine='openpyxl')
            return df
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return None
    else:
        st.error(f"Failed to retrieve file: {response.status_code}")
        return None

def create_hobab_plot(df):
    trace = go.Bar(
        x=df['nemad'],
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
        x=df['nemad'],
        y=df['Leverage'],
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
# رابط کاربری Streamlit
option = st.sidebar.radio("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", ("ETF", "طلا", "اهرم"))
st.title(f"محاسبه ی حباب صندوق های {option}")

df = load_data(option)
if df is not None:
    #df = df.round(3)
    df2 = df.iloc[:,1:]
    st.write(df2)

    # نمایش نمودار حباب
    hobab_plot = create_hobab_plot(df)
    st.plotly_chart(hobab_plot)

    # نمایش نمودار اهرم و پراکندگی در صورت انتخاب گزینه 'اهرم'
    if option == "اهرم":
        leverage_plot = create_leverage_plot(df)
        st.plotly_chart(leverage_plot)
        
st.write("Produced By Taha Sadeghizadeh")
