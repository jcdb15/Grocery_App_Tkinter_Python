import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Sample data
products = [
    ("B001", "Apples", 30.0),
    ("B002", "Bananas", 10.0),
    ("B003", "Carrots", 20.0),
    ("B004", "Dates", 50.0),
    ("B005", "Eggplants", 15.0),
    ("B006", "Figs", 40.0),
    ("B007", "Grapes", 35.0),
    ("B008", "Honeydew", 25.0),
    ("B009", "Indian Fig", 45.0),
    ("B010", "Jackfruit", 55.0),
]

sales_history = [
    {
        "items": [
            ("B001", "Apples", 5, 50.0, 250.0),
            ("B002", "Bananas", 10, 15.0, 150.0),
            ("B006", "Figs", 3, 70.0, 210.0),
            ("B007", "Grapes", 7, 60.0, 420.0),
        ]
    },
    {
        "items": [
            ("B003", "Carrots", 8, 30.0, 240.0),
            ("B001", "Apples", 2, 50.0, 100.0),
            ("B004", "Dates", 1, 70.0, 70.0),
            ("B010", "Jackfruit", 1, 80.0, 80.0),
        ]
    },
    {
        "items": [
            ("B005", "Eggplants", 20, 25.0, 500.0),
            ("B008", "Honeydew", 4, 40.0, 160.0),
            ("B009", "Indian Fig", 5, 65.0, 325.0),
        ]
    },
]

def get_home_stats(products, sales_history):
    total_products = len(products)
    purchase_counts = {}
    profit_per_product = {}

    for sale in sales_history:
        for batch, name, qty, sell_price, total in sale["items"]:
            qty = int(qty)
            purchase_counts[name] = purchase_counts.get(name, 0) + qty

            cost_price = None
            for p in products:
                if p[0] == batch:
                    cost_price = p[2]
                    break

            if cost_price is not None:
                try:
                    cp = float(cost_price)
                    sp = float(sell_price)
                    profit = (sp - cp) * qty
                    profit_per_product[name] = profit_per_product.get(name, 0) + profit
                except Exception as e:
                    print(f"Error: {e}")

    if purchase_counts:
        most_bought = max(purchase_counts, key=purchase_counts.get)
        most_bought_qty = purchase_counts[most_bought]
        most_bought_text = f"{most_bought} ({most_bought_qty} sold)"
    else:
        most_bought_text = "No sales yet"

    total_profit = sum(profit_per_product.values())
    return total_products, most_bought_text, total_profit, profit_per_product

def show_home_page(content_frame, products, sales_history):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="🏠 Grocery Store Dashboard", font=("Arial", 18, "bold")).pack(pady=20)

    total_products, most_bought, total_profit, profit_per_product = get_home_stats(products, sales_history)

    stats_frame = tk.Frame(content_frame, bg="#ffffff", bd=2, relief="groove")
    stats_frame.pack(pady=20, ipadx=20, ipady=20)

    tk.Label(stats_frame, text=f"📦 Total Products Listed: {total_products}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(stats_frame, text=f"🔥 Most Purchased Product: {most_bought}", font=("Arial", 14)).pack(anchor="w", pady=5)
    tk.Label(stats_frame, text=f"💰 Total Profit: ₱{total_profit:.2f}", font=("Arial", 14)).pack(anchor="w", pady=5)

    if profit_per_product:
        fig, ax = plt.subplots(figsize=(6, 6))
        labels = list(profit_per_product.keys())
        sizes = list(profit_per_product.values())

        wedges, texts = ax.pie(
            sizes,
            labels=None,          # No labels outside
            autopct=None,         # No % on slices
            startangle=140,
            wedgeprops=dict(width=0.6, edgecolor='w')  # Donut style with white edges
        )

        ax.set_title("Profit Distribution by Product")

        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        tooltip = tk.Toplevel(content_frame)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        tooltip_label = tk.Label(
            tooltip, text="", bg="yellow", relief="solid", borderwidth=1,
            font=("Arial", 10))
        tooltip_label.pack()

        def on_motion(event):
            if event.x is None or event.y is None:
                tooltip.withdraw()
                return

            # event.x, event.y are mouse coords relative to canvas in pixels
            for i, wedge in enumerate(wedges):
                if wedge.contains_point([event.x, event.y]):
                    profit_val = sizes[i]
                    label = labels[i]
                    tooltip_label.config(text=f"{label}\n₱{profit_val:.2f}")
                    tooltip.geometry(f"+{event.guiEvent.x_root + 10}+{event.guiEvent.y_root + 10}")
                    tooltip.deiconify()
                    return
            tooltip.withdraw()

        canvas.mpl_connect("motion_notify_event", on_motion)

    tk.Label(content_frame, text="Use the menu on the left to manage your store.", font=("Arial", 12, "italic")).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grocery Store Dashboard")
    root.geometry("750x750")

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    show_home_page(content_frame, products, sales_history)

    root.mainloop()
