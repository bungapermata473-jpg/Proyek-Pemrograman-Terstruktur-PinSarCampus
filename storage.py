import csv
import os

FILE_NAME = "Inventaris_pinsarcampus.csv"

def muat_data():
    """Membaca data inventaris dari file CSV."""
    daftar_inventaris = []
    if not os.path.exists(FILE_NAME):
        return daftar_inventaris
    
    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Konversi nilai status string ke boolean
            row["status"] = True if row["status"].lower() == "true" else False
            daftar_inventaris.append(row)
            
    return daftar_inventaris

def simpan_data(daftar_inventaris):
    """Menyimpan data inventaris ke file CSV."""
    fieldnames = ["id", "nama", "jenis", "status"]
    with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in daftar_inventaris:
            writer.writerow(item)