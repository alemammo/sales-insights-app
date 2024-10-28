import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Load sales data from an updated Excel file
file_path = 'All Sales and Payments - Clients - salesperson State'  # Ensure this updated file is in the directory
data_df = pd.read_excel(file_path)

# Clean up column names (strip spaces and standardize)
data_df.columns = data_df.columns.str.strip()

# Convert "Orig Date" to datetime format
data_df['Orig Date'] = pd.to_datetime(data_df['Orig Date'])

# Streamlit App
st.title("Company Sales Insights")

# Filter by salesperson and state
salespeople = data_df['Salesperson'].unique()
states = data_df['State'].unique()

selected_salesperson = st.selectbox("Select Salesperson", salespeople)
selected_state = st.multiselect("Select States", states)

# Filter the data based on salesperson and state
filtered_data = data_df[(data_df['Salesperson'] == selected_salesperson) & 
                        (data_df['State'].isin(selected_state))]

# Inactivity Period Filter
st.subheader("Filter by Inactivity Period")
inactivity_period = st.slider("Select inactivity period in months", 1, 12, 1)
cutoff_date = datetime.now() - timedelta(days=inactivity_period * 30)

# Find clients with no activity in the specified period
inactive_clients = filtered_data.groupby('Client Name').filter(
    lambda x: x['Orig Date'].max() < cutoff_date
)

# Display inactive clients
st.header(f"Inactive Clients for {selected_salesperson} in {', '.join(selected_state)}")
st.write(f"Clients with no activity in the last {inactivity_period} months:")
st.dataframe(inactive_clients[['Client Name', 'Orig Date', 'State', 'Salesperson']])

# Calculate and display insights for the selected salesperson and state
if not inactive_clients.empty:
    # Calculate statistics
    average_time_to_pay = inactive_clients['Days \'til Paid'].mean()
    average_purchase_amount = inactive_clients['Sale Amount'].mean()
    largest_purchase = inactive_clients['Sale Amount'].max()
    largest_purchase_date = inactive_clients.loc[inactive_clients['Sale Amount'].idxmax(), 'Orig Date']
    total_amount_invoices = inactive_clients['Sale Amount'].sum()

    # Display results
    st.header(f"Sales Insights for {selected_salesperson}")
    st.write(f"### Average Time to Pay: {average_time_to_pay:.2f} days")
    st.write(f"### Average Purchase Amount: ${average_purchase_amount:.2f}")
    st.write(f"### Largest Purchase: ${largest_purchase:.2f} on {largest_purchase_date.strftime('%Y-%m-%d')}")
    st.write(f"### Total Amount of Invoices: ${total_amount_invoices:.2f}")
else:
    st.write("No inactive clients found for the selected period.")
