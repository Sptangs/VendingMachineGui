import tkinter as tk
from tkinter import messagebox, ttk
from backend_admin import AdminBackend

class AdminFrontend:
    """Frontend untuk panel admin"""
    
    def __init__(self, root, backend: AdminBackend, colors: dict):
        self.root = root
        self.backend = backend
        self.colors = colors
        self.data_frame = None
    
    def clear_window(self):
        """Membersihkan semua widget di window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_data_frame(self):
        """Membersihkan data frame"""
        if self.data_frame is not None:
            self.data_frame.destroy()
            self.data_frame = None
    
    def show_login(self, on_success):
        """Menampilkan dialog login admin"""
        login = tk.Toplevel(self.root)
        login.title("Login Admin")
        login.geometry("350x300")
        login.configure(bg=self.colors['background'])
        login.resizable(False, False)
        
        login.transient(self.root)
        login.grab_set()
        
        tk.Label(login, text="LOGIN ADMIN",
                 font=("Arial", 16, "bold"),
                 bg=self.colors['background']).pack(pady=20)
        
        tk.Label(login, text="Username:", bg=self.colors['background']).pack()
        user = tk.Entry(login, width=25)
        user.insert(0, "admin")
        user.pack(pady=5)
        
        tk.Label(login, text="Password:", bg=self.colors['background']).pack()
        pwd = tk.Entry(login, width=25, show="*")
        pwd.insert(0, "123")
        pwd.pack(pady=5)
        
        
        def check():
            if self.backend.authenticate_admin(user.get(), pwd.get()):
                login.destroy()
                on_success()
            else:
                messagebox.showerror("Gagal", "Username / Password salah!")
        
        tk.Button(login, text="Login", bg=self.colors['success'],
                  fg='white', width=12, command=check).pack(pady=20)
    
    def show_panel(self, on_back):
        """Menampilkan panel admin"""
        self.clear_window()
        
        header = tk.Label(self.root, text="PANEL ADMIN",
                          bg=self.colors['background'], 
                          font=("Arial", 20, "bold"))
        header.pack(pady=20)
        
        tk.Button(self.root, text="Kembali", bg=self.colors['danger'], 
                  fg='white', command=on_back).pack(pady=10)
        
        menu_frame = tk.Frame(self.root, bg=self.colors['background'])
        menu_frame.pack(pady=20)
        
        btn_style = {'font': ("Arial", 12, "bold"),
                     'width': 15, 'pady': 10, 'cursor': "hand2"}
        
        tk.Button(menu_frame, text="Tambah Produk", bg='#28a745', fg='white',
                  command=self.add_product, **btn_style).grid(
                      row=0, column=0, padx=10, pady=10)
        
        tk.Button(menu_frame, text="Lihat Produk", bg='#17a2b8', fg='white',
                  command=self.view_products, **btn_style).grid(
                      row=0, column=1, padx=10, pady=10)
        
        tk.Button(menu_frame, text="Update Produk", bg='#ffc107', fg='white',
                  command=self.update_product, **btn_style).grid(
                      row=1, column=0, padx=10, pady=10)
        
        tk.Button(menu_frame, text="Hapus Produk", bg='#dc3545', fg='white',
                  command=self.delete_product, **btn_style).grid(
                      row=1, column=1, padx=10, pady=10)
        
        self.data_frame = tk.Frame(self.root, bg='white')
        self.data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def add_product(self):
        """Form tambah produk"""
        self.clear_data_frame()
        
        self.data_frame = tk.Frame(self.root, bg='white')
        self.data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(self.data_frame, text="Tambah Produk", bg='white',
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.data_frame, text="Nama:", bg='white').pack()
        name_entry = tk.Entry(self.data_frame, width=30)
        name_entry.pack()
        
        tk.Label(self.data_frame, text="Harga:", bg='white').pack()
        price_entry = tk.Entry(self.data_frame, width=30)
        price_entry.pack()

        tk.Label(self.data_frame, text="ID:", bg='white').pack()
        id_entry = tk.Entry(self.data_frame, width=30)
        id_entry.pack()
        
        def save():
            id = id_entry.get()
            nama = name_entry.get()
            harga = price_entry.get()
            
            if not nama or not harga or not id:
                messagebox.showwarning("Input Error", "Semua field harus diisi!")
                return
            
            try:
                harga = float(harga)
                result = self.backend.add_product(id,nama, harga)
                
                if result['success']:
                    messagebox.showinfo("Sukses", result['message'])
                    self.add_product()  # Reset form
                else:
                    messagebox.showerror("Error", result['message'])
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka!")
        
        tk.Button(self.data_frame, text="Simpan", bg=self.colors['success'],
                  fg='white', width=15, command=save).pack(pady=10)
    
    def view_products(self):
        """Tampilkan daftar produk"""
        self.clear_data_frame()
        
        self.data_frame = tk.Frame(self.root, bg='white')
        self.data_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        cols = ("ID", "Nama Produk", "Harga")
        table = ttk.Treeview(self.data_frame, columns=cols, show="headings")
        table.pack(fill=tk.BOTH, expand=True)
        
        for col in cols:
            table.heading(col, text=col)
        
        result = self.backend.get_all_products()
        
        if result['success']:
            for row in result['products']:
                table.insert("", tk.END, values=row[:3])  # ID, Nama, Harga
        else:
            messagebox.showerror("Error", result['message'])
    
    def update_product(self):
        """Form update produk"""
        self.clear_data_frame()
        
        self.data_frame = tk.Frame(self.root, bg='white')
        self.data_frame.pack(expand=True, padx=20, pady=20)
        
        tk.Label(self.data_frame, text="Update Produk", bg='white',
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        form = tk.Frame(self.data_frame, bg="white")
        form.pack(padx=20, expand=True)
        
        tk.Label(form, text="ID Lama:", bg="white").grid(row=0, column=0, sticky="w")
        id_lama_entry = tk.Entry(form, width=25)
        id_lama_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form, text="ID Baru:", bg="white").grid(row=1, column=0, sticky="w")
        id_baru_entry = tk.Entry(form, width=25)
        id_baru_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(form, text="Nama Baru:", bg="white").grid(row=2, column=0, sticky="w")
        nama_entry = tk.Entry(form, width=25)
        nama_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(form, text="Harga Baru:", bg="white").grid(row=3, column=0, sticky="w")
        harga_entry = tk.Entry(form, width=25)
        harga_entry.grid(row=3, column=1, pady=5)
        
        def submit_update():
            id_lama = id_lama_entry.get()
            id_baru = id_baru_entry.get()
            nama_baru = nama_entry.get()
            harga_baru = harga_entry.get()
            
            if not id_lama or not id_baru or not nama_baru or not harga_baru:
                messagebox.showwarning("Input Error", "Semua field harus diisi!")
                return
            
            try:
                id_lama = int(id_lama)
                id_baru = int(id_baru)
                harga_baru = float(harga_baru)
                
                result = self.backend.update_product(id_lama, id_baru, 
                                                     nama_baru, harga_baru)
                
                if result['success']:
                    messagebox.showinfo("Success", result['message'])
                else:
                    messagebox.showerror("Error", result['message'])
            except ValueError:
                messagebox.showerror("Error", "ID dan Harga harus berupa angka!")
        
        submit_btn = tk.Button(self.data_frame, text="UPDATE", 
                              bg="yellow", fg="black",
                              font=("Arial", 10, "bold"), 
                              command=submit_update)
        submit_btn.pack(fill=tk.X, pady=10)
    
    def delete_product(self):
        """Form hapus produk"""
        self.clear_data_frame()
        
        self.data_frame = tk.Frame(self.root, bg="white")
        self.data_frame.pack(expand=True, padx=20, pady=20)
        
        tk.Label(self.data_frame, text="HAPUS PRODUK", 
                 font=("Arial", 14, "bold"),
                 bg="white", fg="black").pack(pady=(0, 20))
        
        form = tk.Frame(self.data_frame, bg="white")
        form.pack(padx=20, expand=True)
        
        tk.Label(form, text="ID Produk yang akan dihapus:", 
                 bg="white", anchor="w").pack(fill=tk.X, pady=5)
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
                    id_val = int(id_val)
                    result = self.backend.delete_product(id_val)
                    
                    if result['success']:
                        messagebox.showinfo("Success", result['message'])
                        id_entry.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error", result['message'])
                except ValueError:
                    messagebox.showerror("Error", "ID harus berupa angka!")
        
        submit_btn = tk.Button(self.data_frame, text="HAPUS", 
                              bg="red", fg="white",
                              font=("Arial", 10, "bold"), 
                              command=submit_delete)
        submit_btn.pack(fill=tk.X, pady=10)