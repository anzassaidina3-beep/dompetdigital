import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# --- KONFIGURASI WARNA & FILE ---
NAMA_FILE = "data_pengeluaran.json"
WARNA_BG = "#F0F2F5"       # Abu-abu muda untuk background
WARNA_HEADER = "#2C3E50"   # Biru tua elegan
WARNA_TOMBOL = "#27AE60"   # Hijau segar
WARNA_HAPUS = "#E74C3C"    # Merah
FONT_UTAMA = ("Segoe UI", 10)
FONT_HEADER = ("Segoe UI", 12, "bold")

# --- BAGIAN LOGIKA (BACKEND) ---
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

    # Reset Input
    entry_deskripsi.delete(0, tk.END)
    entry_nominal.delete(0, tk.END)
    combo_kategori.current(0) # Reset ke pilihan pertama
    
    tampilkan_data()
    messagebox.showinfo("Sukses", "Data berhasil disimpan!")

def aksi_hapus():
    selected = tabel.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus!")
        return

    konfirmasi = messagebox.askyesno("Hapus Data", "Yakin ingin menghapus data ini?")
    if konfirmasi:
        # Ambil index data yang dipilih
        index = tabel.index(selected[0])
        data = muat_data()
        
        # Hapus data berdasarkan index
        del data[index]
        simpan_data(data)
        tampilkan_data()
        messagebox.showinfo("Terhapus", "Data berhasil dihapus.")

def tampilkan_data():
    # Bersihkan tabel lama
    for row in tabel.get_children():
        tabel.delete(row)

    data = muat_data()
    total = 0

    for item in data:
        # Penanganan jika data lama tidak punya kategori (opsional)
        kategori = item.get('kategori', 'Umum') 
        
        tabel.insert("", tk.END, values=(
            item['tanggal'], 
            kategori,
            item['deskripsi'], 
            format_rupiah(item['nominal'])
        ))
        total += item['nominal']
    
    label_total.config(text=f"Total Pengeluaran: {format_rupiah(total)}")

# --- BAGIAN TAMPILAN (FRONTEND - GUI) ---
root = tk.Tk()
root.title("Dompet Digital V2.0")
root.geometry("900x550")
root.configure(bg=WARNA_BG)

# 1. Header Judul
frame_header = tk.Frame(root, bg=WARNA_HEADER, pady=15)
frame_header.pack(fill="x")
tk.Label(frame_header, text="PENCATAT KEUANGAN PRIBADI", bg=WARNA_HEADER, fg="white", font=("Segoe UI", 16, "bold")).pack()

# 2. Container Utama (Membagi layar jadi Kiri dan Kanan)
main_frame = tk.Frame(root, bg=WARNA_BG, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# --- BAGIAN KIRI (INPUT FORM) ---
frame_kiri = tk.Frame(main_frame, bg="white", padx=20, pady=20, relief=tk.RIDGE, bd=1)
frame_kiri.pack(side="left", fill="y", padx=(0, 20))

tk.Label(frame_kiri, text="Input Pengeluaran", font=FONT_HEADER, bg="white", fg="#333").pack(anchor="w", pady=(0, 15))

# Input Kategori
tk.Label(frame_kiri, text="Kategori:", bg="white", font=FONT_UTAMA).pack(anchor="w")
combo_kategori = ttk.Combobox(frame_kiri, values=["Makan & Minum", "Transportasi", "Belanja", "Tagihan", "Hiburan", "Lain-lain"], font=FONT_UTAMA, state="readonly")
combo_kategori.current(0)
combo_kategori.pack(fill="x", pady=(5, 15))

# Input Deskripsi
tk.Label(frame_kiri, text="Keterangan:", bg="white", font=FONT_UTAMA).pack(anchor="w")
entry_deskripsi = tk.Entry(frame_kiri, font=FONT_UTAMA, bd=2, relief="groove")
entry_deskripsi.pack(fill="x", pady=(5, 15))

# Input Nominal
tk.Label(frame_kiri, text="Nominal (Rp):", bg="white", font=FONT_UTAMA).pack(anchor="w")
entry_nominal = tk.Entry(frame_kiri, font=FONT_UTAMA, bd=2, relief="groove")
entry_nominal.pack(fill="x", pady=(5, 20))

# Tombol Action
btn_simpan = tk.Button(frame_kiri, text="💾 SIMPAN", bg=WARNA_TOMBOL, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=aksi_tambah, pady=8)
btn_simpan.pack(fill="x", pady=5)

btn_hapus = tk.Button(frame_kiri, text="🗑️ HAPUS DATA", bg=WARNA_HAPUS, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=aksi_hapus, pady=8)
btn_hapus.pack(fill="x", pady=5)

# --- BAGIAN KANAN (TABEL DATA) ---
frame_kanan = tk.Frame(main_frame, bg=WARNA_BG)
frame_kanan.pack(side="right", fill="both", expand=True)

# Styling Tabel (Treeview)
style = ttk.Style()
style.theme_use("clam") # Tema bawaan yang lebih bersih
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#DDD", foreground="#333")
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

# Definisi Kolom
columns = ("Tanggal", "Kategori", "Deskripsi", "Nominal")
tabel = ttk.Treeview(frame_kanan, columns=columns, show="headings", selectmode="browse")

tabel.heading("Tanggal", text="Tanggal")
tabel.heading("Kategori", text="Kategori")
tabel.heading("Deskripsi", text="Keterangan")
tabel.heading("Nominal", text="Jumlah (Rp)")

tabel.column("Tanggal", width=120, anchor="center")
tabel.column("Kategori", width=100, anchor="center")
tabel.column("Deskripsi", width=200, anchor="w")
tabel.column("Nominal", width=120, anchor="e")

# Scrollbar untuk tabel
scrollbar = ttk.Scrollbar(frame_kanan, orient="vertical", command=tabel.yview)
tabel.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tabel.pack(fill="both", expand=True)

# Total Panel
frame_total = tk.Frame(frame_kanan, bg="#34495E", pady=10, padx=10)
frame_total.pack(fill="x", pady=(10, 0))
label_total = tk.Label(frame_total, text="Total Pengeluaran: Rp 0", font=("Segoe UI", 14, "bold"), bg="#34495E", fg="#F1C40F")
label_total.pack(anchor="e")

# Jalankan App
tampilkan_data()
root.mainloop()