import mysql.connector

# =============== KONEKSI DATABASE ===============
def GetConnection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_vendingmachine',
        port=3306
    )

# =============== CREATE DATA ===============
def AddData():
    conn = GetConnection()
    cursor = conn.cursor()

    id = input("Masukkan ID: ")
    namaProduk = input("Masukkan Nama Produk: ")
    harga = input("Masukkan Harga Produk: ")

    query = "INSERT INTO products (id, namaProduk, harga) VALUES (%s, %s, %s)"
    data = (id, namaProduk, harga)

    cursor.execute(query, data)
    conn.commit()
    print("Data berhasil ditambahkan!\n")

    cursor.close()
    conn.close()

# =============== READ DATA ===============
def ReadData():
    conn = GetConnection()
    cursor = conn.cursor()

    query = "SELECT * FROM products"
    cursor.execute(query)

    result = cursor.fetchall()
    print("\n=== DATA PRODUK ===")
    for row in result:
        print(row)
    print("====================\n")

    cursor.close()
    conn.close()

# =============== UPDATE DATA ===============
def UpdateData():
    conn = GetConnection()
    cursor = conn.cursor()

    key = input("Masukkan ID Lama: ")
    idBaru = input("Masukkan ID Baru: ")
    namaBaru = input("Masukkan Nama Produk Baru: ")
    hargaBaru = input("Masukkan Harga Baru: ")

    query = """
        UPDATE products 
        SET id=%s, namaProduk=%s, harga=%s 
        WHERE id=%s
    """
    data = (idBaru, namaBaru, hargaBaru, key)

    cursor.execute(query, data)
    conn.commit()
    print("Data berhasil diperbarui!\n")

    cursor.close()
    conn.close()

# =============== DELETE DATA ===============
def DeleteData():
    conn = GetConnection()
    cursor = conn.cursor()

    key = input("Masukkan ID Produk yang ingin dihapus: ")

    query = "DELETE FROM products WHERE id=%s"
    data = (key,)

    cursor.execute(query, data)
    conn.commit()
    print("Data berhasil dihapus!\n")

    cursor.close()
    conn.close()

# ================== MENU ==================
while True:
    print("""
==== PROGRAM CRUD VENDING MACHINE ====
1. Tambah Data
2. Lihat Data
3. Update Data
4. Hapus Data
5. Keluar
""")
    pilih = input("Pilih menu: ")

    if pilih == "1":
        AddData()
    elif pilih == "2":
        ReadData()
    elif pilih == "3":
        UpdateData()
    elif pilih == "4":
        DeleteData()
    elif pilih == "5":
        print("Program selesai.")
        break
    else:
        print("Pilihan tidak valid!\n")
