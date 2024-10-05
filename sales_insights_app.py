import streamlit as st
import pandas as pd

# Load sales data from an Excel file
file_path = 'All Sales and Payments.xlsx'  # Update this with your file's name and path
data_df = pd.read_excel(file_path)

# Clean up column names (strip spaces and standardize)
data_df.columns = data_df.columns.str.strip()

# Convert "Orig Date" to datetime format
data_df['Orig Date'] = pd.to_datetime(data_df['Orig Date'])

# Streamlit App
st.title("Company Sales Insights")

# Filter by client name
client_names = data_df['Client Name'].unique()
selected_client = st.selectbox("Select a client", client_names)

# Filter by date (month and year)
selected_year = st.selectbox("Select Year", data_df['Orig Date'].dt.year.unique())
selected_month = st.selectbox("Select Month", data_df['Orig Date'].dt.month_name().unique())

# Apply filters
filtered_data = data_df[
    (data_df['Client Name'] == selected_client) & 
    (data_df['Orig Date'].dt.year == selected_year) & 
    (data_df['Orig Date'].dt.month_name() == selected_month)
]

# Calculate statistics
average_time_to_pay = filtered_data['Days \'til Paid'].mean()
average_purchase_amount = filtered_data['Sale Amount'].mean()
largest_purchase = filtered_data['Sale Amount'].max()
largest_purchase_date = filtered_data.loc[filtered_data['Sale Amount'].idxmax(), 'Orig Date']
total_amount_invoices = filtered_data['Sale Amount'].sum()

# Display results
st.header(f"Sales Insights for {selected_client}")
st.write(f"### Average Time to Pay: {average_time_to_pay:.2f} days")
st.write(f"### Average Purchase Amount: ${average_purchase_amount:.2f}")
st.write(f"### Largest Purchase: ${largest_purchase:.2f} on {largest_purchase_date.strftime('%Y-%m-%d')}")
st.write(f"### Total Amount of Invoices: ${total_amount_invoices:.2f}")
