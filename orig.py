import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --- Data Storage ---
products = []
sales_history = []

# --- Main Functions ---
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# --- Stats Calculations ---
def get_home_stats():
    # 1. Total products
    total_products = len(products)

    # 2. Most purchased product
    purchase_counts = {}
    for sale in sales_history:
        for batch, name, qty, sell_price, total in sale["items"]:
            if name not in purchase_counts:
                purchase_counts[name] = 0
            purchase_counts[name] += qty
    if purchase_counts:
        most_bought = max(purchase_counts, key=purchase_counts.get)
        most_bought_qty = purchase_counts[most_bought]
        most_bought_text = f"{most_bought} ({most_bought_qty} sold)"
    else:
        most_bought_text = "No sales yet"

    # 3. Total profit
    total_profit = 0
    for sale in sales_history:
        for batch, name, qty, sell_price, total in sale["items"]:
            # Find cost price
            cost_price = None
            for p in products:
                if p[0] == batch:
                    cost_price = p[2]
                    break
            if cost_price is not None:
                total_profit += (sell_price - cost_price) * qty

    return total_products, most_bought_text, total_profit

# Home Page
def show_home_page():
    clear_content()
    tk.Label(content_frame, text="🏠 Grocery Store Dashboard", font=("Arial", 18, "bold")).pack(pady=20)

    total_products, most_bought, total_profit = get_home_stats()

    stats_frame = tk.Frame(content_frame, bg="#ffffff", bd=2, relief="groove")
    stats_frame.pack(pady=20, ipadx=20, ipady=20)

    tk.Label(stats_frame, text=f"📦 Total Products Listed: {total_products}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(stats_frame, text=f"🔥 Most Purchased Product: {most_bought}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(stats_frame, text=f"💰 Total Profit: ₱{total_profit:.2f}", font=("Arial", 14)).pack(anchor="w", pady=5)

    tk.Label(content_frame, text="Use the menu on the left to manage your store.", font=("Arial", 12, "italic")).pack(pady=10)

# Add Product
def show_add_product_page():
    clear_content()
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

        try:
            price = float(price)
            sell_price = float(sell_price)
            stocks = int(stocks)
        except ValueError:
            messagebox.showerror("Invalid Data", "Price/Sell Price must be numbers, Stocks must be an integer.")
            return

        products.append((batch, name, price, sell_price, stocks))
        batch_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        sell_entry.delete(0, tk.END)
        stocks_entry.delete(0, tk.END)

    tk.Button(content_frame, text="Add Product", bg="#27AE60", fg="white", command=add_product).pack(pady=5)

# Product List
def show_product_list_page():
    clear_content()
    tk.Label(content_frame, text="Product List", font=("Arial", 14, "bold")).pack(pady=10)

    table = ttk.Treeview(
        content_frame,
        columns=("Batch", "Name", "Price", "Sell", "Stocks"),
        show="headings",
        height=10
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

    table.pack()

# Sell Products
def show_sell_products_page():
    clear_content()
    tk.Label(content_frame, text="Sell Products", font=("Arial", 14, "bold")).pack(pady=10)

    if not products:
        tk.Label(content_frame, text="No products available to sell. Add products first.").pack(pady=20)
        return

    selector_frame = tk.Frame(content_frame)
    selector_frame.pack(pady=5)

    tk.Label(selector_frame, text="Select Product:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    product_display = [p[1] for p in products]  # product names only
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

    order_items = []  # list of tuples: (prod_index, qty)

    total_amount_var = tk.StringVar(value="₱0.00")
    total_frame = tk.Frame(content_frame)
    total_frame.pack(pady=5, anchor="e")
    tk.Label(total_frame, text="Total Amount: ", font=("Arial", 12, "bold")).pack(side="left")
    tk.Label(total_frame, textvariable=total_amount_var, font=("Arial", 12, "bold")).pack(side="left")

    # Customer money input and change display
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
        change_var.set("₱0.00")  # reset change when total updates

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

        # Add to order_items list
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

        # Check if change is calculated and customer money covers total
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
            change = 0.0  # fallback if somehow invalid

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
        # Refresh Sell Products page to clear order and update stocks
        show_sell_products_page()

    tk.Button(selector_frame, text="Add to Order", bg="#3498DB", fg="white", command=add_to_order).grid(row=3, column=1, pady=5, sticky="w")

    button_frame = tk.Frame(content_frame)
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Delete Selected", bg="#e74c3c", fg="white", command=delete_from_order).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Calculate Change", bg="#3498DB", fg="white", command=calculate_change).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Finalize Sale", bg="#E67E22", fg="white", command=finalize_order).grid(row=0, column=2, padx=5)

# Sales History
def show_sales_history_page():
    clear_content()
    tk.Label(content_frame, text="Sales History", font=("Arial", 14, "bold")).pack(pady=10)

    if not sales_history:
        tk.Label(content_frame, text="No sales have been made yet.").pack(pady=20)
        return

    history_table = ttk.Treeview(
        content_frame,
        columns=("Date", "Batch", "Name", "Qty", "Sell Price", "Total", "Customer Money", "Change"),
        show="headings",
        height=10
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

# Settings Page (placeholder)
def show_settings_page():
    clear_content()
    tk.Label(content_frame, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(content_frame, text="Settings page is under construction.").pack(pady=20)

# --- GUI Setup ---
root = tk.Tk()
root.title("Grocery Store Dashboard")
root.geometry("800x600")

sidebar = tk.Frame(root, width=200, bg="#2C3E50")
sidebar.pack(side="left", fill="y")

tk.Button(sidebar, text="Home", command=show_home_page, width=20, bg="#1ABC9C", fg="white").pack(pady=10)
tk.Button(sidebar, text="Add Product", command=show_add_product_page, width=20, bg="#27AE60", fg="white").pack(pady=10)
tk.Button(sidebar, text="Product List", command=show_product_list_page, width=20, bg="#2980B9", fg="white").pack(pady=10)
tk.Button(sidebar, text="Sell Products", command=show_sell_products_page, width=20, bg="#E67E22", fg="white").pack(pady=10)
tk.Button(sidebar, text="Sales History", command=show_sales_history_page, width=20, bg="#9b59b6", fg="white").pack(pady=10)
tk.Button(sidebar, text="Settings", command=show_settings_page, width=20, bg="#34495E", fg="white").pack(pady=10)

content_frame = tk.Frame(root, bg="#ECF0F1")
content_frame.pack(side="left", fill="both", expand=True)

show_home_page()

root.mainloop()
