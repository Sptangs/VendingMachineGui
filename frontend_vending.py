import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os

class VendingFrontend:
    """Frontend tampilan Vending Machine"""

    def __init__(self, root, backend, COLORS):
        self.root = root
        self.backend = backend
        self.COLORS = COLORS

        # variabel keypad
        self.mode = ""
        self.temp = ""

    # =====================================================
    #   POPUP
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
    #   TAMPILKAN VENDING MACHINE
    # =====================================================
    def show_vending_machine(self, on_back=None):

        # clear widget
        for w in self.root.winfo_children():
            w.destroy()

        # FRAME UTAMA
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)

        # TITLE
        title_frame = tk.Frame(main_frame, bg="white")
        title_frame.grid(row=0, column=0, columnspan=2, pady=2)

        tk.Label(title_frame, text="VENDING MACHINE",
                 font=("Arial", 15, "bold"), bg="white").pack()
        tk.Label(title_frame, text="Selamat Datang!",
                 font=("Arial", 10), bg="white", fg="#555").pack()

        # DISPLAY PRODUK
        display = tk.Frame(main_frame, bg="#333", bd=8, relief="ridge")
        display.grid(row=1, column=0, sticky="nsew", padx=(10, 2), pady=(10, 5))

        # AREA KANAN
        right_area = tk.Frame(main_frame, bg="#eeeeee")
        right_area.grid(row=1, column=1, sticky="nsew", padx=(2, 10), pady=(10, 5))

        right_area.grid_rowconfigure(1, weight=1)
        right_area.grid_columnconfigure(0, weight=1)

        # CONTROL PANEL
        control_frame = tk.Frame(right_area, bg="#ddd")
        control_frame.grid(row=0, column=0, sticky="ne", padx=5, pady=5)

        entry = tk.Entry(control_frame, font=("Arial", 14), width=28, justify="center")
        entry.grid(row=0, column=0, columnspan=2, pady=2)

        coin_label = tk.Label(control_frame, text="Koin:", font=("Arial", 10), bg="#ddd")
        coin_label.grid(row=1, column=0, sticky="e")
        coin_entry = tk.Entry(control_frame, width=30)
        coin_entry.grid(row=1, column=1)

        id_label = tk.Label(control_frame, text="ID Produk:", font=("Arial", 10), bg="#ddd")
        id_label.grid(row=2, column=0, sticky="e")
        id_entry = tk.Entry(control_frame, width=30)
        id_entry.grid(row=2, column=1)

        # MODE INPUT
        def set_koin():
            self.mode = "koin"
            self.temp = ""
            entry.delete(0, tk.END)

        def set_id():
            self.mode = "id"
            self.temp = ""
            entry.delete(0, tk.END)

        tk.Button(control_frame, text="INPUT KOIN", bg="orange",
                  width=10, command=set_koin).grid(row=3, column=0, pady=5)

        tk.Button(control_frame, text="INPUT ID", bg="lightblue",
                  width=10, command=set_id).grid(row=3, column=1, pady=5)

        # =====================================================
        # KEYPAD
        # =====================================================
        keypad_frame = tk.Frame(right_area, bg="#eeeeee")
        keypad_frame.grid(row=1, column=0, pady=10, sticky='nsew')

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

            b = tk.Button(keypad_frame, text=t, width=6, height=2,
                          font=("Arial", 12, "bold"), bg=bg)
            b.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

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

        # =====================================================
        # BELI PRODUK (PAKAI BACKEND)
        # =====================================================
        def beli():
            try:
                coin = int(coin_entry.get())
                pid = int(id_entry.get())

                # gunakan backend
                result = self.backend.process_purchase(pid, coin)

                if not result["success"]:
                    self.show_popup(f"\n❌ {result['message']}\n")
                else:
                    pesan = (
                        f"\n✅ {result['message']}\n"
                        f"Harga      : Rp {result['harga']}\n"
                        f"Uang Masuk : Rp {result['coin']}\n"
                        f"Kembalian  : Rp {result['kembalian']}\n"
                    )
                    self.show_popup(pesan)

                coin_entry.delete(0, tk.END)
                id_entry.delete(0, tk.END)

            except:
                self.show_popup("\nInput tidak valid!\n")

        tk.Button(right_area, text="BELI PRODUK", bg="green", fg="white",
                  width=20, command=beli).grid(row=2, column=0, pady=5)

        # =====================================================
        # TAMPILKAN PRODUK (PAKAI BACKEND)
        # =====================================================
        def tampilkan_produk():
            data = self.backend.get_all_products()

            if not data["success"]:
                self.show_popup(data["message"])
                return

            hasil = data["products"]

            for widget in display.winfo_children():
                widget.destroy()

            total_kolom = 4
            for i in range(total_kolom):
                display.grid_columnconfigure(i, weight=1)

            row, col = 0, 0

            for pid, nama, harga, gambar in hasil:

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

        tampilkan_produk()
