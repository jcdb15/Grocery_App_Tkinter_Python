# Sell_Products.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def show_sell_products_page(content_frame, products, sales_history):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Sell Products", font=("Arial", 14, "bold")).pack(pady=10)

    if not products:
        tk.Label(content_frame, text="No products available to sell. Add products first.").pack(pady=20)
        return

    selector_frame = tk.Frame(content_frame)
    selector_frame.pack(pady=5)

    tk.Label(selector_frame, text="Select Product:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    product_display = [p[1] for p in products]
    product_var = tk.StringVar(value=product_display[0])
    product_combo = ttk.Combobox(selector_frame, textvariable=product_var, values=product_display, state="readonly", width=40)
    product_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(selector_frame, text="Enter Batch Code:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    batch_code_entry = tk.Entry(selector_frame)
    batch_code_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def select_by_batch():
        batch_code = batch_code_entry.get().strip()
        if not batch_code:
            messagebox.showwarning("Input Needed", "Please enter a batch code.")
            return
        index = next((i for i, p in enumerate(products) if p[0] == batch_code), None)
        if index is None:
            messagebox.showerror("Not Found", f"No product found with batch code '{batch_code}'.")
        else:
            product_var.set(products[index][1])
            messagebox.showinfo("Product Selected", f"Selected product: {products[index][1]}")

    tk.Button(selector_frame, text="Select by Batch Code", command=select_by_batch).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(selector_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    qty_entry = tk.Entry(selector_frame)
    qty_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    order_frame = tk.Frame(content_frame)
    order_frame.pack(pady=10)
    order_table = ttk.Treeview(order_frame, columns=("Product", "Quantity", "Price", "Total"), show="headings", height=8)
    order_table.heading("Product", text="Product")
    order_table.heading("Quantity", text="Quantity")
    order_table.heading("Price", text="Unit Price")
    order_table.heading("Total", text="Total Price")
    order_table.column("Product", width=200)
    order_table.column("Quantity", width=80, anchor="center")
    order_table.column("Price", width=80, anchor="center")
    order_table.column("Total", width=100, anchor="center")
    order_table.pack()

    order_items = []

    total_amount_var = tk.StringVar(value="₱0.00")
    total_frame = tk.Frame(content_frame)
    total_frame.pack(pady=5, anchor="e")
    tk.Label(total_frame, text="Total Amount: ", font=("Arial", 12, "bold")).pack(side="left")
    tk.Label(total_frame, textvariable=total_amount_var, font=("Arial", 12, "bold")).pack(side="left")

    payment_frame = tk.Frame(content_frame)
    payment_frame.pack(pady=10, anchor="e")

    tk.Label(payment_frame, text="Customer Money: ₱", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    customer_money_entry = tk.Entry(payment_frame, width=15)
    customer_money_entry.grid(row=0, column=1, padx=5)

    change_var = tk.StringVar(value="₱0.00")
    tk.Label(payment_frame, text="Change: ", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="e")
    change_label = tk.Label(payment_frame, textvariable=change_var, font=("Arial", 12, "bold"))
    change_label.grid(row=1, column=1, sticky="w", padx=5)

    def update_total_amount():
        total = 0
        for prod_index, qty in order_items:
            sell_price = products[prod_index][3]
            total += sell_price * qty
        total_amount_var.set(f"₱{total:.2f}")
        change_var.set("₱0.00")

    def add_to_order():
        qty_text = qty_entry.get().strip()
        if not qty_text.isdigit():
            messagebox.showerror("Invalid", "Quantity must be a positive integer.")
            return
        qty = int(qty_text)
        if qty <= 0:
            messagebox.showerror("Invalid", "Quantity must be greater than zero.")
            return

        try:
            prod_index = product_display.index(product_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid product selection.")
            return

        batch, name, price, sell_price, stocks = products[prod_index]
        if qty > stocks:
            messagebox.showerror("Not enough stock", f"Only {stocks} in stock for {name}.")
            return

        order_items.append((prod_index, qty))
        order_table.insert("", tk.END, values=(name, qty, f"₱{sell_price:.2f}", f"₱{sell_price * qty:.2f}"))
        qty_entry.delete(0, tk.END)
        update_total_amount()

    def delete_from_order():
        selected = order_table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select an item to delete from the order.")
            return
        for item in selected:
            idx = order_table.index(item)
            order_items.pop(idx)
            order_table.delete(item)
        update_total_amount()

    def calculate_change():
        total_str = total_amount_var.get().replace("₱", "").strip()
        try:
            total = float(total_str)
            customer_money = float(customer_money_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for customer money.")
            return

        if customer_money < total:
            messagebox.showerror("Insufficient Money", f"Customer money (₱{customer_money:.2f}) is less than total amount (₱{total:.2f}).")
            return

        change = customer_money - total
        change_var.set(f"₱{change:.2f}")

    def finalize_order():
        if not order_items:
            messagebox.showwarning("Empty Order", "No items in the order.")
            return

        total_str = total_amount_var.get().replace("₱", "").strip()
        try:
            total = float(total_str)
            customer_money = float(customer_money_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for customer money.")
            return

        if customer_money < total:
            messagebox.showerror("Insufficient Money", "Customer money is less than total amount. Please calculate change first.")
            return

        change_str = change_var.get().replace("₱", "").strip()
        try:
            change = float(change_str)
        except ValueError:
            change = 0.0

        sale_record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": [],
            "customer_money": customer_money,
            "change": change
        }

        for prod_index, qty in order_items:
            batch, name, price, sell_price, stocks = products[prod_index]
            products[prod_index] = (batch, name, price, sell_price, stocks - qty)
            sale_record["items"].append((batch, name, qty, sell_price, qty * sell_price))

        sales_history.append(sale_record)
        messagebox.showinfo("Sale Completed", "All items sold successfully.")
        # Reload page to clear order and update stocks
        show_sell_products_page(content_frame, products, sales_history)

    tk.Button(selector_frame, text="Add to Order", bg="#3498DB", fg="white", command=add_to_order).grid(row=3, column=1, pady=5, sticky="w")

    button_frame = tk.Frame(content_frame)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Delete Selected", bg="#e74c3c", fg="white", command=delete_from_order).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Calculate Change", bg="#3498DB", fg="white", command=calculate_change).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Finalize Sale", bg="#E67E22", fg="white", command=finalize_order).grid(row=0, column=2, padx=5)
