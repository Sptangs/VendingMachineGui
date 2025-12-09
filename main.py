import tkinter as tk
from backend_vending import VendingBackend
from frontend_vending import VendingFrontend

# Konfigurasi warna UI
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

class VendingMachineApp:
    """Aplikasi utama Vending Machine - langsung masuk ke mode belanja"""

    def __init__(self):
        # Setup window
        self.root = tk.Tk()
        self.root.title("Aplikasi Vending Machine")
        self.root.geometry("900x600")
        self.root.configure(bg=COLORS['background'])
        self.root.resizable(0, 0)

        # Inisialisasi backend & frontend vending
        self.vending_backend = VendingBackend()
        self.vending_frontend = VendingFrontend(self.root, self.vending_backend, COLORS)

        # Langsung buka tampilan vending machine
        self.show_vending()

    def show_vending(self):
        """Menampilkan layar vending machine utama"""
        self.vending_frontend.show_vending_machine(on_back=None)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = VendingMachineApp()
    app.run()
