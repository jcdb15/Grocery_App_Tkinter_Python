# Product_List.py
import tkinter as tk
from tkinter import ttk

def show_product_list_page(content_frame, products):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Product List", font=("Arial", 14, "bold")).pack(pady=10)

    table = ttk.Treeview(
        content_frame,
        columns=("Batch", "Name", "Price", "Sell", "Stocks"),
        show="headings",
        height=15
    )
    table.heading("Batch", text="Batch Code")
    table.heading("Name", text="Product Name")
    table.heading("Price", text="Cost Price")
    table.heading("Sell", text="Sell Price")
    table.heading("Stocks", text="Stocks")

    for col in ("Batch", "Name", "Price", "Sell", "Stocks"):
        table.column(col, width=100)

    for p in products:
        table.insert("", tk.END, values=p)

    table.pack(fill="both", expand=True)
