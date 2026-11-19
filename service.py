def cari_inventaris(daftar_inventaris, keyword):
    """Mencari barang berdasarkan nama atau ID."""
    keyword = keyword.lower()
    hasil = [
        item for item in daftar_inventaris 
        if keyword in item["nama"].lower() or keyword in item["id"].lower()
    ]
    return hasil

def urutkan_inventaris(daftar_inventaris, berdasarkan="nama"):
    """Mengurutkan data inventaris secara ascending."""
    return sorted(daftar_inventaris, key=lambda x: x[berdasarkan].lower())

def validasi_input_barang(nama, jenis):
    """Validasi form input agar tidak kosong."""
    if not nama or not nama.strip():
        return False, "Nama barang tidak boleh kosong!"
    if not jenis:
        return False, "Jenis sarana harus dipilih!"
    return True, "Valid"