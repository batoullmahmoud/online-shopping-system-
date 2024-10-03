import json
import os
import subprocess
from tkinter import *
from tkinter import messagebox

# searching for Json file , if located then read it , if not then make one
if os.path.exists("admins.json"):
    try:
        with open("admins.json", "r") as file:
            admins = json.load(file)
    except json.JSONDecodeError:
        print("Error parsing JSON file. Please check the file format.")
        admins = []
else:
    print("admin data file not found. Creating a new file...")
    admins = []
    with open("admins.json", "w") as file:
        json.dump(admins, file, indent=2)

main = Tk()
main.geometry("1366x768")
main.title("SIC Online Shopping ")
main.resizable(0, 0)


def Exit():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=main)
    if sure == True:
        main.destroy()


main.protocol("WM_DELETE_WINDOW", Exit)


def adm():
    main.destroy()  # Close login window
    subprocess.Popen(["python", "admin_page.py"])  # Open admin_page.py


def validate_login():
    email = email_entry.get()
    password = password_entry.get()
    global admin
    for admin in admins:
        if admin["Email"] == email and admin["Password"] == password:
            global current_admin
            current_admin = admin["username"]
            massage = f"Login succssesful welcom, {current_admin} !"
            messagebox.showinfo("Login Succesful", massage)
            adm()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


# placing the background image
label1 = Label(main)
label1.place(relx=0, rely=0, width=1366, height=768)
img = PhotoImage(file="login_bg.png")
label1.configure(image=img)

# Create and place the username label and entry

email_label = Label(main, text="Email", width=35, anchor=W, fg='#908585', font='Roboto')
email_label.place(relx=0.361, rely=0.24)

email_entry = Entry(main, width=35, font='Roboto')
email_entry.place(relx=0.38, rely=0.285, height=30)

# Create and place the password label and entry
passsword_label = Label(main, text="Password", fg='#908585', font='Roboto')
passsword_label.place(relx=0.36, rely=0.35)

password_entry = Entry(main, width=35, show='*', font='Roboto')
password_entry.place(relx=0.38, rely=0.387, height=30)

# Create and place the login button
login_button = Button(main, text="Login", font=('Anton', 18, 'bold'), foreground='white', width=23
                      , border=0, cursor="hand2", bg='#d6413a', activebackground="#d6413a", command=validate_login)
login_button.place(relx=0.375, rely=0.67, height=36)

main.mainloop()