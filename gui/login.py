import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from .dashboard import run_dashboard #to switch after login
from utils.registration import authenticate, register  # NEW
from gui.dashboard import run_dashboard

def run_login():
    #clicks login
    def handle_login():
        username = entry_username.get()
        password = entry_password.get()
        if authenticate(username, password):
            root.destroy()
            run_dashboard(username, password)  # pass for encryption key
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    #clicks register
    def handle_register():
        username = entry_username.get()
        password = entry_password.get()
        success, msg = register(username, password)
        if success:
            messagebox.showinfo("Register", msg)
        else:
            messagebox.showerror("Error Registering", msg)

    #window styling
    root = tk.Tk()
    root.title("HashVault - Login")
    root.geometry("900x600")
    root.minsize(700, 500)
    root.configure(bg="#f0f0f5")

    #colors
    bg_main = "#ffffff"
    bg_card = "#ffffff"
    accent = "#0a0a0a"
    button_color = "#074a77"

    #styling for fonts, buttons and background
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Card.TFrame", background=bg_card)
    style.configure("TLabel", background=bg_card, font=("Bahnschrift", 14))
    style.configure("Header.TLabel", background=bg_card, font=("Bahnschrift", 28, "bold"), foreground=accent)
    style.configure("TButton", font=("Bahnschrift", 12))
    style.map("TButton",
              background=[("active", "#074a77"), ("!active", button_color)],
              foreground=[("active", "white"), ("!active", "white")])

    #background
    main_frame = tk.Frame(root, bg=bg_main)
    main_frame.pack(fill="both", expand=True)

    #center container and centering
    content = ttk.Frame(main_frame, padding=50, style="Card.TFrame")
    content.pack(fill="both", expand=True)
    inner_frame = ttk.Frame(content, padding=80, style="Card.TFrame")
    inner_frame.place(relx=0.5, rely=0.6, anchor="center")

    #heading
    ttk.Label(content, text="Welcome to HashVault", style="Header.TLabel").pack(pady=(0, 40))

    #username and password
    form_frame = ttk.Frame(content, style="Card.TFrame")
    form_frame.pack()

    ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="e", padx=15, pady=20)
    entry_username = ttk.Entry(form_frame, font=("Bahnschrift", 13), width=40)
    entry_username.grid(row=0, column=1, pady=20)

    ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=15, pady=20)
    entry_password = ttk.Entry(form_frame, show="*", font=("Bahnschrift", 13), width=40)
    entry_password.grid(row=1, column=1, pady=20)

    #login and register buttons
    btn_frame = ttk.Frame(content, style="Card.TFrame")
    btn_frame.pack(pady=30)
    ttk.Button(btn_frame, text="Login", width=20, command=handle_login).grid(row=0, column=0, padx=20)
    ttk.Button(btn_frame, text="Register", width=20, command=handle_register).grid(row=0, column=1, padx=20)

    #starts gui 
    root.mainloop()

