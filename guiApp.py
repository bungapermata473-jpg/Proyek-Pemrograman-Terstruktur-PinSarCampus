import tkinter as tk
from tkinter import ttk, messagebox
from storage import muat_data, simpan_data
from service import cari_inventaris, validasi_input_barang

class PinSarCampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PinSarCampus - Sistem Peminjaman Sarana Kampus")
        self.root.geometry("750x500")
        self.root.config(bg="#f4f6f9")

        # Load data dari CSV atau gunakan data default jika kosong
        self.daftar_inventaris = muat_data()
        if not self.daftar_inventaris:
            self.daftar_inventaris = [
                {"id": "INV001", "nama": "Proyektor Epson", "jenis": "Elektronik", "status": True},
                {"id": "INV002", "nama": "Kamera Canon", "jenis": "Elektronik", "status": True},
                {"id": "INV003", "nama": "Aula Utama", "jenis": "Ruangan", "status": True}
            ]
            simpan_data(self.daftar_inventaris)

        self.setup_ui()

    def setup_ui(self):
        # Judul
        lbl_title = tk.Label(self.root, text="SISTEM PEMINJAMAN SARANA KAMPUS (PINSARCAMPUS)", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#333")
        lbl_title.pack(pady=10)

        # Frame Pencarian
        frame_top = tk.Frame(self.root, bg="#f4f6f9")
        frame_top.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_top, text="Cari Barang:", bg="#f4f6f9", font=("Arial", 10)).pack(side="left", padx=5)
        self.ent_cari = tk.Entry(frame_top, font=("Arial", 10), width=25)
        self.ent_cari.pack(side="left", padx=5)

        btn_cari = tk.Button(frame_top, text="Cari", bg="#007bff", fg="white", font=("Arial", 9, "bold"), command=self.aksi_cari)
        btn_cari.pack(side="left", padx=5)

        btn_reset = tk.Button(frame_top, text="Reset", bg="#6c757d", fg="white", font=("Arial", 9, "bold"), command=self.refresh_tabel)
        btn_reset.pack(side="left", padx=5)

        # Frame Tabel
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=5, padx=10, fill="both", expand=True)

        columns = ("ID", "Nama Barang", "Jenis", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.muat_tabel_data(self.daftar_inventaris)

        # Frame Form Input
        form_frame = tk.LabelFrame(self.root, text=" Form Input Inventaris Baru ", font=("Arial", 10, "bold"), bg="#f4f6f9", padx=10, pady=10)
        form_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(form_frame, text="Nama Barang:", bg="#f4f6f9", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_nama = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.ent_nama.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Jenis Sarana:", bg="#f4f6f9", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.cb_jenis = ttk.Combobox(form_frame, values=["Elektronik", "Ruangan"], font=("Arial", 10), width=23, state="readonly")
        self.cb_jenis.grid(row=1, column=1, padx=10, pady=5)
        self.cb_jenis.set("Elektronik")

        # Tombol Aksi Bawah
        btn_frame = tk.Frame(form_frame, bg="#f4f6f9")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        btn_tambah = tk.Button(btn_frame, text="Tambah Data", bg="#28a745", fg="white", font=("Arial", 9, "bold"), padx=10, command=self.aksi_tambah)
        btn_tambah.pack(side="left", padx=5)

        btn_hapus = tk.Button(btn_frame, text="Hapus Terpilih", bg="#dc3545", fg="white", font=("Arial", 9, "bold"), padx=10, command=self.aksi_hapus)
        btn_hapus.pack(side="left", padx=5)

    def muat_tabel_data(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in data:
            status_str = "Tersedia" if item["status"] else "Dipinjam"
            self.tree.insert("", "end", values=(item["id"], item["nama"], item["jenis"], status_str))

    def aksi_tambah(self):
        nama = self.ent_nama.get()
        jenis = self.cb_jenis.get()

        valid, pesan = validasi_input_barang(nama, jenis)
        if not valid:
            messagebox.showwarning("Peringatan", pesan)
            return

        id_baru = f"INV0{len(self.daftar_inventaris) + 1}"
        item_baru = {"id": id_baru, "nama": nama.strip(), "jenis": jenis, "status": True}
        
        self.daftar_inventaris.append(item_baru)
        simpan_data(self.daftar_inventaris)
        self.muat_tabel_data(self.daftar_inventaris)
        
        self.ent_nama.delete(0, tk.END)
        messagebox.showinfo("Sukses", "Data inventaris berhasil ditambahkan!")

    def aksi_hapus(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih baris pada tabel yang ingin dihapus!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            for item_id in selected_item:
                values = self.tree.item(item_id, "values")
                target_id = values[0]
                self.daftar_inventaris = [x for x in self.daftar_inventaris if x["id"] != target_id]

            simpan_data(self.daftar_inventaris)
            self.muat_tabel_data(self.daftar_inventaris)
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")

    def aksi_cari(self):
        keyword = self.ent_cari.get()
        hasil = cari_inventaris(self.daftar_inventaris, keyword)
        self.muat_tabel_data(hasil)

    def refresh_tabel(self):
        self.ent_cari.delete(0, tk.END)
        self.muat_tabel_data(self.daftar_inventaris)

if __name__ == "__main__":
    root = tk.Tk()
    app = PinSarCampusApp(root)
    root.mainloop()