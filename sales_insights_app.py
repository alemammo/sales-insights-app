import streamlit as st
import pandas as pd

# Load sales data from an Excel file
file_path = 'All Sales and Payments.xlsx'  # Ensure this file is in the same directory
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

# Date Range Filter
st.subheader("Filter by Year Range")
all_years = sorted(data_df['Orig Date'].dt.year.unique())
selected_option = st.radio("Choose a time range:", ['All Time', 'Custom Range'])

if selected_option == 'Custom Range':
    start_year = st.selectbox("Start Year", all_years)
    end_year = st.selectbox("End Year", [year for year in all_years if year >= start_year])
    filtered_data = data_df[
        (data_df['Client Name'] == selected_client) &
        (data_df['Orig Date'].dt.year >= start_year) &
        (data_df['Orig Date'].dt.year <= end_year)
    ]
else:
    filtered_data = data_df[data_df['Client Name'] == selected_client]

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

# List clients by payment average
st.subheader("List Clients by Average Payment Time")
payment_time_filter = st.selectbox("Show clients with average payment time less than:", [30, 45, 60])

# Calculate payment time averages for all clients
clients_avg_payment_time = data_df.groupby('Client Name')['Days \'til Paid'].mean().reset_index()
filtered_clients = clients_avg_payment_time[clients_avg_payment_time['Days \'til Paid'] < payment_time_filter]

st.write(f"Clients with average payment time less than {payment_time_filter} days:")
st.dataframe(filtered_clients)
