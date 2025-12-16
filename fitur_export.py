import csv
from tkinter import filedialog, messagebox

def simpan_ke_csv(data):
    """
    Fungsi ini menerima data (list), lalu menyimpannya ke file CSV.
    """
    if not data:
        messagebox.showwarning("Kosong", "Tidak ada data untuk di-export.")
        return

    # Minta user memilih lokasi simpan
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV File (Excel)", "*.csv"), ("All Files", "*.*")],
        title="Simpan Laporan Keuangan"
    )

    if file_path:
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Tulis Header
                writer.writerow(["Tanggal", "Kategori", "Deskripsi", "Nominal"])
                
                # Tulis Data
                for item in data:
                    writer.writerow([
                        item['tanggal'], 
                        item.get('kategori', 'Umum'), 
                        item['deskripsi'], 
                        item['nominal']
                    ])
            
            messagebox.showinfo("Sukses", f"Laporan berhasil disimpan di:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan file: {e}")