import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import requests

class GenApp:
    def __init__(self, master):
        # Theme setup
        self.master = master
        self.master.title("Key Gen App by Void")
        
        # Key Generation Frame
        self.gen_frame = ttk.LabelFrame(master, text="Key Generation", padding=(10, 5))
        self.gen_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Label(self.gen_frame, text="Key Length:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.key_length = ttk.Entry(self.gen_frame, width=5)
        self.key_length.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.key_length.insert(0, "8")

        durations = ['1d', '1w', '2w', '1m', 'infinite']
        self.duration_var = tk.StringVar(value=durations[0])
        self.duration_dropdown = ttk.Combobox(self.gen_frame, values=durations, textvariable=self.duration_var)
        self.duration_dropdown.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(self.gen_frame, text="Key Duration:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.generate_btn = ttk.Button(self.gen_frame, text="Generate Key", command=self.generate_key)
        self.generate_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.generated_key_label = ttk.Label(self.gen_frame, text="Generated Key:")
        self.generated_key_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.generated_key_value = ttk.Label(self.gen_frame, text="")
        self.generated_key_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Key Management Frame
        self.mgmt_frame = ttk.LabelFrame(master, text="Key Management", padding=(10, 5))
        self.mgmt_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

        ttk.Label(self.mgmt_frame, text="Select Key:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.keys_list = self.fetch_keys()
        self.key_var = tk.StringVar()
        self.key_dropdown = ttk.Combobox(self.mgmt_frame, values=self.keys_list, textvariable=self.key_var)
        self.key_dropdown.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.extend_btn = ttk.Button(self.mgmt_frame, text="Extend Key Time", command=self.extend_key_time)
        self.extend_btn.grid(row=1, column=0, padx=5, pady=5)
        self.remove_time_btn = ttk.Button(self.mgmt_frame, text="Remove Key Time", command=self.remove_key_time)
        self.remove_time_btn.grid(row=1, column=1, padx=5, pady=5)
        self.delete_btn = ttk.Button(self.mgmt_frame, text="Delete Key", command=self.delete_key)
        self.delete_btn.grid(row=2, column=0, padx=5, pady=10)
        self.check_time_left_btn = ttk.Button(self.mgmt_frame, text="Check Time Left", command=self.check_time_left)
        self.check_time_left_btn.grid(row=2, column=1, padx=5, pady=10)

    def fetch_keys(self):
        try:
            response = requests.get("http://localhost:5000/keys")
            if response.status_code == 200:
                keys = [key_obj["key"] for key_obj in response.json()["keys"]]
                return keys
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch keys from the backend.")
            return []

    def refresh_keys(self):
        self.keys_list = self.fetch_keys()
        self.key_dropdown['values'] = self.keys_list
        if self.key_var.get() not in self.keys_list:
            self.key_var.set('')

    def generate_key(self):
        try:
            key_length = int(self.key_length.get())
            duration = self.duration_var.get()
            response = requests.post("http://localhost:5000/generate", json={'length': key_length, 'duration': duration})
            if response.status_code == 200:
                self.generated_key_value["text"] = response.json()["key"]
                self.refresh_keys()
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to generate a key.")
            
    def extend_key_time(self):
        key = self.key_var.get()
        if not key:
            messagebox.showwarning("Warning", "Please select a key first.")
            return
        try:
            response = requests.post(f"http://localhost:5000/extend/{key}")
            if response.status_code == 200:
                messagebox.showinfo("Success", "Key time extended.")
                self.refresh_keys()
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to extend key time.")

    def remove_key_time(self):
        key = self.key_var.get()
        if not key:
            messagebox.showwarning("Warning", "Please select a key first.")
            return
        try:
            response = requests.post(f"http://localhost:5000/remove-time/{key}")
            if response.status_code == 200:
                messagebox.showinfo("Success", "Key time reduced.")
                self.refresh_keys()
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to reduce key time.")

    def delete_key(self):
        key = self.key_var.get()
        if not key:
            messagebox.showwarning("Warning", "Please select a key first.")
            return
        try:
            response = requests.delete(f"http://localhost:5000/delete/{key}")
            if response.status_code == 200:
                messagebox.showinfo("Success", "Key deleted.")
                self.refresh_keys()
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to delete key.")

    def check_time_left(self):
        key = self.key_var.get()
        if not key:
            messagebox.showwarning("Warning", "Please select a key first.")
            return
        try:
            response = requests.get(f"http://localhost:5000/time-left/{key}")
            if response.status_code == 200:
                time_left = response.json().get("time_left", "")
                messagebox.showinfo("Time Left", time_left)
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to check time left on the key.")

if __name__ == '__main__':
    root = ThemedTk(theme="black")
    app = GenApp(root)
    root.mainloop()
