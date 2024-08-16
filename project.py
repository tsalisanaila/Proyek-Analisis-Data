import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
data = pd.read_csv(r'all_data.csv')  # Ganti dengan path data Anda

# Ubah nama kolom untuk kemudahan akses
data.columns = data.columns.str.strip().str.lower()

# Tambahkan kolom baru untuk jenis hari (hari kerja atau hari libur)
data['day_type'] = data.apply(lambda row: 'Hari Libur' if row['holiday'] == 1 else 'Hari Kerja', axis=1)

# Streamlit layout
st.title('Analisis Data Peminjaman Sepeda')

# Sidebar untuk memilih plot
plot_option = st.sidebar.selectbox(
    "Pilih Plot yang Ingin Dilihat:",
    (
        "Pengaruh Cuaca dan Suhu terhadap Jumlah Peminjaman Sepeda",
        "Tren Penggunaan Sepeda Berdasarkan Musim",
        "Tren Penggunaan Sepeda Berdasarkan Hari Kerja dan Akhir Pekan"
    )
)

# Tampilkan plot berdasarkan pilihan
if plot_option == "Pengaruh Cuaca dan Suhu terhadap Jumlah Peminjaman Sepeda":
    st.subheader('Distribusi Jumlah Peminjaman Berdasarkan Cuaca')
    
    # Plotly boxplot untuk pengaruh cuaca
    box_fig = px.box(data, x='weathersit', y='cnt', 
                     labels={'weathersit': 'Kondisi Cuaca', 'cnt': 'Jumlah Peminjaman'},
                     title='Distribusi Jumlah Peminjaman Berdasarkan Cuaca')
    st.plotly_chart(box_fig)
    
    st.write("""
    **Legenda:** 1 : Cuaca baik (cerah)   2 : Cuaca sedang (berawan)   3 : Cuaca buruk (hujan atau salju)
    
    **Penjelasan:** Boxplot ini menunjukkan distribusi jumlah peminjaman sepeda berdasarkan kondisi cuaca. 
    Secara umum, cuaca memengaruhi jumlah peminjaman sepeda. Kondisi cuaca yang lebih baik cenderung memiliki lebih banyak peminjaman sepeda.
    """)

    st.subheader('Hubungan antara Suhu dan Jumlah Peminjaman Sepeda')
    
    # Plotly scatter plot untuk melihat hubungan suhu dan peminjaman
    scatter_fig = px.scatter(data, x='temp', y='cnt', 
                             labels={'temp': 'Suhu (Normalized)', 'cnt': 'Jumlah Peminjaman'},
                             title='Hubungan antara Suhu dan Jumlah Peminjaman Sepeda',
                             opacity=0.6)
    scatter_fig.update_traces(marker=dict(size=8))
    st.plotly_chart(scatter_fig)
    
    st.write("""
    **Penjelasan:** Scatter plot ini menunjukkan korelasi positif antara suhu dan jumlah peminjaman sepeda, yang berarti, jumlah peminjaman sepeda cenderung meningkat seiring dengan peningkatan suhu.
    """)

elif plot_option == "Tren Penggunaan Sepeda Berdasarkan Musim":
    st.subheader('Tren Penggunaan Sepeda Berdasarkan Musim')
    
    # Menghitung rata-rata musiman
    season_counts = data.groupby('season')['cnt'].mean().reset_index()

    # Plotly line plot untuk tren musim
    line_fig = px.line(season_counts, x='season', y='cnt', 
                       labels={'season': 'Musim', 'cnt': 'Rata-rata Jumlah Peminjaman'},
                       title='Tren Penggunaan Sepeda Berdasarkan Musim',
                       markers=True)
    st.plotly_chart(line_fig)
    
    st.write("""
    **Legenda:** 1 : Musim semi   2 : Musim panas   3 : Musim gugur   4 : Musim dingin
             
    **Penjelasan:** Line plot ini menggambarkan tren rata-rata penggunaan sepeda berdasarkan musim. Puncak peminjaman sepeda terjadi di musim gugur. Sementara musim semi memiliki jumlah peminjaman sepeda yang paling rendah.
    """)

elif plot_option == "Tren Penggunaan Sepeda Berdasarkan Hari Kerja dan Akhir Pekan":
    st.subheader('Perbandingan Jumlah Peminjaman pada Hari Kerja dan Hari Libur')
    
    # Menghitung jumlah peminjaman per jenis hari
    day_type_counts = data.groupby('day_type')['cnt'].sum().reset_index()

    # Plotly bar chart untuk hari kerja vs libur
    bar_fig = px.bar(day_type_counts, x='day_type', y='cnt', 
                     labels={'day_type': 'Jenis Hari', 'cnt': 'Jumlah Peminjaman'},
                     title='Perbandingan Jumlah Peminjaman pada Hari Kerja dan Hari Libur',
                     color='day_type')
    st.plotly_chart(bar_fig)
    
    st.write("""
    **Penjelasan:** Bar chart ini menunjukkan bahwa jumlah peminjaman sepeda pada hari kerja lebih tinggi dibandingkan dengan peminjaman sepeda pada hari libur.
    """)

# Footer note
st.sidebar.write("Pilih plot yang ingin Anda lihat dari pilihan di atas.")
