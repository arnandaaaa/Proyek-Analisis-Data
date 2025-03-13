import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data():
    customers_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/customers_dataset.csv")
    orders_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
    payments_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/order_payments_dataset.csv")
    reviews_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/order_reviews_dataset.csv")
    items_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/order_items_dataset.csv")
    products_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/products_dataset.csv")
    sellers_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/sellers_dataset.csv")
    category_translation_df = pd.read_csv("https://raw.githubusercontent.com/arnandaaaa/Proyek-Analisis-Data/refs/heads/main/data/product_category_name_translation.csv")
    
    return customers_df, orders_df, payments_df, reviews_df, items_df, products_df, sellers_df, category_translation_df

customers, orders, payments, reviews, items, products, sellers, category_translation = load_data()

# Sidebar untuk Filter
st.sidebar.title("Filter Data")
start_date = st.sidebar.date_input("Tanggal Mulai", orders["order_purchase_timestamp"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", orders["order_purchase_timestamp"].max())

# Filter Data
filtered_orders = orders[(orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & (orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
filtered_payments = payments[payments['order_id'].isin(filtered_orders['order_id'])]
filtered_items = items[items['order_id'].isin(filtered_orders['order_id'])]

# Nama Dashboard
st.title("📊 E-Commerce Dashboard")

# Matrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Total Order", f"{filtered_orders.shape[0]:,}")
col2.metric("Total Pelanggan", f"{customers.shape[0]:,}")
col3.metric("Total Produk", f"{products.shape[0]:,}")

col4, col5, col6 = st.columns(3)
col4.metric("Total Seller", f"{sellers.shape[0]:,}")
col5.metric("Total Review", f"{reviews.shape[0]:,}")
col6.metric("Total Pembayaran", f"{filtered_payments.shape[0]:,}")

# Kategori Produk Terlaris
st.subheader("Kategori Produk Terlaris")
items_products = filtered_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
items_products = items_products.merge(category_translation, on='product_category_name', how='left')
category_sales = items_products.groupby('product_category_name_english')['order_id'].count().reset_index()
category_sales = category_sales.sort_values(by='order_id', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=category_sales, y='product_category_name_english', x='order_id', palette='Purples_r', ax=ax)
ax.set_xlabel("Jumlah Order")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

#Pendatan Per BUlan
st.subheader("Pendapatan Per Bulan")
payments_orders = filtered_payments.merge(filtered_orders[['order_id', 'order_purchase_timestamp']], on='order_id', how='inner')
payments_orders['order_purchase_timestamp'] = pd.to_datetime(payments_orders['order_purchase_timestamp'])
monthly_spending = payments_orders.groupby(payments_orders['order_purchase_timestamp'].dt.to_period('M'))['payment_value'].sum().reset_index()
monthly_spending['order_purchase_timestamp'] = monthly_spending['order_purchase_timestamp'].astype(str) 

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_spending, x='order_purchase_timestamp', y='payment_value', marker='o', ax=ax)
ax.tick_params(axis='x', labelsize=10)
plt.xticks(rotation=45)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Pendapatan")
st.pyplot(fig)

# Kota dengan Pelanggan Terbanyak
st.subheader("Kota dengan Pelanggan Terbanyak")
top_cities = customers['customer_city'].value_counts().head(10).reset_index()
top_cities.columns = ['customer_city', 'count']

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_cities, y='customer_city', x='count', palette='Purples_r', ax=ax)
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Kota")
st.pyplot(fig)

# Status Pesanan
st.subheader("Status Pesanan")
order_status_count = filtered_orders['order_status'].value_counts().reset_index()
order_status_count.columns = ['order_status', 'count']

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=order_status_count, x='order_status', y='count', palette='Purples_r', ax=ax)
ax.set_xlabel("Status")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

#MEtode pembayaran
st.subheader("Metode Pembayaran")
payment_counts = filtered_payments['payment_type'].value_counts().reset_index()
payment_counts.columns = ['payment_type', 'count']

fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(data=payment_counts, x='payment_type', y='count', palette='Purples_r', ax=ax)
ax.set_xlabel("Metode")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

# Rating Produk
st.subheader("Rating Produk")
fig, ax = plt.subplots(figsize=(7, 5))
sns.countplot(x=reviews['review_score'], palette='mako', ax=ax)
ax.set_xlabel("Review Score")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

st.caption('Copyright © Muh Arnesta Arnanda 2025')
