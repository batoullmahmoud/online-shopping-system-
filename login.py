import json
import os
from tkinter import *
from tkinter import messagebox
import subprocess

# Searching for the JSON file, if located then read it
if os.path.exists("users.json"):
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except json.JSONDecodeError:
        print("Error parsing JSON file. Please check the file format.")
        users = []
else:
    print("User data file not found. Creating a new file...")
    users = []
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

main = Tk()
main.geometry("1366x768")
main.title("SIC Online Shopping ")
main.resizable(0, 0)

def Exit():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=main)
    if sure == True:
        main.destroy()

main.protocol("WM_DELETE_WINDOW", Exit)

def usr():
    main.destroy()
    subprocess.Popen(["python", "user_interface.py"])

def save_logged(id,username,phone,email,gender,gover,password,age,national_id,cart):
    logged_user = {
        "ID": id,
        "username": username,
        "Phone Number": phone,
        "Email": email,
        "Gender": gender,
        "Governorate": gover,
        "Password":password,
        "Age": age,
        "National ID": national_id,
        "Cart": cart
    }
    with open("user.json", "w") as user_file:
        json.dump([logged_user], user_file, indent=4)



def validate_login():
    email = email_entry.get()
    password = password_entry.get()
    global user
    for user in users:
        if user["Email"] == email and user["Password"] == password:
            global current_user
            current_user = user["username"]
            message = f"Login successful, welcome {current_user}!"
            messagebox.showinfo("Login Successful", message)
            save_logged(user["ID"],user["username"],user["Phone Number"],user["Email"],user["Gender"],user["Governorate"],user["Password"],user["Age"],user["National ID"],user["Cart"])
            usr()
            return

    messagebox.showerror("Login Failed", "Invalid username or password")

def open_register():
    main.destroy()
    subprocess.run(["python", "register.py"])

# Placing the background image
label1 = Label(main)
label1.place(relx=0, rely=0, width=1366, height=768)
img = PhotoImage(file="login_bg.png")
label1.configure(image=img)

# Create and place the email label and entry
email_label = Label(main, text="Email", width=35, anchor=W, fg='#908585', font='Roboto')
email_label.place(relx=0.361, rely=0.24)

email_entry = Entry(main, width=35, font='Roboto')
email_entry.place(relx=0.38, rely=0.283, height=30)

# Create and place the password label and entry
password_label = Label(main, text="Password", fg='#908585', font='Roboto')
password_label.place(relx=0.36, rely=0.35)

password_entry = Entry(main, width=35, show='*', font='Roboto')
password_entry.place(relx=0.38, rely=0.387, height=30)

# Create and place the login button
login_button = Button(main, text="Login", font=('Anton', 18, 'bold'), foreground='white', width=23,
                      border=0, cursor="hand2", bg='#d6413a', activebackground="#d6413a", command=validate_login)
login_button.place(relx=0.375, rely=0.67, height=36)

# Link to the registration page
register_label = Label(main, text="Don't have an account? Create your account:", fg="#d6413a", font='Roboto')
register_label.place(relx=0.365, rely=0.80)

register_button = Button(main, text="Register", font=('Anton', 12),foreground='white', width=23,
                      border=0, cursor="hand2", bg='#d6413a', activebackground="#F1E9D2", command=open_register)
register_button.place(relx=0.485, rely=0.85, height=30)

main.mainloop()