import string
import random
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3



with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
db.commit()
db.close()


class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Password Generator')
        self.master.geometry('800x800')  
        self.master.config(bg='#FADCD9')  
        self.master.resizable(True, True)  

        
        self.username = StringVar()
        self.password_len = IntVar(value=12)
        self.generated_password = StringVar()
        self.n_username = StringVar()
        self.n_generated_password = StringVar()

        
        self.configure_style()

        
        self.create_title_label()
        self.create_username_entry()
        self.create_password_length_entry()
        self.create_generate_button()
        self.create_generated_password_entry()
        self.create_copy_button()
        self.create_accept_button()
        self.create_reset_button()

    def configure_style(self):
        """Style configuration for the app"""
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 14), background='#F2F2F2', foreground='#333333')  # Very dark grey text
        style.configure('TButton', font=('Arial', 12, 'bold'), background='#F2F2F2', foreground='#333333', padding=12)
        style.configure('TEntry', font=('Arial', 14), foreground='#333333', padding=5)  # Dark text for entry fields

    def create_title_label(self):
        """Creates the title label"""
        title_label = ttk.Label(self.master, text=": PASSWORD GENERATOR :", font=('Arial', 24, 'bold'), foreground='#E67E22', background='#F2F2F2')
        title_label.grid(row=0, column=0, columnspan=3, pady=30, padx=20)

    def create_username_entry(self):
        """Creates the username input section"""
        user_label = ttk.Label(self.master, text="Enter Username:")
        user_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)
        self.username_entry = ttk.Entry(self.master, textvariable=self.n_username, width=40)
        self.username_entry.grid(row=1, column=1, columnspan=2, pady=10, padx=20)

    def create_password_length_entry(self):
        """Creates the password length input section"""
        length_label = ttk.Label(self.master, text="Password Length:")
        length_label.grid(row=2, column=0, padx=20, pady=10, sticky=W)
        self.length_entry = ttk.Entry(self.master, textvariable=self.password_len, width=10)
        self.length_entry.grid(row=2, column=1, pady=10, padx=20)

    def create_generate_button(self):
        """Creates the generate password button"""
        generate_button = ttk.Button(self.master, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=3, column=0, columnspan=3, pady=20)

    def create_generated_password_entry(self):
        """Creates the generated password display section"""
        generated_password_label = ttk.Label(self.master, text="Generated Password:")
        generated_password_label.grid(row=4, column=0, padx=20, pady=10, sticky=W)
        self.generated_password_entry = ttk.Entry(self.master, textvariable=self.generated_password, width=40, foreground='#C0392B', font=('Arial', 14, 'italic'))
        self.generated_password_entry.grid(row=4, column=1, columnspan=2, pady=10, padx=20)

    def create_copy_button(self):
        """Creates the copy to clipboard button"""
        copy_button = ttk.Button(self.master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_button.grid(row=5, column=0, columnspan=3, pady=20)

    def create_accept_button(self):
        """Creates the save password button"""
        accept_button = ttk.Button(self.master, text="Save Password", command=self.accept_fields)
        accept_button.grid(row=6, column=0, columnspan=3, pady=10)

    def create_reset_button(self):
        """Creates the reset button"""
        reset_button = ttk.Button(self.master, text="Reset", command=self.reset_fields)
        reset_button.grid(row=7, column=0, columnspan=3, pady=10)

    def generate_password(self):
        """Generate a random password based on user input"""
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()?!"
        numbers = "1234567890"
        length = self.password_len.get()

        # Validate inputs
        if not self.n_username.get():
            messagebox.showerror("Error", "Username cannot be empty")
            return
        
        if length < 6:
            messagebox.showerror("Error", "Password length must be at least 6")
            return
        
        
        all_chars = upper + lower + chars + numbers
        password = "".join(random.sample(all_chars, length))
        self.generated_password.set(password)

    def copy_to_clipboard(self):
        """Copy the generated password to clipboard"""
        password = self.generated_password.get()
        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy")

    def accept_fields(self):
        """Save the username and generated password to the database"""
        username = self.n_username.get()
        password = self.generated_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required")
            return

        
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (username, password))
            db.commit()
        messagebox.showinfo("Success", "Password saved successfully!")

    def reset_fields(self):
        """Reset all fields"""
        self.username_entry.delete(0, END)
        self.length_entry.delete(0, END)
        self.generated_password_entry.delete(0, END)



if __name__ == '__main__':
    root = Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
