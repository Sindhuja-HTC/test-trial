import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_PATH = 'data/sales.csv'

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=['Date', 'Product', 'Quantity', 'Revenue'])

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Dashboard", "Upload"))

data = load_data()

if page == "Dashboard":
    st.title("📊 Sales Dashboard")
    if data.empty:
        st.info("No sales data available. Please upload a file.")
    else:
        st.write("### Sales Data", data)
        st.write("---")
        st.write("#### Total Revenue: $", data['Revenue'].sum())
        st.write("#### Total Quantity Sold:", data['Quantity'].sum())
        # Plot revenue by product
        fig, ax = plt.subplots()
        data.groupby('Product')['Revenue'].sum().plot(kind='bar', ax=ax)
        ax.set_ylabel('Revenue')
        ax.set_title('Revenue by Product')
        st.pyplot(fig)

elif page == "Upload":
    st.title("⬆️ Upload Sales Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        if set(['Date', 'Product', 'Quantity', 'Revenue']).issubset(new_data.columns):
            save_data(new_data)
            st.success("File uploaded and data saved!")
        else:
            st.error("CSV must contain columns: Date, Product, Quantity, Revenue.")
    st.write("You can upload a new sales data file to update the dashboard.")
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_PATH = 'data/sales.csv'

def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=['Date', 'Product', 'Quantity', 'Revenue'])

def save_data(df):
    df.to_csv(DATA_PATH, index=False)

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Dashboard", "Upload"))

data = load_data()

if page == "Dashboard":
    st.title("📊 Sales Dashboard")
    if data.empty:
        st.info("No sales data available. Please upload a file.")
    else:
        st.write("### Sales Data", data)
        st.write("---")
        st.write("#### Total Revenue: $", data['Revenue'].sum())
        st.write("#### Total Quantity Sold:", data['Quantity'].sum())
        # Plot revenue by product
        fig, ax = plt.subplots()
        data.groupby('Product')['Revenue'].sum().plot(kind='bar', ax=ax)
        ax.set_ylabel('Revenue')
        ax.set_title('Revenue by Product')
        st.pyplot(fig)

elif page == "Upload":
    st.title("⬆️ Upload Sales Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        if set(['Date', 'Product', 'Quantity', 'Revenue']).issubset(new_data.columns):
            save_data(new_data)
            st.success("File uploaded and data saved!")
        else:
            st.error("CSV must contain columns: Date, Product, Quantity, Revenue.")
    st.write("You can upload a new sales data file to update the dashboard.")
