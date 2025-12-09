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

root = tk.Tk()
root.title("Aplikasi Vending Machine")
root.geometry("900x600")
root.configure(bg=COLORS['background'])
root.resizable(0, 0)

data_frame = None


# =============================================================
# SYSTEM MENU
# =============================================================

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def clear_data_frame():
    global data_frame
    if data_frame is not None:
        data_frame.destroy()
        data_frame = None


# =============================================================
# HALAMAN MENU UTAMA
# =============================================================
def show_main_menu():
    clear_window()

    content_frame = tk.Frame(root, bg=COLORS['background'])
    content_frame.pack(fill=tk.BOTH, expand=True)

    header = tk.Label(content_frame, text="MENU UTAMA",
                      font=("Arial", 22, "bold"), bg=COLORS['background'])
    header.pack(pady=40)

    button_frame = tk.Frame(content_frame, bg=COLORS['background'])
    button_frame.pack()

    # Tombol Belanja
    btn_beli = tk.Button(
        button_frame, text="Mode Belanja", bg=COLORS['secondary'], fg='white',
        font=("Arial", 14, "bold"), width=20, pady=10,
        command=show_vending_machine
    )
    btn_beli.pack(pady=10)

    # Tombol Admin
    btn_admin = tk.Button(
        button_frame, text="Admin", bg=COLORS['warning'], fg='white',
        font=("Arial", 14, "bold"), width=20, pady=10,
        command=admin_login
    )
    btn_admin.pack(pady=10)


# =============================================================
# LOGIN ADMIN CRUD
# =============================================================
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


# =============================================================
# PANEL ADMIN
# =============================================================
def show_admin_panel():
    clear_window()
    global data_frame

    header = tk.Label(root, text="PANEL ADMIN",
                      bg=COLORS['background'], font=("Arial", 20, "bold"))
    header.pack(pady=20)

    tk.Button(root, text="Kembali", bg=COLORS['danger'], fg='white',
              command=show_main_menu).pack(pady=10)

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


# =============================================================
# CRUD PRODUK
# =============================================================
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

    tk.Label(form, text="ID Lama:", bg="white").grid(row=0, column=0, sticky="w")
    id_lama = tk.Entry(form, width=25)
    id_lama.grid(row=0, column=1, pady=5)

    tk.Label(form, text="ID Baru:", bg="white").grid(row=1, column=0, sticky="w")
    id_baru = tk.Entry(form, width=25)
    id_baru.grid(row=1, column=1, pady=5)

    tk.Label(form, text="Nama Baru:", bg="white").grid(row=2, column=0, sticky="w")
    nama_baru = tk.Entry(form, width=25)
    nama_baru.grid(row=2, column=1, pady=5)

    tk.Label(form, text="Harga Baru:", bg="white").grid(row=3, column=0, sticky="w")
    harga_baru = tk.Entry(form, width=25)
    harga_baru.grid(row=3, column=1, pady=5)

    def submit_update():
        id_lama = id_lama_entry.get()
        id_baru = id_baru_entry.get()
        nama_baru = nama_entry.get()
        harga_baru = harga_entry.get()

        if not id_lama or not id_baru or not nama_baru or not harga_baru:
            messagebox.showwarning("Input Error", "Semua field harus diisi!")
            return

        try:
            conn = GetConnection()
            if conn:
                cursor = conn.cursor()
                query = """
                        UPDATE products
                        SET id=%s, \
                            namaProduk=%s, \
                            harga=%s
                        WHERE id = %s \
                        """
                data = (id_baru, nama_baru, harga_baru, id_lama)
                cursor.execute(query, data)
                conn.commit()
                messagebox.showinfo("Success", "Data berhasil diperbarui!")
                cursor.close()
                conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    submit_btn = tk.Button(data_frame, text="UPDATE", bg="yellow", fg="black",
                           font=("Arial", 10, "bold",), command=submit_update)
    submit_btn.pack(fill=tk.X, pady=10)


def delete_product():
        clear_data_frame()
        global data_frame

        data_frame = tk.Frame(root, bg="white")
        data_frame.pack(expand=True, padx=20, pady=20)

        tk.Label(data_frame, text="HAPUS PRODUK", font=("Arial", 14, "bold"),
                 bg="white", fg="black").pack(pady=(0, 20))

        form = tk.Frame(data_frame, bg="white")
        form.pack(padx=20, expand=True)

        tk.Label(form, text="ID Produk yang akan dihapus:", bg="white", anchor="w").pack(fill=tk.X, pady=5)
        id_entry = tk.Entry(form)
        id_entry.pack(fill=tk.X, pady=(0, 20))

        def submit_delete():
            id_val = id_entry.get()

            if not id_val:
                messagebox.showwarning("Input Error", "ID harus diisi!")
                return

            response = messagebox.askyesno("Konfirmasi",
                                           f"Yakin hapus produk dengan ID: {id_val}?")
            if response:
                try:
                    conn = GetConnection()
                    if conn:
                        cursor = conn.cursor()
                        query = "DELETE FROM products WHERE id=%s"
                        data = (id_val,)
                        cursor.execute(query, data)
                        conn.commit()
                        messagebox.showinfo("Success", "Data berhasil dihapus!")
                        cursor.close()
                        conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")

        submit_btn = tk.Button(data_frame, text="HAPUS", bg="red", fg="white",
                               font=("Arial", 10, "bold"), command=submit_delete)
        submit_btn.pack(fill=tk.X, pady=10)



# =============================================================
# VENDING MACHINE + POPUP KEYPAD dan TAMPILAN PRODUK
# =============================================================
def show_vending_machine():
    clear_window()

    root.update_idletasks()

    # =============================
    #  FRAME UTAMA (2 KOLOM)
    # =============================
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # GRID
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_columnconfigure(0, weight=3)  # DISPLAY BESAR DI KIRI
    main_frame.grid_columnconfigure(1, weight=1)  # CANVAS DI KANAN

    # =============================
    #  TITLE DI ATAS
    # =============================
    title_frame = tk.Frame(main_frame, bg="white")
    title_frame.grid(row=0, column=0, columnspan=2, pady=2)

    tk.Label(title_frame,
             text="VENDING MACHINE",
             font=("Arial", 15, "bold"),
             bg="white").pack()

    tk.Label(title_frame,
             text="Selamat Datang!",
             font=("Arial", 10),
             bg="white",
             fg="#555").pack()

    # =============================
    #  DISPLAY PRODUK DI KIRI
    # =============================
    display = tk.Frame(main_frame, bg="#333", bd=8, relief="ridge")
    display.grid(row=1, column=0, sticky="nsew", padx=(10, 2), pady=(10, 5))

    # =============================
    #  CANVAS DI KANAN
    # =============================
    canvas = tk.Canvas(main_frame, bg="#eeeeee", bd=2, relief="ridge", width=50)
    canvas.grid(row=1, column=1, sticky="nsew", padx=(2, 10), pady=(10, 5))

    # Gambar panel mesin sederhana
    canvas.create_rectangle(10, 10, 160, 485, fill="#591b3c", outline="black")

    # Tombol keypad
    canvas.create_rectangle(20, 200, 150, 250, fill="#888", tags="vm")
    canvas.create_text(90, 225, text="KEYPAD", tags="vm")

    canvas.tag_bind("vm", "<Button-1>", open_keypad)

    # =============================
    #  FUNGSI TAMPILKAN PRODUK
    # =============================
    def tampilkan_produk():
        conn = GetConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT namaproduk, harga, gambar FROM products")
        hasil = cursor.fetchall()

        # Bersihkan isi display
        for widget in display.winfo_children():
            widget.destroy()

        # Atur jumlah kolom per baris
        total_kolom = 4

        # Kolom proporsional
        for i in range(total_kolom):
            display.grid_columnconfigure(i, weight=1, uniform="col")

        row, col = 0, 0

        for nama, harga, gambar in hasil:

            # Jika gambar tidak ada → pakai default
            if not gambar or not os.path.exists(gambar):
                gambar = "img/default.png"

            # Perkecil ukuran agar lebih compact
            img = Image.open(gambar)
            img = img.resize((40, 40))  # lebih kecil = lebih rapi
            img_tk = ImageTk.PhotoImage(img)

            # Card lebih kecil & tanpa jarak besar
            card = tk.Frame(display, bg="#3a3a3a", bd=2, relief="solid")
            card.grid(row=row, column=col, padx=(3, 0), pady=(3, 3), sticky="n")

            # Gambar
            tk.Label(card, image=img_tk, bg="white").pack(pady=(1, 0))

            # Nama produk
            tk.Label(card, text=nama, fg="white", bg="#3a3a3a",
                     font=("Arial", 7)).pack()

            # Harga
            tk.Label(card, text=f"Rp {harga}", fg="#ffdd33", bg="#3a3a3a",
                     font=("Arial", 7, "bold")).pack(pady=(0, 2))

            # prevent gambar hilang
            card.image = img_tk

            # Geser kolom
            col += 1
            if col == total_kolom:
                col = 0
                row += 1

        conn.close()

    tampilkan_produk()

    # =============================
    #  TOMBOL KEMBALI DI KANAN BAWAH
    # =============================
    btn_frame = tk.Frame(root, bg="white")
    btn_frame.pack(fill="x", side="bottom")

    tk.Button(btn_frame,
              text="Kembali",
              bg=COLORS['danger'],
              fg="white",
              width=12,
              command=show_main_menu).pack(anchor="e", padx=10, pady=(2, 5))

# ================= POPUP KEYPAD ====================
def open_keypad(event=None):
    win = tk.Toplevel(root)
    win.title("Input Vending Machine")
    win.geometry("360x600")
    win.resizable(0, 0)
    win.configure(bg="#ececec")

    win.mode = "koin"
    win.temp = ""

    tk.Label(win, text="VENDING MACHINE",
             font=("Arial", 16, "bold"), bg="#ececec").pack(pady=5)

    entry = tk.Entry(win, font=("Arial", 18), justify="center")
    entry.pack()

    tk.Label(win, text="Masukkan Koin (min 1000)", bg="#ececec").pack()
    coin_entry = tk.Entry(win, font=("Arial", 14), justify="center")
    coin_entry.pack()

    tk.Label(win, text="Masukkan ID Produk", bg="#ececec").pack()
    id_entry = tk.Entry(win, font=("Arial", 14), justify="center")
    id_entry.pack()

    text = tk.Text(win, width=43, height=8)
    text.pack(pady=5)

    # tampilkan daftar produk
    def tampil():
        try:
            conn = GetConnection()
            cur = conn.cursor()
            cur.execute("SELECT id, namaproduk, harga FROM products")
            rows = cur.fetchall()

            text.delete(1.0, tk.END)
            text.insert(tk.END, "===== DAFTAR PRODUK =====\n")
            for r in rows:
                text.insert(tk.END, f"ID: {r[0]} | {r[1]} | Harga: {r[2]}\n")

        except Exception as e:
            text.insert(tk.END, f"DB Error: {e}")

    tampil()

    # keypad mode
    def set_koin():
        win.mode = "koin"
        win.temp = ""
        entry.delete(0, tk.END)

    def set_id():
        win.mode = "id"
        win.temp = ""
        entry.delete(0, tk.END)

    btn_frame = tk.Frame(win, bg="#ececec")
    btn_frame.pack()

    tk.Button(btn_frame, text="INPUT KOIN", bg="orange",
              width=12, command=set_koin).grid(row=0, column=0)
    tk.Button(btn_frame, text="INPUT ID", bg="lightblue",
              width=12, command=set_id).grid(row=0, column=1)

    key_frame = tk.Frame(win)
    key_frame.pack()

    tombol = ["1", "2", "3", "C",
              "4", "5", "6", "0",
              "7", "8", "9", "OK"]

    def press(t):
        win.temp += t
        entry.delete(0, tk.END)
        entry.insert(0, win.temp)

    def clear():
        win.temp = ""
        entry.delete(0, tk.END)

    def ok():
        if win.mode == "koin":
            coin_entry.delete(0, tk.END)
            coin_entry.insert(0, win.temp)
        else:
            id_entry.delete(0, tk.END)
            id_entry.insert(0, win.temp)

        win.temp = ""
        entry.delete(0, tk.END)

    r, c = 0, 0
    for t in tombol:
        bg = "#4CAF50" if t == "OK" else "#ff6b6b" if t == "C" else "white"
        b = tk.Button(key_frame, text=t, width=6, height=2,
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

    # fungsi beli
    def beli():
        try:
            coin = int(coin_entry.get())
            pid = int(id_entry.get())

            conn = GetConnection()
            cur = conn.cursor()
            cur.execute("SELECT namaProduk, harga FROM products WHERE id=%s", (pid,))
            row = cur.fetchone()

            coin_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)

            if not row:
                show_popup(f"\n❌ Produk tidak ditemukan!\n")
                return

            nama, harga = row
            if coin < harga:
                show_popup(f"\n⚠ Uang kurang {harga - coin}\n")
            else:
                show_popup(f"\n✅ Berhasil beli {nama}\nKembalian: {coin - harga}\n")

        except:
            show_popup(f"\nInput salah!\n")

    tk.Button(win, text="BELI PRODUK", bg="green",
              fg="white", width=20, command=beli).pack(pady=5)

    tk.Button(win, text="Refresh", command=tampil).pack(pady=3)


# =============================================================
# RUN PROGRAM
# =============================================================
show_main_menu()
root.mainloop()
