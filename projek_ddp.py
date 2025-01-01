import streamlit as st
import pandas as pd
from image import display_image

# Background
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('backgroundlistrik.png');
        background-size: cover;
        background-position: center center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.header('Pilihan menu')

# Sidebar content selection
option = st.sidebar.radio('opsi:', ('Menghitung total daya elektronik', 'Menghitung total biaya per kWh', 'Menghitung total biaya listrik per hari, bulan, dan tahun'))

if option == 'Menghitung total daya elektronik': # Konten 1
    st.header('🔋 Menghitung total daya elektronik')   
    barangelektronik = st.number_input(f'Silahkan masukkan nomor barang elektronik yang anda gunakan  1. Kulkas 2. Mesin Cuci 3. TV 4. Lampu 5. AC : ', min_value = 0)
    jampenggunaan = st.number_input("Berapa  lama anda menggunakan barang tersebut?")

    watt = 0
    namabarang = ""

    match barangelektronik :
        case 1 :
            watt = 150
            namabarang = "Kulkas"
        case 2 :
            watt = 200
            namabarang = "Mesin Cuci"
        case 3 :
            watt = 80
            namabarang = "TV"
        case 4 :
            watt = 60
            namabarang = "Lampu"
        case 5 :
            watt = 1000
            namabarang = "AC"

    total_watt = watt * jampenggunaan
    st.write(f"Total watt yang digunakan oleh {namabarang} adalah {total_watt} watt")

# Konten 2
if option == 'Menghitung total biaya per kWh': 
    st.header('⚡ Menghitung total biaya per kWh')

    def hitung_konsumsi_energi(daya_watt, waktu_jam):
        return (daya_watt / 1000) * waktu_jam

    def hitung_biaya(tarif_per_kWh, total_konsumsi):
        return tarif_per_kWh * total_konsumsi 

    # Input daya perangkat
    unit = st.selectbox('Pilih unit daya:', {'watt', 'Kilowatt'})
    daya_watt = st.number_input('Masukkan daya perangkat (watt):', min_value= 0)

    # Konversi unit ke kilowatt
    if unit == 'Kilowatt':
        daya_watt *= 1000

    # Input waktu penggunaan
    waktu_jam = st.number_input('Masukkan waktu penggunaan (jam):', min_value= 0)

    # Tarif Listrik
    tarif_per_kWh = st.number_input('Masukkan tarif listrik per kWh (rupiah):', min_value= 0)

    st.header('Hasil Perhitungan ✨')

    # Tombol untuk menghitung
    if st.button('Hitung Konsumsi Energi'):
        if daya_watt > 0 and waktu_jam > 0: 
            total_konsumsi = hitung_konsumsi_energi(daya_watt, waktu_jam)
            total_biaya = hitung_biaya(tarif_per_kWh, total_konsumsi)

            st.success(f'Konsumsi energi total: {total_konsumsi:.2f} kWh')
            st.write(f'Energi selama {waktu_jam} jam dengan daya {daya_watt} watt adalah {total_konsumsi:.2f} kWh')
            st.write(f'Total biaya untuk konsumsi energi ini adalah: {total_biaya:.2f} rupiah')

        else:
            st.error('Input valid dan lebih besar dari nol')

    # Display image
    st.image('kilometer_listrik.png')

    st.markdown('''
    ### Cara penggunaan:
    1. Pilih unit daya (watt atau kilowatt)
    2. Masukkan nilai daya perangkat 
    3. Masukkan waktu penggunaan dalam jam
    4. Klik tombol 'Hitung Konsumsi Energi' untuk melihat hasilnya'
    ''')

# Konten 3
elif option == 'Menghitung total biaya listrik per hari, bulan, dan tahun': 
    st.header('💡 Menghitung total biaya listrik per hari, bulan, dan tahun')
    #Table
    st.write('Tabel Harga Listrik PerkWh')
    df = pd.DataFrame({
        'GOLONGAN': ['R1', 'R1', 'R1', 'B1'],
        'DAYA LISTRIK': ['450 VA (Subsidi)', '900 VA', '1300+ VA', 'Bisnis'],
        'TARIF/HARGA LISTRIK PER KWH': ['Rp415/kWh', 'Rp1.352/kWh', 'Rp1.444,70/kWh', 'Rp1.114,74/kWh']
    })
    df.index = df.index + 1
    st.table(df)

    #Header
    st.header('Hasil Perhitungan ✨')

    class PerhitunganListrik:
        def __init__(self, daya_watt, waktu_perjam, unit_daya):
            self.daya_watt = daya_watt
            self.waktu_perjam = waktu_perjam
            self.unit_daya = unit_daya
            self.kwh = (self.daya_watt * self.waktu_perjam) / 1000
            self.tarif = self.pilih_tarif()

        #Menentukan jenis tarif
        def pilih_tarif(self):
            if self.unit_daya == '450 VA (subsidi)':
                return 415
            elif self.unit_daya == '900 VA':
                return 1352
            elif self.unit_daya == '1300+ VA':
                return 1444.70
            elif self.unit_daya == 'Bisnis':
                return 1114.74
            else :
                return 0
            
        #Menghitung pengeluaran listrik per jam, bulan dan tahun
        def hitung_total_biaya (self, periode):

            if periode == 'Per Hari':
                return self.kwh * self.tarif
            elif periode == 'Per Bulan':
                return self.kwh * self.tarif * 30 # Mengambil patokan 30 hari dalam 1 bulan
            elif periode == 'Per Tahun':
                return self.kwh * self.tarif * 360
            else:
                return 0

    # Input penggunaan waktu (perjam)
    waktu_perjam = st.number_input('Masukan penggunaan waktu/hari (jam):', min_value = 0, max_value=24)

    # Input daya perangkat dalam watt (w)
    daya_watt = st.number_input('Masukan daya perangkat (dalam watt):', min_value = 0)
    st.write(f'Total kWh: {(daya_watt * waktu_perjam)/1000} kWh')

    # Pilih jenis unit daya
    unit_daya = st.selectbox('Pilih jenis tarif/unit:', ['450 VA (subsidi)', '900 VA', '1300+ VA', 'Bisnis'])

    # Pilih periode perhitungan (per Hari, bulan, atau tahun)
    periode = st.selectbox('Pilih periode perhitungan:', ['Per Hari', 'Per Bulan', 'Per Tahun'])

    # Perhitungan biaya listrik
    if st.button('Hitung Jumlah Biaya'):
        if daya_watt > 0 and waktu_perjam > 0:
            listrik = PerhitunganListrik (daya_watt, waktu_perjam, unit_daya)
            biaya_total = listrik.hitung_total_biaya(periode) # Menghitung biaya berdasarkan periode
            st.write(f"Biaya listrik untuk jenis daya listrik {unit_daya} dengan daya {daya_watt} watt dan penggunaan {waktu_perjam} jam per hari adalah Rp {biaya_total:,.2f} ({periode})")
        else:
            st.write('Tidak Valid')

            