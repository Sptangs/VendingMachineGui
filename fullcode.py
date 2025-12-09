import tkinter as tk
from tkinter import messagebox, ttk, mainloop
from PIL import Image, ImageTk
import mysql.connector
import os

# ===================== WARNA UI =====================
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'warning': '#f39c12',
    'success': '#27ae60',
    'danger': '#e74c3c',
    'accent': '#e74c3c',
    'background': '#f5f5f5',
    'light': '#ecf0f1'
}

# =============== KONEKSI DATABASE ===============
def GetConnection():
    return mysql.connector.connect(
        host='localhost',
        database='db_vendingmachine',
        user='root',
        password='',
        port=3306
    )

root = tk.Tk()
root.title("Aplikasi Vending Machine")
root.geometry("900x600")
root.configure(bg=COLORS['background'])
root.resizable(0, 0)

# Variabel untuk input
root.mode = ""
root.temp = ""

# =============================
#  FUNGSI POPUP
# =============================
def show_popup(pesan, title="Informasi"):
    pop = tk.Toplevel()
    pop.title(title)
    pop.geometry("300x180")
    pop.configure(bg="white")
    pop.resizable(0,0)

    tk.Label(pop, text=title, font=("Arial", 14, "bold"), bg="white").pack(pady=5)
    tk.Label(pop, text=pesan, font=("Arial", 12), bg="white").pack(pady=5)

    tk.Button(pop, text="OK", bg="#4CAF50", fg="white",
              font=("Arial", 12), command=pop.destroy).pack(pady=(5, 10))


# =============================
#  TAMPILKAN VENDING MACHINE
# =============================
def show_vending_machine():

    root.update_idletasks()

    # =============================
    #  FRAME UTAMA
    # =============================
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)

    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=1)

    # =============================
    #  TITLE
    # =============================
    title_frame = tk.Frame(main_frame, bg="white")
    title_frame.grid(row=0, column=0, columnspan=2, pady=2)

    tk.Label(title_frame, text="VENDING MACHINE",
             font=("Arial", 15, "bold"), bg="white").pack()

    tk.Label(title_frame, text="Selamat Datang!",
             font=("Arial", 10), bg="white", fg="#555").pack()

    # =============================
    #  DISPLAY PRODUK KIRI
    # =============================
    display = tk.Frame(main_frame, bg="#333", bd=8, relief="ridge")
    display.grid(row=1, column=0, sticky="nsew", padx=(10, 2), pady=(10, 5))

    # =============================
    #  AREA KANAN (CANVAS + TOMBOL)
    # =============================
    right_area = tk.Frame(main_frame, bg="#eeeeee")
    right_area.grid(row=1, column=1, sticky="nsew", padx=(2, 10), pady=(10, 5))
    right_area.grid_rowconfigure(1, weight=0)

    # Canvas mesin (kiri atas di area kanan)
    # =============================
    #  FRAME TOMBOL (SEBELAH KANAN ATAS)
    # =============================
    control_frame = tk.Frame(right_area, bg="#ddd")
    control_frame.grid(row=0, column=0, sticky="ne", padx=5, pady=5)

    # ENTRY UTAMA
    entry = tk.Entry(control_frame, font=("Arial", 14), width=28, justify="center")
    entry.grid(row=0, column=0, columnspan=2, pady=2)

    # INPUT KOIN
    coin_label = tk.Label(control_frame, text="Koin:", font=("Arial", 10), bg="#ddd")
    coin_label.grid(row=1, column=0, sticky="e")
    coin_entry = tk.Entry(control_frame, width=30)
    coin_entry.grid(row=1, column=1)

    # INPUT ID
    id_label = tk.Label(control_frame, text="ID Produk:", font=("Arial", 10), bg="#ddd")
    id_label.grid(row=2, column=0, sticky="e")
    id_entry = tk.Entry(control_frame, width=30)
    id_entry.grid(row=2, column=1)

    # =============================
    #  TOMBOL MODE INPUT
    # =============================
    def set_koin():
        root.mode = "koin"
        root.temp = ""
        entry.delete(0, tk.END)

    def set_id():
        root.mode = "id"
        root.temp = ""
        entry.delete(0, tk.END)

    tk.Button(control_frame, text="INPUT KOIN", bg="orange",
              width=10, command=set_koin).grid(row=3, column=0, pady=5)

    tk.Button(control_frame, text="INPUT ID", bg="lightblue",
              width=10, command=set_id).grid(row=3, column=1, pady=5)

    # =============================
    #  KEYPAD (DI KANAN BAWAH)
    # =============================
    keypad_frame = tk.Frame(right_area, bg="#eeeeee")
    keypad_frame.grid(row=1, column=0, pady=10)

    tombol = ["1", "2", "3", "C",
              "4", "5", "6", "0",
              "7", "8", "9", "OK"]

    def press(t):
        root.temp += t
        entry.delete(0, tk.END)
        entry.insert(0, root.temp)

    def clear():
        root.temp = ""
        entry.delete(0, tk.END)

    def ok():
        if root.mode == "koin":
            coin_entry.delete(0, tk.END)
            coin_entry.insert(0, root.temp)
        else:
            id_entry.delete(0, tk.END)
            id_entry.insert(0, root.temp)

        root.temp = ""
        entry.delete(0, tk.END)

    r, c = 0, 0
    for t in tombol:
        bg = "#4CAF50" if t == "OK" else "#ff6b6b" if t == "C" else "white"
        b = tk.Button(keypad_frame, text=t, width=6, height=2,
                      font=("Arial", 12, "bold"), bg=bg)
        b.grid(row=r, column=c, padx=5, pady=5)

        if t == "C":
            b.config(command=clear)
        elif t == "OK":
            b.config(command=ok)
        else:
            b.config(command=lambda v=t: press(v))

        c += 1
        if c > 3:
            c = 0
            r += 1

    # =============================
    #  FUNGSI BELI PRODUK
    # =============================
    def beli():
        try:
            coin = int(coin_entry.get())
            pid = int(id_entry.get())

            conn = GetConnection()
            cur = conn.cursor()
            cur.execute("SELECT namaProduk, harga FROM products WHERE id=%s", (pid,))
            row = cur.fetchone()

            conn.close()
            coin_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)

            if not row:
                show_popup("\n❌ Produk tidak ditemukan!\n")
                return

            nama, harga = row
            if coin < harga:
                show_popup(f"\n⚠ Uang kurang {harga - coin}\n")
            else:
                show_popup(f"\n✅ Berhasil beli {nama}\nKembalian: {coin - harga}\n")

        except:
            show_popup("\nInput salah!\n")

    tk.Button(right_area, text="BELI PRODUK", bg="green", fg="white",
              width=20, command=beli).grid(row=2, column=0, pady=5)

    # =============================
    #  FUNGSI DISPLAY PRODUK
    # =============================
    def tampilkan_produk():
        conn = GetConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT namaproduk, harga, gambar FROM products")
        hasil = cursor.fetchall()

        for widget in display.winfo_children():
            widget.destroy()

        total_kolom = 4
        for i in range(total_kolom):
            display.grid_columnconfigure(i, weight=1, uniform="col")

        row, col = 0, 0

        for nama, harga, gambar in hasil:

            if not gambar or not os.path.exists(gambar):
                gambar = "img/default.png"

            img = Image.open(gambar)
            img = img.resize((50, 50))
            img_tk = ImageTk.PhotoImage(img)

            card = tk.Frame(display, bg="#3a3a3a", bd=2, relief="solid")
            card.grid(row=row, column=col, padx=5, pady=5, sticky="n")

            tk.Label(card, image=img_tk, bg="white").pack()
            tk.Label(card, text=nama, fg="white", bg="#3a3a3a",
                     font=("Arial", 8)).pack()
            tk.Label(card, text=f"Rp {harga}", fg="#ffdd33", bg="#3a3a3a",
                     font=("Arial", 8, "bold")).pack()

            card.image = img_tk

            col += 1
            if col == total_kolom:
                col = 0
                row += 1

        conn.close()

    tampilkan_produk()

show_vending_machine()
root.mainloop()
