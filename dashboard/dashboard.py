# Import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style untuk visualisasi
sns.set(style='dark')

# Fungsi untuk menghitung total penyewaan berdasarkan jam
def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    return hour_count_df

# Fungsi untuk memfilter data berdasarkan tahun 2011
def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

# Fungsi untuk menghitung total penyewaan oleh pengguna terdaftar (registered)
def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
    return reg_df

# Fungsi untuk menghitung total penyewaan oleh pengguna casual
def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({
        "casual": ["sum"]
    })
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
    return cas_df

# Fungsi untuk menghitung total penyewaan berdasarkan jam
def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

# Fungsi untuk menghitung total penyewaan berdasarkan musim
def macem_season(day_df):
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index()
    return season_df

# Load dataset
days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

# Konversi kolom tanggal ke tipe datetime
datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)
hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

# Menentukan rentang tanggal minimum dan maksimum
min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()
min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

# Sidebar untuk input rentang waktu
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn.vectorstock.com/i/1000x1000/37/87/bicycle-sharing-system-rgb-color-icon-vector-35393787.webp")
    
    # Input rentang tanggal
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

# Filter data berdasarkan rentang tanggal yang dipilih
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

# Menghitung data untuk visualisasi
hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_days)

# Header dashboard
st.header('Bike Sharing Dashboard :sparkles:')

# Menampilkan metrik harian
st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

# Visualisasi performa penyewaan sepeda dalam beberapa tahun terakhir
st.subheader("Performa Penyewaan Sepeda dalam Beberapa Tahun Terakhir")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["count_cr"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Visualisasi jam penyewaan terbanyak dan tersedikit
st.subheader("Jam Penyewaan Terbanyak dan Tersedikit")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan Banyak Penyewa Sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)", fontsize=30)
ax[1].set_title("Jam dengan Sedikit Penyewa Sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Visualisasi musim penyewaan terbanyak
st.subheader("Musim Penyewaan Terbanyak")
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="count_cr", 
    x="season",
    data=season_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Visualisasi perbandingan pengguna terdaftar vs casual
st.subheader("Perbandingan Pengguna Terdaftar vs Casual")
labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  
st.pyplot(fig1)