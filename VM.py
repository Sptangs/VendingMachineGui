import tkinter as tk

root = tk.Tk()
root.title("VENDING MACHINE")
root.geometry("380x500")

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.create_rectangle(10, 10, 370, 490, fill="red", outline="black")
canvas.create_rectangle(20, 20, 280, 400, fill="white", outline="black")
canvas.create_rectangle(20, 420, 280, 470, fill="gray", outline="black")
canvas.create_rectangle(290, 300, 360, 350, fill="gray", outline="black")

def open_desktop(event=None):
    win = tk.Toplevel(root)
    win.title("Keypad")
    win.geometry("250x200")
    win.configure(bg="lightgray")


def keypat():
    keypad = canvas.create_rectangle(
        290, 200, 360, 250,
        fill="grey", outline="white",
        tags="keypad"
    )

    canvas.tag_bind("keypad", "<Button-1>", open_desktop)

keypat()

root.mainloop()
