import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import pytest

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

        # New plot: quantity sold by product
        fig2, ax2 = plt.subplots()
        data.groupby('Product')['Quantity'].sum().plot(kind='bar', color='orange', ax=ax2)
        ax2.set_ylabel('Quantity Sold')
        ax2.set_title('Total Quantity Sold by Product')
        st.pyplot(fig2)

        # Adding a new plot for sales trend over time
        # Plot sales trend over time
        fig3, ax3 = plt.subplots()
        data['Date'] = pd.to_datetime(data['Date'])  # Ensure 'Date' is in datetime format
        data.groupby('Date')['Revenue'].sum().plot(ax=ax3)
        ax3.set_ylabel('Revenue')
        ax3.set_title('Sales Trend Over Time')
        st.pyplot(fig3)

        # Adding state and country columns to the data
        if 'State' not in data.columns:
            data['State'] = ''  # Placeholder for State
        if 'Country' not in data.columns:
            data['Country'] = ''  # Placeholder for Country

        # New plot: Revenue by State
        if 'State' in data.columns and not data['State'].isnull().all():
            fig4, ax4 = plt.subplots()
            revenue_by_state = data.groupby('State')['Revenue'].sum()
            revenue_by_state.plot(kind='bar', color='green', ax=ax4)
            ax4.set_ylabel('Revenue')
            ax4.set_title('Revenue by State')
            st.pyplot(fig4)

        # New plot: Revenue by Country
        if 'Country' in data.columns and not data['Country'].isnull().all():
            fig5, ax5 = plt.subplots()
            revenue_by_country = data.groupby('Country')['Revenue'].sum()
            revenue_by_country.plot(kind='bar', color='purple', ax=ax5)
            ax5.set_ylabel('Revenue')
            ax5.set_title('Revenue by Country')
            st.pyplot(fig5)

elif page == "Upload":
    st.title("⬆️ Upload Sales Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        # Ensure 'Date' is in datetime format
        new_data['Date'] = pd.to_datetime(new_data['Date'])

        # Check if required columns exist in the uploaded file
        required_columns = ['Date', 'Product', 'Quantity', 'Revenue']
        if set(required_columns).issubset(new_data.columns):
            save_data(new_data)
            st.success("File uploaded and data saved!")
        else:
            st.error(
                "CSV must contain columns: Date, Product, Quantity, Revenue."
            )
    st.write("You can upload a new sales data file to update the dashboard.")


# Adding unit tests for data integrity and plot functionality

def test_load_data():
    df = load_data()
    assert isinstance(df, pd.DataFrame), "Data should be loaded as a DataFrame"
    assert set(['Date', 'Product', 'Quantity', 'Revenue']).issubset(
        df.columns
    ), "DataFrame should have required columns"

def test_save_data():
    test_df = pd.DataFrame({
        'Date': ['2025-11-01'],
        'Product': ['Widget'],
        'Quantity': [10],
        'Revenue': [200]
    })
    save_data(test_df)
    df = load_data()
    assert not df.empty, "Data should be saved and loaded correctly"
    assert 'Widget' in df['Product'].values, (
        "Saved data should contain the test product"
    )


# Ensure proper spacing before test_dashboard_plots
def test_dashboard_plots():
    df = load_data()
    if not df.empty:
        assert 'State' in df.columns, "State column should exist in the data"
        assert 'Country' in df.columns, (
            "Country column should exist in the data"
        )