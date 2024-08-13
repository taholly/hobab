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
            if option == "طلا":
                df.pop("Unnamed: 0")
                df = df.sort_values(by="real_hobab")
            else:
                df.pop("nemad")
                df = df.rename(columns={"Unnamed: 0":"nemad"})

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
        name='حباب صندوق',
        text=df['hobab'],
        hoverinfo='x+y+text'
    )
    layout = go.Layout(
        title='حباب صندوق',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='حباب', tickformat='.2%'),  # قالب‌بندی درصدی با دو رقم اعشار
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        width=1000,  # Width of the figure
        height=600   # Height of the figure

    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig


# ایجاد نمودار حباب با سه ستون
def create_hobab_comparison_plot(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['nemad'],
        y=df['real_hobab'],
        marker=dict(color='blue'),
        name='Real Hobab',
        text=df['real_hobab'],
        hoverinfo='x+y+text'
    ))

    fig.add_trace(go.Bar(
        x=df['nemad'],
        y=df['hobab'],
        marker=dict(color='orange'),
        name='Hobab',
        text=df['hobab'],
        hoverinfo='x+y+text'
    ))

    fig.add_trace(go.Bar(
        x=df['nemad'],
        y=df['intrinsic_hobab'],
        marker=dict(color='green'),
        name='Intrinsic Hobab',
        text=df['intrinsic_hobab'],
        hoverinfo='x+y+text'
    ))

    fig.update_layout(
        title='مقایسه حباب‌های واقعی، حباب و حباب ذاتی',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='حباب', tickformat='.2%'),
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        width=1000,  # Width of the figure
        height=600
    )
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
        width=1000,  # Width of the figure
        height=600
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig

# تابع برای بولد کردن ارقام
def bold_numbers(val):
    return f'font-weight: bold'

# رابط کاربری Streamlit
st.sidebar.markdown(
    "<style>.sidebar .sidebar-content { background: #2C3E50; color: blue; }</style>",
    unsafe_allow_html=True
)
option = st.sidebar.radio("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", ("ETF", "طلا", "اهرم"))
st.title(f"محاسبه ی حباب صندوق های {option}")

df = load_data(option)
if df is not None:
    df = df.round(3)

    # بولد کردن ارقام در دیتا فریم
    df_styled = df.style.applymap(bold_numbers)

    # نمایش جدول به‌صورت تعاملی
    st.dataframe(df_styled)

    if option == "طلا":
        # نمایش نمودار مقایسه حباب‌ها
        hobab_comparison_plot = create_hobab_comparison_plot(df)
        st.plotly_chart(hobab_comparison_plot)
    else:
        # نمایش نمودار حباب
        hobab_plot = create_hobab_plot(df)
        st.plotly_chart(hobab_plot)

        # نمایش نمودار اهرم و پراکندگی در صورت انتخاب گزینه 'اهرم'
        if option == "اهرم":
            leverage_plot = create_leverage_plot(df)
            st.plotly_chart(leverage_plot)

st.write("Produced By Taha Sadeghizadeh")
