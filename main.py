import tkinter as tk
from PIL import ImageTk, Image
import sys, os

class HackingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hacking App")
        self.geometry("500x300")
        self.resizable(False, False)

        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("B.TLabel", font=(None, 40))
        style.configure("B.TButton", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
        style.configure("TEntry", foregound="black", background="white")



if __name__ == "__main__":
    app = HackingApp()
    app.mainloop()