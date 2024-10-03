import tkinter as tk
from tkinter import ttk
import json
from PIL import Image, ImageTk

# read file , load data
users_file = open("users.json",'r')
users_list = json.load(users_file)
users_file.close()

def ret_info(user_id):
    for user in users_list:
        if user["ID"] == user_id:
            return user["Cart"], user["Governorate"]
    return [], None

def calculate_price(cart_lst):  # list of dictionaries
    if len(cart_lst) == 0:
        return 0
    return calculate_price(cart_lst[1:]) + cart_lst[0]["Price"]

def calculate_fees(user_governorate):
    governorate_prices = {"cairo": 20, "giza": 30, "alexandria": 40, "port said": 50, "banha": 60}
    if user_governorate.lower() in governorate_prices.keys():
        return governorate_prices[user_governorate]
    return 80

def show_price_details(cart_list, user_gov):
    items_price = calculate_price(cart_list)
    delivery_fees = calculate_fees(user_gov)
    total_price = items_price + delivery_fees

    price_window = tk.Toplevel(root)
    price_window.title("Price Details")
    price_window.geometry("400x300")
    price_window.configure(bg="#f5f5f5")

    ttk.Label(price_window, text=f"Total Items Price: ${items_price:.2f}", style="Custom.TLabel").pack(pady=10)
    ttk.Label(price_window, text=f"Delivery Fees: ${delivery_fees:.2f}", style="Custom.TLabel").pack(pady=10)
    ttk.Label(price_window, text=f"Total Price: ${total_price:.2f}", font=("Arial", 16, "bold"), style="Custom.TLabel").pack(pady=10)

def show_cart_page(user_id):
    cart_list, user_gov = ret_info(user_id)

    for widget in main_frame.winfo_children():
        widget.destroy()

    if not cart_list:
        ttk.Label(main_frame, text="Cart is Empty!", style="Custom.TLabel").pack(pady=20)
        return

    ttk.Label(main_frame, text="Cart Items", font=("Arial", 18, "bold"), style="Custom.TLabel").pack(pady=10)

    items_frame = ttk.Frame(main_frame, style="TFrame")
    items_frame.pack(fill='both', expand=True)

    canvas = tk.Canvas(items_frame)
    scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # show cart items
    for item in cart_list:
        item_frame = ttk.Frame(scrollable_frame, padding="5", style="TFrame")
        item_frame.pack(pady=5, padx=10, fill='x')

        img = Image.open(item["ImagePath"])
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(item_frame, image=img)
        img_label.image = img  # reference => to avoid garbage collection
        img_label.pack(side='left', padx=10)

        details = f"{item['Name']} - ${item['Price']} - {item['Brand']} - {item['ModelYear']}"
        ttk.Label(item_frame, text=details, style="Custom.TLabel").pack(side='left')

    checkout_button = ttk.Button(main_frame, text="Checkout", style="Modern.TButton", command=lambda: show_price_details(cart_list, user_gov))
    checkout_button.pack(pady=20)

# Main window
root = tk.Tk()
root.title("User Cart")
root.geometry("700x700")
root.configure(bg="#FFB347")

# Style configurations
style = ttk.Style()
style.theme_use("clam")

style.configure("Custom.TLabel", foreground="#4f4f4f", background="#f5f5f5", font=("Arial", 12))

style.configure("Modern.TButton",
                background="#CFB095",
                foreground="#000000",
                font=("Arial", 12, "bold"),
                padding=10,
                relief="raised")

style.map("Modern.TButton",
          background=[("active", "#FFE4C4")],
          foreground=[("active", "#000000")])

style.configure("TFrame", background="#f5f5f5")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill='both', expand=True)

show_cart_page(1)

root.mainloop()