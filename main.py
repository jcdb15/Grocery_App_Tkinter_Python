# main.py
import tkinter as tk
from pages.Home import show_home_page
from pages.Add_Product import show_add_product_page
from pages.Product_List import show_product_list_page
from pages.Sell_Products import show_sell_products_page
from pages.Sales_History import show_sales_history_page
from pages.Settings import show_settings_page

def run():
    global root, content_frame

    # Shared data
    products = []
    sales_history = []

    root = tk.Tk()
    root.title("Grocery Store Dashboard")
    root.geometry("800x600")

    # Sidebar
    sidebar = tk.Frame(root, width=200, bg="#2C3E50")
    sidebar.pack(side="left", fill="y")

    # Sidebar buttons with commands passing shared data and content frame
    tk.Button(sidebar, text="Home",
              command=lambda: show_home_page(content_frame, products, sales_history),
              width=20, bg="#1ABC9C", fg="white").pack(pady=10)

    tk.Button(sidebar, text="Add Product",
              command=lambda: show_add_product_page(content_frame, products),
              width=20, bg="#27AE60", fg="white").pack(pady=10)

    tk.Button(sidebar, text="Product List",
              command=lambda: show_product_list_page(content_frame, products),
              width=20, bg="#2980B9", fg="white").pack(pady=10)

    tk.Button(sidebar, text="Sell Products",
              command=lambda: show_sell_products_page(content_frame, products, sales_history),
              width=20, bg="#E67E22", fg="white").pack(pady=10)

    tk.Button(sidebar, text="Sales History",
              command=lambda: show_sales_history_page(content_frame, sales_history),
              width=20, bg="#9b59b6", fg="white").pack(pady=10)

    tk.Button(sidebar, text="Settings",
              command=lambda: show_settings_page(content_frame),
              width=20, bg="#34495E", fg="white").pack(pady=10)

    # Main content frame where pages render their UI
    content_frame = tk.Frame(root, bg="#ECF0F1")
    content_frame.pack(side="left", fill="both", expand=True)

    # Show Home page by default
    show_home_page(content_frame, products, sales_history)

    root.mainloop()

if __name__ == "__main__":
    run()
