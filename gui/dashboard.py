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
    columns = ("Service", "Username", "Password", "Action", "Delete")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    #loading user credentials
    credentials = load_user_credentials(username)
    for cred in credentials:
        service = cred["service"]
        user = cred["username"]
        encrypted_password = cred["password"]
        tree.insert("", "end", values=(service, user, "********", "Show", "Delete"))
    
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
            service = entry_service.get().strip()
            uname = entry_username.get().strip()
            pwd = entry_password.get().strip()

            # Input validation
            if not service or not uname or not pwd:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                encrypted = encrypt_service_password(encryption_key, pwd)
                
                # Save to file first
                credentials = load_user_credentials(username)
                credentials.append({
                    "service": service,
                    "username": uname,
                    "password": encrypted
                })
                save_user_credentials(username, credentials)
                
                # add to tree with correct column order: Service, Username, Password, Action, Delete
                tree.insert("", "end", values=(service, uname, "********", "Show", "Delete"))
                
                popup.destroy()
                messagebox.showinfo("Success", "Credential added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save credential: {str(e)}")

        #submit and cancel buttons
        btn_frame = tk.Frame(popup, bg=bg_main)
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Submit", style="Popup.TButton", command=handle_submit).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancel", style="Popup.TButton", command=popup.destroy).grid(row=0, column=1, padx=10)

    def toggle_password(item_id):
        values = tree.item(item_id, "values")
        service, user, current_password, action, delete = values
        
        if current_password == "********":
            # Show password - decrypt from file
            credentials = load_user_credentials(username)
            for cred in credentials:
                if cred["service"] == service and cred["username"] == user:
                    decrypted = decrypt_service_password(encryption_key, cred["password"])
                    tree.set(item_id, column="Password", value=decrypted)
                    tree.set(item_id, column="Action", value="Hide")  # ← Changes button to "Hide"
                    break
        else:
            # Hide password
            tree.set(item_id, column="Password", value="********")
            tree.set(item_id, column="Action", value="Show")  # Changes button back to "Show"
    
    #delete credential function
    def delete_credential(item_id):
        values = tree.item(item_id, "values")
        service, user = values[0], values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete credential for {service}?"):
            credentials = load_user_credentials(username)
            credentials = [c for c in credentials if not (c["service"] == service and c["username"] == user)]
            save_user_credentials(username, credentials)
            tree.delete(item_id)
            messagebox.showinfo("Success", "Credential deleted successfully!")

    #if show is clicked
    def on_tree_click(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            col = tree.identify_column(event.x)
            row_id = tree.identify_row(event.y)
            if row_id:
                if col == "#4":  # Show/Hide button
                    toggle_password(row_id)
                elif col == "#5":  # Delete button  ← NEW
                    delete_credential(row_id)
    #manage click
    tree.bind("<Button-1>", on_tree_click)
    root.mainloop()