import tkinter as tk

def get_home_stats(products, sales_history):
    total_products = len(products)
    purchase_counts = {}

    # Count total purchases per product name
    for sale in sales_history:
        for batch, name, qty, sell_price, total in sale["items"]:
            purchase_counts[name] = purchase_counts.get(name, 0) + int(qty)

    if purchase_counts:
        most_bought = max(purchase_counts, key=purchase_counts.get)
        most_bought_qty = purchase_counts[most_bought]
        most_bought_text = f"{most_bought} ({most_bought_qty} sold)"
    else:
        most_bought_text = "No sales yet"

    total_profit = 0.0

    # Calculate total profit
    for sale in sales_history:
        for batch, name, qty, sell_price, total in sale["items"]:
            cost_price = None
            # Find the cost price of the product by batch
            for p in products:
                if p[0] == batch:
                    cost_price = p[2]
                    break
            
            # Debug print to see the values being processed
            print(f"Processing sale item -> Batch: {batch}, Name: {name}, Qty: {qty}, Sell Price: {sell_price}, Cost Price: {cost_price}")

            if cost_price is not None:
                try:
                    cp = float(cost_price)
                    sp = float(sell_price)
                    q = int(qty)
                    profit = (sp - cp) * q
                    total_profit += profit
                    print(f"Profit for this item: {profit}")
                except Exception as e:
                    print(f"Error converting price or quantity to number: {e}")
            else:
                print(f"Cost price not found for batch '{batch}'")

    return total_products, most_bought_text, total_profit

def show_home_page(content_frame, products, sales_history):
    # Clear content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="🏠 Grocery Store Dashboard", font=("Arial", 18, "bold")).pack(pady=20)

    total_products, most_bought, total_profit = get_home_stats(products, sales_history)

    stats_frame = tk.Frame(content_frame, bg="#ffffff", bd=2, relief="groove")
    stats_frame.pack(pady=20, ipadx=20, ipady=20)

    tk.Label(stats_frame, text=f"📦 Total Products Listed: {total_products}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(stats_frame, text=f"🔥 Most Purchased Product: {most_bought}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(stats_frame, text=f"💰 Total Profit: ₱{total_profit:.2f}", font=("Arial", 14)).pack(anchor="w", pady=5)

    tk.Label(content_frame, text="Use the menu on the left to manage your store.", font=("Arial", 12, "italic")).pack(pady=10)
