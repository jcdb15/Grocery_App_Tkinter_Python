# Add_Product.py
import tkinter as tk
from tkinter import messagebox

def show_add_product_page(content_frame, products):
    # Clear previous widgets
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Add Product", font=("Arial", 14, "bold")).pack(pady=10)

    form_frame = tk.Frame(content_frame)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Batch Code:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    batch_entry = tk.Entry(form_frame)
    batch_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Product Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Cost Price:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    price_entry = tk.Entry(form_frame)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Sell Price:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    sell_entry = tk.Entry(form_frame)
    sell_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Stocks:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    stocks_entry = tk.Entry(form_frame)
    stocks_entry.grid(row=4, column=1, padx=5, pady=5)

    def add_product():
        batch = batch_entry.get().strip()
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        sell_price = sell_entry.get().strip()
        stocks = stocks_entry.get().strip()

        if not batch or not name or not price or not sell_price or not stocks:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        # Check duplicate batch code
        if any(p[0] == batch for p in products):
            messagebox.showerror("Duplicate Batch Code", "Batch code already exists.")
            return

        try:
            price = float(price)
            sell_price = float(sell_price)
            stocks = int(stocks)
        except ValueError:
            messagebox.showerror("Invalid Data", "Price/Sell Price must be numbers, Stocks must be an integer.")
            return

        products.append((batch, name, price, sell_price, stocks))
        messagebox.showinfo("Success", f"Product '{name}' added.")
        batch_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        sell_entry.delete(0, tk.END)
        stocks_entry.delete(0, tk.END)

    tk.Button(content_frame, text="Add Product", bg="#27AE60", fg="white", command=add_product).pack(pady=5)
