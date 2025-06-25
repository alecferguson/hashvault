import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from utils.encryption import derive_key, encrypt_service_password, decrypt_service_password
from utils.credential_utilities import load_user_credentials, save_user_credentials, get_user_file


def run_dashboard(username="User", master_password=""):
    #derive encryption key from users login password
    encryption_key = derive_key(master_password)

    #main dashboard
    root = tk.Tk()
    root.title("HashVault - Dashboard")
    root.geometry("1000x600")
    root.configure(bg="#f0f0f5")

    #styling colors
    bg_main = "#f0f0f5"
    accent = "#0a0a0a"
    button_color = "#074a77"

    #style for background, buttons, headers
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dashboard.TFrame", background=bg_main)
    style.configure("Header.TLabel", font=("Bahnschrift", 24, "bold"), background=bg_main, foreground=accent)
    style.configure("TButton", font=("Bahnschrift", 11))
    style.map("TButton",
              background=[("active", "#2980b9"), ("!active", button_color)],
              foreground=[("active", "white"), ("!active", "white")])

    #main container for all items
    main_frame = ttk.Frame(root, padding=30, style="Dashboard.TFrame")
    main_frame.pack(fill="both", expand=True)

    #header
    ttk.Label(main_frame, text=f"Welcome, {username}", style="Header.TLabel").pack(anchor="w", pady=(0, 20))

    #table to show all the details of the services and related details
    columns = ("Service", "Username", "Password", "RealPassword", "Action")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    #loading user credentials
    credentials = load_user_credentials(username)
    for cred in credentials:
        service = cred["service"]
        user = cred["username"]
        encrypted_password = cred["password"]
        tree.insert("", "end", values=(service, user, "********", encrypted_password, "Show"))
    
    #columns 
    for col in columns:
        if col == "RealPassword":
            tree.column(col, width=0, stretch=False) #hide password
            tree.heading(col, text="")
        else:
            tree.column(col, anchor="center", width=180)
            tree.heading(col, text=col)

    tree.pack(fill="both", expand=True)

    # buttons for logout and adding 
    btn_frame = tk.Frame(main_frame, bg=bg_main)
    btn_frame.pack(pady=20)
    ttk.Button(btn_frame, text="Add Credential", command=lambda: open_add_popup(root, tree)).grid(row=0, column=0, padx=15)
    ttk.Button(btn_frame, text="Logout", command=lambda: logout(root)).grid(row=0, column=1, padx=15)

    #logs out and back to login screen
    def logout(current_window):
        current_window.destroy()
        from .login import run_login
        run_login()

    #add credential pop up
    def open_add_popup(parent, tree):
        popup = tk.Toplevel(parent)
        popup.title("Add Credential")
        popup.geometry("400x300")
        popup.configure(bg=bg_main)
        popup.after(1, lambda: popup.grab_set())

        style.configure("Popup.TLabel", background=bg_main, font=("Bahnschrift", 12))
        style.configure("Popup.TButton", font=("Bahnschrift", 11))

        #inputs for service, username, password 
        ttk.Label(popup, text="Service:", style="Popup.TLabel").pack(pady=(20, 5))
        entry_service = ttk.Entry(popup, width=40)
        entry_service.pack()

        ttk.Label(popup, text="Username:", style="Popup.TLabel").pack(pady=(20, 5))
        entry_username = ttk.Entry(popup, width=40)
        entry_username.pack()

        ttk.Label(popup, text="Password:", style="Popup.TLabel").pack(pady=(20, 5))
        entry_password = ttk.Entry(popup, width=40, show="*")
        entry_password.pack()

        #saves the info and display
        def handle_submit():
            service = entry_service.get()
            uname = entry_username.get()
            pwd = entry_password.get()

            if service and uname and pwd:
                encrypted = encrypt_service_password(encryption_key, pwd)
                tree.insert("", "end", values=(service, uname, "********", encrypted, "Show"))
                # Save to file
                credentials = load_user_credentials(username)
                credentials.append({
                    "service" : service,
                    "username" : uname,
                    "password" : encrypted
                })
                save_user_credentials(username, credentials)
                popup.destroy()

        #submit and cancel buttons
        btn_frame = tk.Frame(popup, bg=bg_main)
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Submit", style="Popup.TButton", command=handle_submit).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancel", style="Popup.TButton", command=popup.destroy).grid(row=0, column=1, padx=10)

    #password popup with needing key input
    def show_password_popup(item_id):
        values = tree.item(item_id, "values")
        service, username, _, real_password, _ = values

        popup = tk.Toplevel()
        popup.title("Enter Decryption Key")
        popup.geometry("400x200")
        popup.configure(bg=bg_main)
        popup.after(1, lambda: popup.grab_set())

        ttk.Label(popup, text=f"Enter decryption key to view password for {service}:", font=("Bahnschrift", 12),
                  background=bg_main).pack(pady=20)
        entry_key = ttk.Entry(popup, width=30, show="*")
        entry_key.pack()

        #when the decrypt is clicked it shows password
        def reveal():
            key = entry_key.get()
            try:
                plain = decrypt_service_password(encryption_key, real_password)
                tree.set(item_id, column="Password", value=plain)
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Decryption failed", str(e))

        ttk.Button(popup, text="Decrypt", command=reveal).pack(pady=20)

    #if show is clicked
    def on_tree_click(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            col = tree.identify_column(event.x)
            if col == "#5":  # Show button
                row_id = tree.identify_row(event.y)
                if row_id:
                    show_password_popup(row_id)

    #manage click
    tree.bind("<Button-1>", on_tree_click)

    root.mainloop()