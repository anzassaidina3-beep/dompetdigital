import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- KONFIGURASI ---
NAMA_FILE = "data_pengeluaran.json"
WARNA_BG = "#F0F2F5"
WARNA_HEADER = "#2C3E50"

# --- BACKEND (LOGIKA) ---
def muat_data():
    if os.path.exists(NAMA_FILE):
        try:
            with open(NAMA_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

def simpan_data(data):
    with open(NAMA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def aksi_tambah():
    deskripsi = entry_deskripsi.get()
    nominal_str = entry_nominal.get()
    kategori = combo_kategori.get()

    if not deskripsi or not nominal_str or not kategori:
        messagebox.showwarning("Peringatan", "Semua kolom wajib diisi!")
        return

    try:
        nominal = int(nominal_str)
    except ValueError:
        messagebox.showerror("Error", "Nominal harus berupa angka!")
        return

    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    item_baru = {
        "tanggal": tanggal,
        "kategori": kategori,
        "deskripsi": deskripsi,
        "nominal": nominal
    }

    data = muat_data()
    data.append(item_baru)
    simpan_data(data)

    entry_deskripsi.delete(0, tk.END)
    entry_nominal.delete(0, tk.END)
    
    tampilkan_data()
    update_grafik() # Update grafik setelah tambah data
    messagebox.showinfo("Sukses", "Data berhasil disimpan!")

def aksi_hapus():
    selected = tabel.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus!")
        return

    if messagebox.askyesno("Hapus Data", "Yakin ingin menghapus data ini?"):
        index = tabel.index(selected[0])
        data = muat_data()
        del data[index]
        simpan_data(data)
        tampilkan_data()
        update_grafik() # Update grafik setelah hapus data
        messagebox.showinfo("Terhapus", "Data berhasil dihapus.")

def tampilkan_data():
    for row in tabel.get_children():
        tabel.delete(row)

    data = muat_data()
    total = 0

    for item in data:
        kategori = item.get('kategori', 'Umum')
        tabel.insert("", tk.END, values=(item['tanggal'], kategori, item['deskripsi'], format_rupiah(item['nominal'])))
        total += item['nominal']
    
    label_total.config(text=f"Total Pengeluaran: {format_rupiah(total)}")

def update_grafik():
    """Fungsi untuk membuat Pie Chart berdasarkan Kategori"""
    data = muat_data()
    if not data:
        return

    # Hitung total per kategori
    kategori_total = {}
    for item in data:
        kat = item.get('kategori', 'Lainnya')
        nom = item['nominal']
        kategori_total[kat] = kategori_total.get(kat, 0) + nom

    # Siapkan data untuk chart
    labels = list(kategori_total.keys())
    values = list(kategori_total.values())

    # Bersihkan grafik lama
    figure.clear()
    
    # Buat Pie Chart baru
    ax = figure.add_subplot(111)
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    ax.set_title("Persentase Pengeluaran")

    # Refresh canvas
    canvas.draw()

# --- FRONTEND (GUI) ---
root = tk.Tk()
root.title("Dompet Digital V3.0 - Dengan Analisis")
root.geometry("1000x600")
root.configure(bg=WARNA_BG)

# Header
tk.Label(root, text="DOMPET DIGITAL PINTAR", bg=WARNA_HEADER, fg="white", font=("Segoe UI", 16, "bold"), pady=10).pack(fill="x")

# Tab System (Notebook)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# --- TAB 1: INPUT & DATA ---
tab1 = tk.Frame(notebook, bg=WARNA_BG)
notebook.add(tab1, text="📝 Input & Data")

# Frame Kiri (Input) - Tab 1
frame_input = tk.Frame(tab1, bg="white", padx=20, pady=20)
frame_input.pack(side="left", fill="y", padx=10, pady=10)

tk.Label(frame_input, text="Kategori", bg="white").pack(anchor="w")
combo_kategori = ttk.Combobox(frame_input, values=["Makan", "Transport", "Belanja", "Tagihan", "Hiburan"], state="readonly")
combo_kategori.current(0)
combo_kategori.pack(fill="x", pady=(0, 10))

tk.Label(frame_input, text="Deskripsi", bg="white").pack(anchor="w")
entry_deskripsi = tk.Entry(frame_input)
entry_deskripsi.pack(fill="x", pady=(0, 10))

tk.Label(frame_input, text="Nominal (Rp)", bg="white").pack(anchor="w")
entry_nominal = tk.Entry(frame_input)
entry_nominal.pack(fill="x", pady=(0, 20))

tk.Button(frame_input, text="SIMPAN", bg="#27AE60", fg="white", command=aksi_tambah).pack(fill="x", pady=5)
tk.Button(frame_input, text="HAPUS", bg="#E74C3C", fg="white", command=aksi_hapus).pack(fill="x")

# Frame Kanan (Tabel) - Tab 1
frame_tabel = tk.Frame(tab1)
frame_tabel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

columns = ("Tanggal", "Kategori", "Deskripsi", "Nominal")
tabel = ttk.Treeview(frame_tabel, columns=columns, show="headings")
for col in columns: tabel.heading(col, text=col)
tabel.column("Tanggal", width=120); tabel.column("Nominal", anchor="e")
tabel.pack(fill="both", expand=True)

label_total = tk.Label(frame_tabel, text="Total: Rp 0", font=("Arial", 12, "bold"), pady=10)
label_total.pack(anchor="e")

# --- TAB 2: LAPORAN GRAFIK ---
tab2 = tk.Frame(notebook, bg="white")
notebook.add(tab2, text="📊 Analisis Grafik")

# Area Grafik Matplotlib
figure = plt.Figure(figsize=(6, 5), dpi=100)
canvas = FigureCanvasTkAgg(figure, tab2)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

# Jalankan
tampilkan_data()
update_grafik()
root.mainloop()