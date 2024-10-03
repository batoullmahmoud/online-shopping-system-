import re
import os
import json
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
import subprocess

# Read file, load data
if os.path.exists("users.json"):
    with open("users.json", 'r') as users_file:
        users_list = json.load(users_file)
else:
    users_list = []

# Function to create the gradient background
def create_gradient(canvas, width, height, start_color, end_color):
    start_r = int(start_color[1:3], 16)
    start_g = int(start_color[3:5], 16)
    start_b = int(start_color[5:7], 16)

    end_r = int(end_color[1:3], 16)
    end_g = int(end_color[3:5], 16)
    end_b = int(end_color[5:7], 16)

    steps = height
    for i in range(steps):
        r = int(start_r + (end_r - start_r) * i / steps)
        g = int(start_g + (end_g - start_g) * i / steps)
        b = int(start_b + (end_b - start_b) * i / steps)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)

# Function to draw a rounded rectangle
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def validate_data():
    errors = []
    if not name_var.get().strip():
        errors.append("- Name cannot be empty.")
    if not re.match(r'^\d{10,15}$', phone_var.get()):
        errors.append("- Phone number must be 10-15 digits long.")
    if not re.match(r'^\S+@\S+\.\S+$', email_var.get()):
        errors.append("- Invalid email format.")
    if not gender_var.get().strip():
        errors.append("- Gender cannot be empty.")
    if not governorate_var.get().strip():
        errors.append("- Governorate cannot be empty.")
    if len(password_var.get()) < 6:
        errors.append("- Password must be at least 6 characters long.")
    try:
        age = int(age_var.get())
        if age <= 0:
            errors.append("- Age must be a positive number.")
    except ValueError:
        errors.append("- Age must be a valid integer.")
    if not re.match(r'^\d{14}$', national_id_var.get()):
        errors.append("- National ID must be 14 digits long.")

    return errors

def register_user():
    errors = validate_data()
    if errors:
        error_message = "\n".join(errors)
        messagebox.showerror("Invalid Input", error_message)
        return
    user_id = len(users_list) + 1
    user_data = {
        "ID": user_id,
        "username": name_var.get(),
        "Phone Number": phone_var.get(),
        "Email": email_var.get(),
        "Gender": gender_var.get(),
        "Governorate": governorate_var.get(),
        "Password": password_var.get(),
        "Age": age_var.get(),
        "National ID": national_id_var.get(),
        "Cart": []
    }

    if not os.path.exists("users.json"):
        with open("users.json", "w") as file:
            json.dump([], file, indent=4)

    with open("users.json", "r+") as file:
        users = json.load(file)
        users.append(user_data)
        file.seek(0)
        json.dump(users, file, indent=4)

    messagebox.showinfo("Success", "Registration successful!")

def go_to_login():
    root.destroy()
    subprocess.run(["python", "login.py"])

# Create the main window
root = tk.Tk()
root.title("Registration Page")
root.geometry("1366x768")

# Gradient background
width, height = 1366, 768
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()

start_color = "#ff626d"
end_color = "#ff9a70"
create_gradient(canvas, width, height, start_color, end_color)

frame_width = 800
frame_height = 400
x1 = (width - frame_width) // 2
y1 = (height - frame_height) // 2
x2 = x1 + frame_width
y2 = y1 + frame_height

round_rectangle(x1, y1, x2, y2, radius=40, fill="#ffffff", outline="")

# Font styles
title_font = tkFont.Font(family="Arial", size=24, weight="bold")
label_font = tkFont.Font(family="Arial", size=12)
button_font = tkFont.Font(family="Arial", size=14, weight="bold")

# Variables to store user input
name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
gender_var = tk.StringVar()
governorate_var = tk.StringVar()
password_var = tk.StringVar()
age_var = tk.StringVar()
national_id_var = tk.StringVar()

# Add "Register" title
register_label = tk.Label(root, text="Register", font=title_font, bg="#ffffff", fg="black")
register_label.place(x=x1 + frame_width // 2, y=y1 + 24, anchor="center")

# Left column labels and entries
name_label = tk.Label(root, text="Name", font=label_font, bg="#ffffff")
name_label.place(x=x1 + 70, y=y1 + 80)
name_entry = tk.Entry(root, font=label_font, textvariable=name_var, width=30)
name_entry.place(x=x1 + 70, y=y1 + 110)

phone_label = tk.Label(root, text="Phone Number", font=label_font, bg="#ffffff")
phone_label.place(x=x1 + 70, y=y1 + 150)
phone_entry = tk.Entry(root, font=label_font, textvariable=phone_var, width=30)
phone_entry.place(x=x1 + 70, y=y1 + 180)

email_label = tk.Label(root, text="Email", font=label_font, bg="#ffffff")
email_label.place(x=x1 + 70, y=y1 + 220)
email_entry = tk.Entry(root, font=label_font, textvariable=email_var, width=30)
email_entry.place(x=x1 + 70, y=y1 + 250)

gender_label = tk.Label(root, text="Gender", font=label_font, bg="#ffffff")
gender_label.place(x=x1 + 70, y=y1 + 290)
gender_entry = tk.Entry(root, font=label_font, textvariable=gender_var, width=10)
gender_entry.place(x=x1 + 70, y=y1 + 320)

# Right column labels and entries
governorate_label = tk.Label(root, text="Governorate", font=label_font, bg="#ffffff")
governorate_label.place(x=x1 + 460, y=y1 + 80)
governorate_entry = tk.Entry(root, font=label_font, textvariable=governorate_var, width=20)
governorate_entry.place(x=x1 + 460, y=y1 + 110)

password_label = tk.Label(root, text="Password", font=label_font, bg="#ffffff")
password_label.place(x=x1 + 460, y=y1 + 150)
password_entry = tk.Entry(root, font=label_font, textvariable=password_var, width=20, show="*")
password_entry.place(x=x1 + 460, y=y1 + 180)

age_label = tk.Label(root, text="Age", font=label_font, bg="#ffffff")
age_label.place(x=x1 + 460, y=y1 + 220)
age_entry = tk.Entry(root, font=label_font, textvariable=age_var, width=10)
age_entry.place(x=x1 + 460, y=y1 + 250)

national_id_label = tk.Label(root, text="National ID", font=label_font, bg="#ffffff")
national_id_label.place(x=x1 + 460, y=y1 + 290)
national_id_entry = tk.Entry(root, font=label_font, textvariable=national_id_var, width=30)
national_id_entry.place(x=x1 + 460, y=y1 + 320)

# Register button
register_button = tk.Button(root, text="Register", font=button_font, bg="#ff4c4c", fg="white", bd=0, padx=20, pady=10, command=register_user)
register_button.place(x=x1 + frame_width // 2 - 50, y=y1 + 360, anchor="center")

login_button = tk.Button(root, text="Go to Login", font=button_font, bg="#F1E9D2", fg="black", bd=0, padx=20, pady=10, command=go_to_login)
login_button.place(relx=0.95, rely=0.85, anchor="ne")

root.mainloop()