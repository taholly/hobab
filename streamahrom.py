import pandas as pd
import requests
from io import BytesIO
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
# بارگذاری داده‌ها از URL
def load_data(option):
    if option == "طلا":
        file_name = "tala.xlsx"
    elif option == "اهرم":
        file_name = "ahromi"
        file_name2 = "ahromcomb1.xlsx"
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
                df.drop(columns=['نماد', "hobab_gold", "hobab_coin", "p_of_others", "p_of_coin", "p_of_gold"], inplace=True)
                return df
            elif option == 'اهرم':
                df.pop("nemad")
                df = df.rename(columns={"Unnamed: 0": "nemad"})
                
                url = f'https://raw.githubusercontent.com/taholly/hobab/main/{file_name2}'
                response = requests.get(url)
                if response.status_code == 200:
                    file = BytesIO(response.content)
                    try:
                        df1 = pd.read_excel(file, engine='openpyxl')
                        df1.pop("Unnamed: 0")
                        return df , df1
                    except Exception as e:
                        st.error(f"خطا در خواندن فایل Excel: {e}")
                        return None    
            else:
                df.pop("nemad")
                df = df.rename(columns={"Unnamed: 0": "nemad"})

            return df
        except Exception as e:
            st.error(f"خطا در خواندن فایل Excel: {e}")
            return None
    else:
        st.error(f"دریافت فایل شکست خورد: {response.status_code}")
        return None

def create_pie_chart(row, labels):
    values = row.values
    fig = px.pie(values=values, names=labels, title='ترکیب دارایی ها')
    return fig
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
        width=800,  # عرض مناسب‌تر
        height=600
    )
    fig = go.Figure(data=[trace], layout=layout)
    return fig

# ایجاد نمودار مقایسه حباب‌ها
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
        marker=dict(color='green'),
        name='Nominal Hobab',
        text=df['hobab'],
        hoverinfo='x+y+text'
    ))

    fig.update_layout(
        title='مقایسه حباب‌های واقعی و اسمی',
        xaxis=dict(title='نماد'),
        yaxis=dict(title='حباب', tickformat='.2%'),
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        width=800,  # عرض مناسب‌تر
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
        width=800,  # عرض مناسب‌تر
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

if option == "اهرم":
    df, df1 = load_data(option)
else:
    df = load_data(option)
if df is not None:
    df = df.round(3)

    # نمایش جدول
    st.dataframe(df)

    if option == "طلا":
        # نمایش نمودار مقایسه حباب‌ها
        hobab_comparison_plot = create_hobab_comparison_plot(df)
        st.plotly_chart(hobab_comparison_plot)
    else:
        # نمایش نمودار حباب
        hobab_plot = create_hobab_plot(df)
        st.plotly_chart(hobab_plot)
        df1.set_index('صندوق',inplace=True)
        df.set_index('nemad',inplace=True)
        df['Leverage'] = df['Leverage'] * (df1['سهام'] / df1['NAV'])
        df['Leverage'] = df['Leverage'].map('{:,.2f}'.format)
        df1.reset_index()
        df.reset_index()
        leverage_plot = create_leverage_plot(df)
        st.plotly_chart(leverage_plot)
        # لیست صندوق‌ها برای انتخاب
        funds = ["اهرم", "توان", "موج", "نارنج اهرم", "شتاب", "جهش", "بیدار"]
        
        # انتخاب صندوق توسط کاربر
        selected_fund = st.selectbox("یکی از صندوق‌ها را انتخاب کنید:", funds)
        
        # فیلتر سطر مربوطه از df1
        selected_row = df1[df1['صندوق'] == selected_fund]
        st.dataframe(df1)
        df1.pop("NAV")
        if not selected_row.empty:
            selected_row = selected_row.iloc[0]
            labels = df1.columns.drop('صندوق')  # فرض می‌کنیم ستون اول نام صندوق است و بقیه ستون‌ها درصد هستند

            # رسم نمودار پای چارت
            pie_chart = create_pie_chart(selected_row[labels], labels)
            st.plotly_chart(pie_chart)
        else:
            st.warning(f"صندوق {selected_fund} یافت نشد.")
st.write("Produced By Taha Sadeghizadeh")
