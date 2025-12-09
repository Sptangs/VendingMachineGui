import tkinter as tk
from tkinter import messagebox, ttk
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

# =========================================================
# JENDELA UTAMA
# =========================================================
root = tk.Tk()
root.title("Aplikasi Vending Machine")
root.geometry("900x600")
root.configure(bg=COLORS['background'])
root.resizable(0, 0)

data_frame = None
root.mode = ""
root.temp = ""

# =========================================================
# CLEAR FUNCTION
# =========================================================
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def clear_data_frame():
    global data_frame
    if data_frame is not None:
        data_frame.destroy()
        data_frame = None

# =========================================================
# POPUP
# =========================================================
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

# =========================================================
# PANEL ADMIN
# =========================================================
def show_admin_panel():
    clear_window()
    global data_frame

    header = tk.Label(root, text="PANEL ADMIN",
                      bg=COLORS['background'], font=("Arial", 20, "bold"))
    header.pack(pady=20)

    menu_frame = tk.Frame(root, bg=COLORS['background'])
    menu_frame.pack(pady=20)

    btn_style = {'font': ("Arial", 12, "bold"),
                 'width': 15, 'pady': 10, 'cursor': "hand2"}

    tk.Button(menu_frame, text="Tambah Produk", bg='#28a745', fg='white',
              command=add_product, **btn_style).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(menu_frame, text="Lihat Produk", bg='#17a2b8', fg='white',
              command=view_products, **btn_style).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(menu_frame, text="Update Produk", bg='#ffc107', fg='white',
              command=update_product, **btn_style).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(menu_frame, text="Hapus Produk", bg='#dc3545', fg='white',
              command=delete_product, **btn_style).grid(row=1, column=1, padx=10, pady=10)

    data_frame = tk.Frame(root, bg='white')
    data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# =========================================================
# LOGIN ADMIN
# =========================================================
def admin_login():
    login = tk.Toplevel(root)
    login.title("Login Admin")
    login.geometry("350x300")
    login.configure(bg=COLORS['background'])
    login.resizable(False, False)

    login.transient(root)
    login.grab_set()

    tk.Label(login, text="LOGIN ADMIN",
             font=("Arial", 16, "bold"),
             bg=COLORS['background']).pack(pady=20)

    tk.Label(login, text="Username:", bg=COLORS['background']).pack()
    user = tk.Entry(login, width=25)
    user.insert(0, "admin")
    user.pack(pady=5)

    tk.Label(login, text="Password:", bg=COLORS['background']).pack()
    pwd = tk.Entry(login, width=25, show="*")
    pwd.insert(0, "admin123")
    pwd.pack(pady=5)

    def check():
        if user.get() == "admin" and pwd.get() == "admin123":
            login.destroy()
            show_admin_panel()
        else:
            messagebox.showerror("Gagal", "Username / Password salah!")

    tk.Button(login, text="Login", bg=COLORS['success'],
              fg='white', width=12, command=check).pack(pady=20)

# =========================================================
# CRUD PRODUK
# =========================================================

def add_product():
    clear_data_frame()
    global data_frame

    data_frame = tk.Frame(root, bg='white')
    data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(data_frame, text="Tambah Produk", bg='white',
             font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(data_frame, text="Nama:", bg='white').pack()
    name_entry = tk.Entry(data_frame, width=30)
    name_entry.pack()

    tk.Label(data_frame, text="Harga:", bg='white').pack()
    price_entry = tk.Entry(data_frame, width=30)
    price_entry.pack()

    def save():
        nama = name_entry.get()
        harga = price_entry.get()

        try:
            conn = GetConnection()
            cur = conn.cursor()
            cur.execute("INSERT INTO products (namaproduk, harga) VALUES (%s,%s)",
                        (nama, harga))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Sukses", "Produk ditambahkan!")
            add_product()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(data_frame, text="Simpan", bg=COLORS['success'],
              fg='white', width=15, command=save).pack(pady=10)

def view_products():
    clear_data_frame()
    global data_frame

    data_frame = tk.Frame(root, bg='white')
    data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    cols = ("ID", "Nama Produk", "Harga")
    table = ttk.Treeview(data_frame, columns=cols, show="headings")
    table.pack(fill=tk.BOTH, expand=True)

    for col in cols:
        table.heading(col, text=col)

    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute("SELECT id, namaproduk, harga FROM products")
        for row in cur.fetchall():
            table.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_product():
    clear_data_frame()
    global data_frame

    data_frame = tk.Frame(root, bg='white')
    data_frame.pack(expand=True, padx=20, pady=20)

    tk.Label(data_frame, text="Update Produk", bg='white',
             font=("Arial", 14, "bold")).pack(pady=10)

    form = tk.Frame(data_frame, bg="white")
    form.pack(padx=20, expand=True)

    tk.Label(form, text="ID Lama:", bg="white").grid(row=0, column=0)
    id_lama = tk.Entry(form)
    id_lama.grid(row=0, column=1, pady=5)

    tk.Label(form, text="ID Baru:", bg="white").grid(row=1, column=0)
    id_baru = tk.Entry(form)
    id_baru.grid(row=1, column=1, pady=5)

    tk.Label(form, text="Nama Baru:", bg="white").grid(row=2, column=0)
    nama_baru = tk.Entry(form)
    nama_baru.grid(row=2, column=1, pady=5)

    tk.Label(form, text="Harga Baru:", bg="white").grid(row=3, column=0)
    harga_baru = tk.Entry(form)
    harga_baru.grid(row=3, column=1, pady=5)

    def submit_update():
        old = id_lama.get()
        new_id = id_baru.get()
        new_nama = nama_baru.get()
        new_harga = harga_baru.get()

        if not old or not new_id or not new_nama or not new_harga:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")
            return

        try:
            conn = GetConnection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products SET id=%s, namaproduk=%s, harga=%s WHERE id=%s
            """, (new_id, new_nama, new_harga, old))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Produk berhasil diperbarui!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(data_frame, text="UPDATE", bg="yellow",
              font=("Arial", 10, "bold"), command=submit_update).pack(fill=tk.X, pady=10)

def delete_product():
    clear_data_frame()
    global data_frame

    data_frame = tk.Frame(root, bg="white")
    data_frame.pack(expand=True, padx=20, pady=20)

    tk.Label(data_frame, text="HAPUS PRODUK", font=("Arial", 14, "bold"),
             bg="white").pack(pady=10)

    tk.Label(data_frame, text="ID Produk:", bg="white").pack()
    id_entry = tk.Entry(data_frame)
    id_entry.pack(pady=5)

    def submit_delete():
        val = id_entry.get()
        if not val:
            messagebox.showwarning("Input Error", "ID harus diisi!")
            return

        if messagebox.askyesno("Konfirmasi", f"Hapus produk ID {val}?"):
            try:
                conn = GetConnection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id=%s", (val,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Produk berhasil dihapus!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    tk.Button(data_frame, text="HAPUS", bg="red", fg="white",
              font=("Arial", 10, "bold"), command=submit_delete).pack(fill=tk.X, pady=10)

# =========================================================
# TAMPILKAN MESIN
# =========================================================
def show_vending_machine():
    clear_window()
    root.update_idletasks()

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)

    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=1)

    # JUDUL
    title_frame = tk.Frame(main_frame, bg="white")
    title_frame.grid(row=0, column=0, columnspan=2)

    tk.Label(title_frame, text="VENDING MACHINE",
             font=("Arial", 15, "bold"), bg="white").pack()

    # DISPLAY PRODUK (kiri)
    display = tk.Frame(main_frame, bg="#333", bd=8, relief="ridge")
    display.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # AREA KANAN
    right_area = tk.Frame(main_frame, bg="#eee")
    right_area.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # FRAME TOMBOL KANAN ATAS
    control_frame = tk.Frame(right_area, bg="#ddd")
    control_frame.grid(row=0, column=0, sticky="n", pady=10)

    entry = tk.Entry(control_frame, font=("Arial", 14), width=28, justify="center")
    entry.grid(row=0, column=0, columnspan=2, pady=3)

    coin_entry = tk.Entry(control_frame, width=30)
    id_entry = tk.Entry(control_frame, width=30)

    tk.Label(control_frame, text="Koin:", bg="#ddd").grid(row=1, column=0)
    coin_entry.grid(row=1, column=1)

    tk.Label(control_frame, text="ID Produk:", bg="#ddd").grid(row=2, column=0)
    id_entry.grid(row=2, column=1)

    # MODE KOIN/ID
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

    # KEYPAD
    keypad_frame = tk.Frame(right_area, bg="#eee")
    keypad_frame.grid(row=1, column=0)

    tombol = ["1","2","3","C",
              "4","5","6","0",
              "7","8","9","OK"]

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

    r = c = 0
    for t in tombol:
        bg = "#4CAF50" if t == "OK" else "#ff6b6b" if t == "C" else "white"
        b = tk.Button(keypad_frame, text=t, width=6, height=2,
                      font=("Arial", 12, "bold"), bg=bg)

        if t == "C":
            b.config(command=clear)
        elif t == "OK":
            b.config(command=ok)
        else:
            b.config(command=lambda v=t: press(v))

        b.grid(row=r, column=c, padx=5, pady=5)

        c += 1
        if c > 3:
            c = 0
            r += 1

    # BELI
    def beli():
        try:
            coin = int(coin_entry.get())
            pid = int(id_entry.get())

            conn = GetConnection()
            cur = conn.cursor()
            cur.execute("SELECT namaProduk, harga FROM products WHERE id=%s", (pid,))
            row = cur.fetchone()
            conn.close()

            if not row:
                show_popup("❌ Produk tidak ditemukan!")
                return

            nama, harga = row

            if coin < harga:
                show_popup(f"⚠ Uang kurang {harga - coin}")
            else:
                show_popup(f"Berhasil beli {nama}\nKembalian: {coin - harga}")

            coin_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)

        except:
            show_popup("Input salah!")

    tk.Button(right_area, text="BELI PRODUK", bg="green", fg="white",
              width=20, command=beli).grid(row=2, column=0, pady=10)

    # ADMIN BUTTON (TIDAK auto-run)
    tk.Button(right_area, text="ADMIN", bg="#555", fg="white",
              width=20, command=admin_login).grid(row=3, column=0, pady=10)

    # TAMPILKAN ITEM
    def tampilkan_produk():
        conn = GetConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT namaproduk, harga, gambar FROM products")
        hasil = cursor.fetchall()
        conn.close()

        for widget in display.winfo_children():
            widget.destroy()

        total_kolom = 4
        row = col = 0

        for nama, harga, gambar in hasil:

            if not gambar or not os.path.exists(gambar):
                gambar = "img/default.png"

            img = Image.open(gambar)
            img = img.resize((50, 50))
            img_tk = ImageTk.PhotoImage(img)

            card = tk.Frame(display, bg="#3a3a3a", bd=2, relief="solid")
            card.grid(row=row, column=col, padx=5, pady=5)

            tk.Label(card, image=img_tk, bg="white").pack()
            tk.Label(card, text=nama, fg="white", bg="#3a3a3a").pack()
            tk.Label(card, text=f"Rp {harga}", fg="#ffdd33",
                     bg="#3a3a3a", font=("Arial", 8, "bold")).pack()

            card.image = img_tk

            col += 1
            if col == total_kolom:
                col = 0
                row += 1

    tampilkan_produk()

# =========================================================
# START
# =========================================================
show_vending_machine()
root.mainloop()
