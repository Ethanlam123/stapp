import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Define the path for the CSV file
data_file = 'data/expenses.csv'

# Load existing data if available
if os.path.exists(data_file):
    expenses = pd.read_csv(data_file)
    
else:
    expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
    
def display_Table(df):
    # 5 columns: NO, Date, Category, Amount, Description
    col1, col2, col3, col4, col5 = st.columns([0.5, 1, 1, 1, 2])
    col1.write('NO')
    col2.write('Date')
    col3.write('Category')
    col4.write('Amount')
    col5.write('Description') 
    for i in range(len(df)):
        idx = i
        date = df['Date'][i]
        category = df['Category'][i]
        amount = df['Amount'][i]
        description = df['Description'][i]    
        col1.text(idx+1)
        col2.text(date)
        col3.text(category)
        col4.text(amount)
        col5.text(description)
    
        
# Function to save data to CSV
def save_data(frame):
    frame.to_csv(data_file, index=False)

def display_Report():
    st.write('Expenses Recorded:')
    st.write('Total Expenses:', expenses['Amount'].sum())
    st.write(expenses.groupby('Category')['Amount'].sum())
    with st.expander('All Expenses'):
        # st.write(expenses)
        display_Table(expenses)
        

    
def display_Chart():
    fig = px.pie(expenses, names='Category', values='Amount', title='Expenses by Category')
    st.plotly_chart(fig)


# Streamlit UI
st.title('Expense Tracker')

# Input form
with st.form('expense_form', clear_on_submit=True):
    date = st.date_input('Date')
    category = st.selectbox('Category', ['🍱Food', '🚗Transport', '🧽Utilities', '🎳Entertainment', '🎈Others'])
    amount = st.number_input('Amount', min_value=0.0, format='%f')
    description = st.text_area('Description')
    submitted = st.form_submit_button('Submit')
    if description == '':
        description = '-'

    if submitted:
        # Append new expense
        new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
        expenses = pd.concat([expenses, new_expense], ignore_index=True)
        save_data(expenses)
        st.success('Expense added successfully!')

# Show data table
table, chart = st.tabs(['Table', 'Chart'])
with table:
    display_Report()
with chart:
    display_Chart()