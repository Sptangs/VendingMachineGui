import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
from frontend_admin import AdminFrontend
from backend_admin import AdminBackend

class VendingFrontend:
    """Frontend tampilan Vending Machine"""

    def __init__(self, root, backend, COLORS):
        self.root = root
        self.backend = backend
        self.COLORS = COLORS

        self.mode = ""
        self.temp = ""

    def go_to_admin(self):
        admin_backend = AdminBackend()   
        admin = AdminFrontend(
            self.root,
            admin_backend,               
            self.COLORS
        )

        admin.show_login(
            on_success=lambda: admin.show_panel(
                on_back=self.show_vending_machine
            )
        )
    
    # =====================================================
    #   SIMPLE POPUP (untuk pesan singkat)
    # =====================================================
    def show_popup(self, pesan, title="Informasi"):
        pop = tk.Toplevel()
        pop.title(title)
        pop.geometry("300x180")
        pop.configure(bg="white")
        pop.resizable(0, 0)

        tk.Label(pop, text=title, font=("Arial", 14, "bold"), bg="white").pack(pady=5)
        tk.Label(pop, text=pesan, font=("Arial", 12), bg="white").pack(pady=5)

        tk.Button(
            pop, text="OK", bg="#4CAF50", fg="white",
            font=("Arial", 12), command=pop.destroy
        ).pack(pady=(5, 10))

    # =====================================================
    #   INFORMATIVE POPUP (lebih besar + gambar produk)
    # =====================================================
    def show_info_popup(self, nama_produk, harga, uang_masuk, kembalian, gambar_path):
        popup = tk.Toplevel()
        popup.title("Informasi")
        popup.geometry("420x500")  
        popup.resizable(False, False)

        main_frame = tk.Frame(popup, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        title = tk.Label(
            main_frame,
            text="Informasi",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(0, 20))

        try:
            if not gambar_path or not os.path.exists(gambar_path):
                raise FileNotFoundError()

            img = Image.open(gambar_path)
            img = img.resize((160, 160))
            photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(main_frame, image=photo)
            img_label.image = photo
            img_label.pack(pady=5)
        except:
            tk.Label(main_frame, text="[Gambar Tidak Ditemukan]", font=("Arial", 12)).pack(pady=5)

        info_text = (
            f"✔ Berhasil membeli {nama_produk}\n\n"
            f"Harga        : Rp {harga}\n"
            f"Uang Masuk   : Rp {uang_masuk}\n"
            f"Kembalian    : Rp {kembalian}"
        )

        info_label = tk.Label(
            main_frame,
            text=info_text,
            justify="left",
            font=("Arial", 14)
        )
        info_label.pack(pady=10)

        btn_ok = tk.Button(
            main_frame,
            text="OK",
            font=("Arial", 12, "bold"),
            width=12,
            command=popup.destroy
        )
        btn_ok.pack(pady=15)

        popup.grab_set()

    # =====================================================
    #   TAMPILKAN VENDING MACHINE
    # =====================================================
    def show_vending_machine(self, on_back=None):

        for w in self.root.winfo_children():
            w.destroy()


        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=0)
        

    
        title_frame = tk.Frame(main_frame, bg="white")
        title_frame.grid(row=0, column=0, columnspan= 3)

        # =============================
        # RUNNING TEXT
        # =============================
        welcome_text = "   Selamat Datang di Vending Machine Kami!   "
        running_label = tk.Label(
            title_frame,
            text=welcome_text,
            font=("Times New Roman", 15),
            bg="black",
            fg="white",
            justify="center",
            bd=5,            
            relief="ridge",   
            padx=5, pady=2, height= 3  
        )
        running_label.pack(pady=(5, 0), fill="x") 

        def scroll_text():
            nonlocal welcome_text

            welcome_text = welcome_text[1:] + welcome_text[0]
            running_label.config(text=welcome_text)

            running_label.after(200, scroll_text)

        scroll_text() 


        display = tk.Frame(main_frame, bg="#333", bd=8, relief="raise", height=75, width=100)
        display.grid(row=2, column=0,columnspan=3, sticky="nsew", padx=(10, 10), pady=10)

        display = tk.Frame(main_frame, bg="#333", bd=8, relief="ridge", width=100)
        display.grid(row=1, column=0,columnspan=2, sticky="nsew", padx=(10, 2), pady=10)

        right_area = tk.Frame(main_frame, bg="grey")
        right_area.grid(row=1, column=2, sticky="nsew", padx=(2, 10), pady=10)

        right_area.grid_rowconfigure(1, weight=1)
        right_area.grid_columnconfigure(0, weight=1)

        control_frame = tk.Frame(right_area, bg="#ddd",)
        control_frame.grid(row=0, column=0, sticky="nsew", pady=5,padx=5)

        entry = tk.Entry(control_frame, font=("Arial", 14), width=28, justify="center")
        entry.grid(row=0, column=0, columnspan=2, pady=3,padx=2)

        coin_label = tk.Label(control_frame, text="Koin:", font=("Arial", 10), bg="#ddd")
        coin_label.grid(row=1, column=0, sticky="e")
        coin_entry = tk.Entry(control_frame, width=20)
        coin_entry.grid(row=1, column=1)

        id_label = tk.Label(control_frame, text="ID Produk:", font=("Arial", 10), bg="#ddd")
        id_label.grid(row=2, column=0, sticky="e")
        id_entry = tk.Entry(control_frame, width=20)
        id_entry.grid(row=2, column=1)

        def set_koin():
            self.mode = "koin"
            self.temp = ""
            entry.delete(0, tk.END)

        def set_id():
            self.mode = "id"
            self.temp = ""
            entry.delete(0, tk.END)

        tk.Button(control_frame, text="INPUT KOIN", bg="orange",
                  width=10, command=set_koin).grid(row=3, column=0, pady=2)

        tk.Button(control_frame, text="INPUT ID", bg="lightblue",
                  width=10, command=set_id).grid(row=3, column=1, pady=2)

        # =====================================================
        # KEYPAD
        # =====================================================
        keypad_frame = tk.Frame(right_area, bg="#eeeeee")
        keypad_frame.grid(row=1, column=0,padx=2)

        tombol = [
            "1", "2", "3", "C",
            "4", "5", "6", "0",
            "7", "8", "9", "OK"
        ]

        def press(t):
            self.temp += t
            entry.delete(0, tk.END)
            entry.insert(0, self.temp)

        def clear():
            self.temp = ""
            entry.delete(0, tk.END)

        def ok():
            if self.mode == "koin":
                coin_entry.delete(0, tk.END)
                coin_entry.insert(0, self.temp)
            else:
                id_entry.delete(0, tk.END)
                id_entry.insert(0, self.temp)

            self.temp = ""
            entry.delete(0, tk.END)

        r, c = 0, 0
        for t in tombol:
            bg = "#4CAF50" if t == "OK" else "#ff6b6b" if t == "C" else "white"

            b = tk.Button(keypad_frame, text=t, width=6, height=3, relief="raised",bd="4",
                          font=("Arial", 12, "bold"), bg=bg)
            b.grid(row=r, column=c, padx=2, pady=1, sticky="nsew")

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

        for i in range(4):
            keypad_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            keypad_frame.grid_rowconfigure(i, weight=1)

        def beli():
            try:
                coin = int(coin_entry.get())
                pid = int(id_entry.get())
            except ValueError:
                self.show_popup("\nInput tidak valid!\n")
                return
            result = self.backend.process_purchase(pid, coin)

            if not result.get("success"):
                self.show_popup(f"\n❌ {result.get('message')}\n")
            else:
                prod_info = self.backend.get_product_by_id(pid)
                gambar_path = prod_info.get("gambar") if prod_info.get("success") else None

                self.show_info_popup(
                    result.get("nama_produk", "Produk"),
                    result.get("harga", 0),
                    result.get("coin", coin),
                    result.get("kembalian", 0),
                    gambar_path or "img/default.png"
                )

            coin_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)

        tk.Button(right_area, text="BELI PRODUK", bg="green", fg="white",
                  width=20, command=beli).grid(row=2, column=0, pady=2)
        
        tk.Button(
                right_area,
                text="ADMIN",
                bg="green",
                fg="white",
                width=20,
                command=self.go_to_admin
            ).grid(row=3, column=0, padx=5)

        def tampilkan_produk():
            data = self.backend.get_all_products()

            if not data.get("success"):
                self.show_popup(data.get("message", "Gagal memuat produk"))
                return

            hasil = data.get("products", [])

            for widget in display.winfo_children():
                widget.destroy()

            total_kolom = 4
            for i in range(total_kolom):
                display.grid_columnconfigure(i, weight=1)

            row, col = 0, 0
            for item in hasil:
                if len(item) == 4:
                    pid, nama, harga, gambar = item
                elif len(item) == 3:
                    pid, nama, harga = item
                    gambar = None
                else:
                    continue

                if not gambar or not os.path.exists(gambar):
                    gambar = "img/default.png"

                try:
                    img = Image.open(gambar)
   
                    max_width, max_height = 75, 50
                    img.thumbnail((max_width, max_height))
                    
                    img_tk = ImageTk.PhotoImage(img)
                except:
                    img_tk = None

                card = tk.Frame(display, bg="#3a3a3a", bd=2, relief="solid")
                card.grid(row=row, column=col, padx=5, pady=5, sticky="n")

                if img_tk:
                    tk.Label(card, image=img_tk, bg="white").pack()
                    card.image = img_tk
                else:
                    tk.Label(card, text="[No Img]", bg="#3a3a3a", fg="white").pack()

                tk.Label(card, text=nama, fg="white", bg="#3a3a3a",
                        font=("Arial", 8)).pack()
                tk.Label(card, text=f"Rp {harga}", fg="#ffdd33", bg="#3a3a3a",
                        font=("Arial", 8, "bold")).pack()


                col += 1
                if col == total_kolom:
                    col = 0
                    row += 1

        tampilkan_produk()
