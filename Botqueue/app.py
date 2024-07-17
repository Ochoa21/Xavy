import tkinter as tk
from tkinter import messagebox
import requests
import pyotp
import qrcode
from PIL import Image, ImageTk
import sqlite3
import os

# Crear base de datos para almacenar usuarios
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, otp_secret TEXT)''')
conn.commit()
conn.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Filas Virtuales")

        self.logged_in_user = None

        self.create_login_interface()

    def create_login_interface(self):
        self.clear_window()

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.otp_label = tk.Label(self.root, text="OTP:")
        self.otp_label.pack()
        self.otp_entry = tk.Entry(self.root)
        self.otp_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(self.root, text="Register", command=self.show_registration_interface)
        self.register_button.pack()

    def show_registration_interface(self):
        self.clear_window()

        self.username_label = tk.Label(self.root, text="New Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="New Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.owner_key_label = tk.Label(self.root, text="Owner Key:")
        self.owner_key_label.pack()
        self.owner_key_entry = tk.Entry(self.root, show="*")
        self.owner_key_entry.pack()

        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        owner_key = self.owner_key_entry.get()

        if owner_key != "clave_temporal":
            messagebox.showerror("Error", "Invalid Owner Key")
            return

        otp_secret = pyotp.random_base32()
        totp = pyotp.TOTP(otp_secret)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, otp_secret) VALUES (?, ?, ?)", (username, password, otp_secret))
            conn.commit()
            self.show_qr(totp.provisioning_uri(username, issuer_name="Queue Manager"))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        conn.close()

    def show_qr(self, provisioning_uri):
        qr = qrcode.make(provisioning_uri)
        qr.save("otp_qr.png")
        qr_image = Image.open("otp_qr.png")
        qr_photo = ImageTk.PhotoImage(qr_image)

        self.qr_label = tk.Label(self.root, image=qr_photo)
        self.qr_label.image = qr_photo
        self.qr_label.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        otp = self.otp_entry.get()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password, otp_secret FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()

        if result and result[0] == password:
            totp = pyotp.TOTP(result[1])
            if totp.verify(otp):
                self.logged_in_user = username
                self.create_main_interface()
            else:
                messagebox.showerror("Error", "Invalid OTP")
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    def create_main_interface(self):
        self.clear_window()

        self.queue_name_label = tk.Label(self.root, text="Nombre de la Fila:")
        self.queue_name_label.pack()
        self.queue_name_entry = tk.Entry(self.root)
        self.queue_name_entry.pack()

        self.create_queue_button = tk.Button(self.root, text="Crear Fila", command=self.create_queue)
        self.create_queue_button.pack()

        self.user_label = tk.Label(self.root, text="Usuario:")
        self.user_label.pack()
        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack()

        self.add_user_button = tk.Button(self.root, text="Agregar Usuario a Fila", command=self.add_user_to_queue)
        self.add_user_button.pack()

        self.process_queue_button = tk.Button(self.root, text="Procesar Fila", command=self.process_queue)
        self.process_queue_button.pack()

        self.block_url_button = tk.Button(self.root, text="Bloquear URL", command=self.block_url)
        self.block_url_button.pack()

        self.history_button = tk.Button(self.root, text="Ver Historial", command=self.show_history)
        self.history_button.pack()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_queue(self):
        queue_name = self.queue_name_entry.get()
        messagebox.showinfo("Info", f"Queue {queue_name} created!")

    def add_user_to_queue(self):
        user = self.user_entry.get()
        messagebox.showinfo("Info", f"User {user} added to the queue!")

    def process_queue(self):
        messagebox.showinfo("Info", "Queue processed!")

    def block_url(self):
        blocked_url = self.queue_name_entry.get()
        # Aquí se debe implementar la lógica para bloquear el URL en el proxy
        messagebox.showinfo("Info", f"URL {blocked_url} blocked!")

    def show_history(self):
        messagebox.showinfo("Historial", "Aquí se mostraría el historial de URLs bloqueadas")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
