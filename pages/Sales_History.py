# Sales_History.py
import tkinter as tk
from tkinter import ttk

def show_sales_history_page(content_frame, sales_history):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Sales History", font=("Arial", 14, "bold")).pack(pady=10)

    if not sales_history:
        tk.Label(content_frame, text="No sales have been made yet.").pack(pady=20)
        return

    history_table = ttk.Treeview(
        content_frame,
        columns=("Date", "Batch", "Name", "Qty", "Sell Price", "Total", "Customer Money", "Change"),
        show="headings",
        height=15
    )
    history_table.heading("Date", text="Date")
    history_table.heading("Batch", text="Batch")
    history_table.heading("Name", text="Product Name")
    history_table.heading("Qty", text="Qty")
    history_table.heading("Sell Price", text="Sell Price")
    history_table.heading("Total", text="Total")
    history_table.heading("Customer Money", text="Customer Money")
    history_table.heading("Change", text="Change")

    for col in ("Date", "Batch", "Name", "Qty", "Sell Price", "Total", "Customer Money", "Change"):
        history_table.column(col, width=100)

    for sale in sales_history:
        customer_money = sale.get("customer_money", 0)
        change = sale.get("change", 0)
        for batch, name, qty, sell_price, total in sale["items"]:
            history_table.insert(
                "",
                tk.END,
                values=(sale["date"], batch, name, qty, sell_price, total, f"₱{customer_money:.2f}", f"₱{change:.2f}")
            )

    history_table.pack(fill="both", expand=True)
