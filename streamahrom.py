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
        file_name = "ahromi.xlsx"
        file_name2 = "ahromcomb.xlsx"
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

# ایجاد نمودار حباب
def create_hobab_plot(df):
    trace = go.Bar(
        x=df['nemad'],
        y=df['hobab'],
        marker=dict(color='blue'),
        name='حباب صندوق',
        text=df['hobab'],
        hoverinfo='x+y+text'
    )
    layout = go.Layout(
        title='حباب صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='حباب', tickformat='.2%'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        width=800,
        height=600
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig

# ایجاد نمودار اهرم
def create_leverage_plot(df):
    trace = go.Bar(
        x=df['nemad'],
        y=df['Leverage'],
        marker=dict(color='green'),
        name='اهرم صندوق',
        text=df['Leverage'],
        hoverinfo='x+y+text'
    )
    layout = go.Layout(
        title='اهرم صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='اهرم', tickformat='.2f'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        width=800,
        height=600
    )
    fig = go.Figure(data=[trace], layout=layout)
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
    
    # نمایش جدول
    st.dataframe(df)

    # نمایش نمودار حباب یا نمودارهای اضافی در صورت انتخاب "اهرم"
    if option == "طلا":
        # اینجا می‌توانید نمودار مرتبط با طلا را نمایش دهید
        st.write("نمودار طلا را اینجا نمایش دهید")
    else:
        # نمایش نمودار حباب
        hobab_plot = create_hobab_plot(df)
        st.plotly_chart(hobab_plot)

        if option == "اهرم":
            # نمایش نمودار اهرم
            leverage_plot = create_leverage_plot(df)
            st.plotly_chart(leverage_plot)
            
            # بررسی و نمایش df1 (دیتافریم دوم)
            if df1 is not None:
                st.write("داده‌های اضافی از فایل AHROMCOMB.xlsx:")
                st.dataframe(df1)

st.write("Produced By Taha Sadeghizadeh")
