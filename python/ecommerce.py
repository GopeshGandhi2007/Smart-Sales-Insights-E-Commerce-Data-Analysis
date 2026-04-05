 # pip install streamlit
# pip install streamlit sqlalchemy pymysql pandas matplotlib plotly

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# --- MySQL Connection using SQLAlchemy ---
user = "root"
password = "TIGER"
host = "localhost"
database = "ecommercedb"

# Create DB connection
try:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    st.success("Connected to Database Successfully")
except Exception as e:
    st.error(f"Failed to connect to Database: {e}")
    st.stop()

# --- Query Data ---
query = """
SELECT 
    t.TransactionID AS order_id,
    p.ProductName AS product,
    tp.Quantity AS quantity,
    p.Price AS price,
    t.TransactionDate AS order_date
FROM `Transaction` t
JOIN TransactionProduct tp ON t.TransactionID = tp.TransactionID
JOIN Product p ON tp.ProductID = p.ProductID;
"""

try:
    df = pd.read_sql(query, engine)
except Exception as e:
    st.error(f"Failed to fetch data: {e}")
    st.stop()

# --- Data Processing ---
df['order_date'] = pd.to_datetime(df['order_date'])
df['total'] = df['quantity'] * df['price']
df['month'] = df['order_date'].dt.strftime('%b')
df['month_num'] = df['order_date'].dt.month

# Sort month names properly
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# --- KPIs ---
st.title("E-Commerce Sales Dashboard")

total_revenue = df['total'].sum()
order_count = df['order_id'].nunique()
avg_basket_size = total_revenue / order_count if order_count != 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Total Orders", order_count)
col3.metric("Avg Basket Size", f"₹{avg_basket_size:,.2f}")

st.markdown("---")

# --- Charts ---
col4, col5 = st.columns(2)

with col4:
    st.subheader("Monthly Sales Trend")
    monthly_sales = (
        df.groupby('month')['total']
        .sum()
        .reindex(month_order)
        .dropna()
    )
    fig1, ax1 = plt.subplots()
    ax1.plot(monthly_sales.index, monthly_sales.values, marker='o', color='blue')
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales (₹)")
    ax1.set_title("Monthly Sales")
    st.pyplot(fig1)

with col5:
    st.subheader("Product Revenue Share")
    product_rev = df.groupby('product')['total'].sum()
    fig2, ax2 = plt.subplots()
    ax2.pie(product_rev, labels=product_rev.index, autopct='%1.1f%%',
            startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

st.markdown("---")

# --- Heatmap ---
st.subheader("Monthly Sales Heatmap")
heatmap_data = df.groupby(['product', 'month'])['total'].sum().reset_index()
heatmap_data['month'] = pd.Categorical(heatmap_data['month'], categories=month_order, ordered=True)
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

st.markdown("---")

# --- Filter Sidebar ---
st.sidebar.header("Filter Transactions")
months = sorted(df['month'].unique(), key=lambda x: month_order.index(x))
products = df['product'].unique().tolist()

selected_months = st.sidebar.multiselect("Select Month", options=month_order, default=months)
selected_products = st.sidebar.multiselect("Select Product", options=products, default=products)

filtered_df = df[
    (df['month'].isin(selected_months)) & (df['product'].isin(selected_products))
]

# --- Filtered Table ---
st.subheader("Filtered Transactions")
st.dataframe(filtered_df[['order_id', 'order_date', 'product', 'quantity', 'price', 'total']])

# --- Drill-down Explorer ---
st.subheader("Drill-down by Product")
selected_drill = st.selectbox("Select a product to explore:", df['product'].unique())
product_df = df[df['product'] == selected_drill].sort_values(by='order_date')

st.write(f"Showing orders for *{selected_drill}*:")
st.dataframe(product_df[['order_id', 'order_date', 'quantity', 'price', 'total']])
    