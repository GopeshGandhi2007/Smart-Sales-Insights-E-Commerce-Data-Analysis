# pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# --- Sample Dataset ---
data = {
    'order_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'product': ['Shoes', 'Shirt', 'Shoes', 'Watch', 'Shirt', 'Shoes', 'Watch', 'Shirt'],
    'quantity': [1, 2, 1, 1, 3, 2, 2, 1],
    'price': [1000, 500, 1000, 2000, 500, 1000, 2000, 500],
    'order_date': pd.to_datetime([
        '2024-01-05', '2024-01-12', '2024-02-03', '2024-02-15',
        '2024-03-20', '2024-03-25', '2024-04-10', '2024-04-22'
    ])
}
df = pd.DataFrame(data)
df['total'] = df['quantity'] * df['price']
df['month'] = df['order_date'].dt.strftime('%b')
df['month_num'] = df['order_date'].dt.month

# --- KPIs ---
st.title("E-Commerce Sales Dashboard")
total_revenue = df['total'].sum()
order_count = df['order_id'].nunique()
avg_basket_size = total_revenue / order_count

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue}")
col2.metric("Total Orders", order_count)
col3.metric("Avg Basket Size", f"₹{avg_basket_size:.2f}")

st.markdown("---")

# --- Charts Section ---
col4, col5 = st.columns(2)

with col4:
    st.subheader("Monthly Sales Trend")
    monthly_sales = df.groupby('month')['total'].sum().reindex(['Jan','Feb','Mar','Apr'])
    fig1, ax1 = plt.subplots()
    ax1.plot(monthly_sales.index, monthly_sales.values, marker='o', color='blue')
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales (₹)")
    st.pyplot(fig1)

with col5:
    st.subheader("Product Revenue Share")
    product_rev = df.groupby('product')['total'].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(product_rev, labels=product_rev.index, autopct='%1.1f%%')
    st.pyplot(fig2)

st.markdown("---")

# --- Heatmap ---
st.subheader("Monthly Sales Heatmap")
heatmap_data = df.groupby(['product', 'month'])['total'].sum().reset_index()
heatmap_pivot = heatmap_data.pivot(index='product', columns='month', values='total').fillna(0)
fig3 = px.imshow(
    heatmap_pivot,
    text_auto=True,
    color_continuous_scale='Blues',
    labels=dict(x="Month", y="Product", color="Sales (₹)")
)
st.plotly_chart(fig3, use_container_width=True)

# --- Top Products ---
st.subheader("Top Products")
top_products = df.groupby('product')['quantity'].sum().sort_values(ascending=False).head(3)
for prod, qty in top_products.items():
    st.write(f"**{prod}** — {qty} units sold")

# --- Filter Sidebar ---
st.sidebar.header("Filter Transactions")
months = df['month'].unique().tolist()
products = df['product'].unique().tolist()
selected_months = st.sidebar.multiselect("Select Month", options=months, default=months)
selected_products = st.sidebar.multiselect("Select Product", options=products, default=products)

filtered_df = df[
    (df['month'].isin(selected_months)) & (df['product'].isin(selected_products))
]

# --- Filtered Table ---
st.subheader("Filtered Transactions")
st.dataframe(filtered_df[['order_id', 'order_date', 'product', 'quantity', 'price', 'total']])

# --- Drill-down Explorer ---
st.subheader(" Drill-down by Product")
selected_drill = st.selectbox("Select a product to explore:", df['product'].unique())
product_df = df[df['product'] == selected_drill].sort_values(by='order_date')
st.write(f"Showing orders for *{selected_drill}*:")
st.dataframe(product_df[['order_id', 'order_date', 'quantity', 'price', 'total']])
