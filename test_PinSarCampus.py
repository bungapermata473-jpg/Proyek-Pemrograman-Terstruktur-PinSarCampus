import unittest
from service import cari_inventaris, validasi_input_barang

class TestPinSarCampus(unittest.TestCase):
    
    def setUp(self):
        # Data dummy untuk pengujian
        self.sample_data = [
            {"id": "INV001", "nama": "Proyektor Epson", "jenis": "Elektronik", "status": True},
            {"id": "INV002", "nama": "Kamera Canon", "jenis": "Elektronik", "status": True},
            {"id": "INV003", "nama": "Aula Utama", "jenis": "Ruangan", "status": True}
        ]

    def test_cari_inventaris_ditemukan(self):
        # Menguji pencarian barang yang ada
        hasil = cari_inventaris(self.sample_data, "Proyektor")
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["nama"], "Proyektor Epson")

    def test_cari_inventaris_tidak_ditemukan(self):
        # Menguji pencarian barang yang tidak ada
        hasil = cari_inventaris(self.sample_data, "Gitar")
        self.assertEqual(len(hasil), 0)

    def test_validasi_input_berhasil(self):
        # Menguji input valid (nama terisi dan jenis dipilih)
        valid, pesan = validasi_input_barang("Speaker Aktif", "Elektronik")
        self.assertTrue(valid)
        self.assertEqual(pesan, "Valid")

    def test_validasi_input_kosong(self):
        # Menguji validasi jika nama barang kosong
        valid, pesan = validasi_input_barang("", "Elektronik")
        self.assertFalse(valid)
        self.assertEqual(pesan, "Nama barang tidak boleh kosong!")

if __name__ == "__main__":
    unittest.main()