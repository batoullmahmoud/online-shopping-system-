import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

import os
from PIL import Image, ImageTk

# Read file and load data
with open("categories.json", 'r') as categories_file:
    categories_list = json.load(categories_file)

# Initialize root and canvas as global variables
root = tk.Tk()
canvas = tk.Canvas(root, width=1366, height=768, highlightthickness=0)
canvas.pack(fill="both", expand=True)

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

# Stack class for page navigation
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return None if self.isEmpty() else self.items.pop()

    def isEmpty(self):
        return not self.items

    def top(self):
        return None if self.isEmpty() else self.items[-1]

    def count(self):
        return None if self.isEmpty() else len(self.items)
# obj mn stack
pages_stack = Stack()

# Back button functionality
def back():
    if not pages_stack.isEmpty():  # There is a previous page
        previous_page = pages_stack.pop()
        previous_page()  # Call the previous page function

# Function to draw rounded rectangle
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Function to create a rounded button
def create_rounded_button(canvas, x, y, width, height, text=None, icon=None, command=None, radius=25, bg="#CFB095", active_bg="#FFE4C4"):
    button_id = canvas.create_polygon(
        x + radius, y,
        x + width - radius, y,
        x + width, y + radius,
        x + width, y + height - radius,
        x + width - radius, y + height,
        x + radius, y + height,
        x, y + height - radius,
        x, y + radius,
        fill=bg, outline="", tags="button"
    )
    
    if icon:
        icon_image = Image.open(icon)
        icon_image = icon_image.resize((height - 10, height - 10), Image.LANCZOS)  # Use LANCZOS for resizing
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_id = canvas.create_image(x + width // 2, y + height // 2, image=icon_photo, tags="button")
        canvas.image = icon_photo  # Store reference to avoid garbage collection
    elif text:
        text_id = canvas.create_text(x + width // 2, y + height // 2, text=text, font=("Arial", 12, "bold"), fill="#000000", tags="button")

    def on_enter(event):
        canvas.itemconfig(button_id, fill=active_bg)

    def on_leave(event):
        canvas.itemconfig(button_id, fill=bg)

    def on_click(event):
        if command:
            command()

    canvas.tag_bind(button_id, "<Enter>", on_enter)
    canvas.tag_bind(button_id, "<Leave>", on_leave)
    canvas.tag_bind(button_id, "<Button-1>", on_click)

    if icon:
        canvas.tag_bind(icon_id, "<Enter>", on_enter)
        canvas.tag_bind(icon_id, "<Leave>", on_leave)
        canvas.tag_bind(icon_id, "<Button-1>", on_click)
    elif text:
        canvas.tag_bind(text_id, "<Enter>", on_enter)
        canvas.tag_bind(text_id, "<Leave>", on_leave)
        canvas.tag_bind(text_id, "<Button-1>", on_click)

# Function to create a rounded button with an icon only
def create_rounded_button_icon(canvas, x, y, width, height, icon=None, command=None, radius=25):
    button_id = canvas.create_polygon(
        x + radius, y,
        x + width - radius, y,
        x + width, y + radius,
        x + width, y + height - radius,
        x + width - radius, y + height,
        x + radius, y + height,
        x, y + height - radius,
        x, y + radius,
        fill="", outline="", tags="button"
    )
    
    if icon:
        icon_image = Image.open(icon)
        icon_image = icon_image.resize((width, height), Image.LANCZOS)  # Resize to fit the button
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_id = canvas.create_image(x + width // 2, y + height // 2, image=icon_photo, tags="button")
        canvas.image = icon_photo  # Store reference to avoid garbage collection

    def on_click(event):
        if command:
            command()

    canvas.tag_bind(button_id, "<Button-1>", on_click)
    if icon:
        canvas.tag_bind(icon_id, "<Button-1>", on_click)

# Show categories page
def show_categories_page():

    clear_canvas()  # Clear canvas before drawing new elements
    canvas.create_text(width // 2, 70, text="Categories", font=("Arial", 48, "bold"), fill="#4f4f4f")
    exit_button()


    y_offset = 150
    for category in categories_list.keys():
        create_rounded_button(canvas, width // 2 - 250, y_offset, 500, 50, text=category, command=lambda c=category: open_category_page(c))
        y_offset += 90



def open_update_item_form(category, index):
    update_item_form(category, index)

# Store the PhotoImage references globally or within the class
photo_image_references = []  # List to hold references to PhotoImage objects

def open_category_page(category):
    global photo_image_references  # Ensure we're using the global list to store image references
    clear_canvas()  # Clear canvas before drawing new elements
    pages_stack.push(lambda: show_categories_page())  # Push current page to stack
    canvas.create_text(width // 2, 50, text=f"Manage items for {category}", font=("Arial", 18, "bold"), fill="#4f4f4f")

    # Initialize coordinates
    x_start = width // 10
    y_start = 100
    x_offset = (width - 2 * x_start) // 3  # Adjust the width for each item
    y_offset = 200

    row_count = 0
    column_count = 0
    # Loading Items:
    # items = categories_list[category]: Retrieves the items for the selected category from categories_list.
    items = categories_list[category]
    num_items = len(items)

    # Clear the references list at the start of page loading to prevent old references from being kept unnecessarily
    photo_image_references.clear()
    # Iterating Through Items:
    for i in range(num_items):
        item = items[i]
        item_image_path = item.get('ImagePath')
        print(f"Loading image from: {item_image_path}")

        if item_image_path and os.path.exists(item_image_path):
            try:
                # Open and resize the image
                item_image = Image.open(item_image_path)
                item_image = item_image.resize((70, 70), Image.LANCZOS)

                # Convert to PhotoImage and append to the list to persist the reference
                item_photo = ImageTk.PhotoImage(item_image)
                photo_image_references.append(item_photo)  # Keep a reference to prevent garbage collection

            except Exception as e:
                print(f"Error loading image {item_image_path}: {e}")
                continue

            # Calculate position
            x = width // 2 - 450 + column_count * 200  # Center items horizontally
            y = y_start + row_count * y_offset

            # Debugging information
            print(f"Drawing image at ({x}, {y})")

            # Draw image as button using the cached PhotoImage object
            create_rounded_button(canvas, x, y, 160, 250, command=lambda i=i: open_update_item_form(category, i))
            canvas.create_image(x + 80, y + 60, image=item_photo)  # Center image inside button

            # Display details below the image
            details = [
                f"Name: {item['Name']}",
                f"Price: ${item['Price']}",
                f"Brand: {item['Brand']}",
                f"Model Year: {item['ModelYear']}"
            ]
            # b3ml lkol item button byft7  open_update_item_form(category, i),function lma click on the item
            y_detail = y + 130  # Adjust y position to be below the image
            for detail in details:
                canvas.create_text(x + 70, y_detail, text=detail, font=("Arial", 10), fill="#333", tags="click_text")
                canvas.tag_bind("click_text", "<Button-1>", lambda event, cat=category, i=i: open_update_item_form(cat, i))
                y_detail += 20

            column_count += 1
            if column_count == 5:  # Move to next row after 5 columns
                column_count = 0
                row_count += 1
        else:
            print(f"Image path not found or invalid: {item_image_path}")

            create_rounded_button(canvas, x, y, 160, 250, command=lambda i=i: open_update_item_form(category, i))
            create_rounded_button_icon(canvas, x + 40, y + 20, 80, 80, icon=item_image_path, radius=40)

        
            # Display details below the image
            details = [
                f"Name: {item['Name']}",
                f"Price: ${item['Price']}",
                f"Brand: {item['Brand']}",
                f"Model Year: {item['ModelYear']}"
            ]

            y_detail = y + 130  # Adjust y position to be below the image
            for detail in details:
                canvas.create_text(x + 70, y_detail, text=detail, font=("Arial", 10), fill="#333", tags="click_text")
                canvas.tag_bind("click_text", "<Button-1>", lambda event, cat=category, i=i: open_update_item_form(cat, i))
                y_detail += 20
            column_count += 1
            if column_count == 5:  # Move to next row after 5 columns
                column_count = 0
                row_count += 1

            else:
                print(f"Image path not found or invalid: {item_image_path}")

        
    # Add buttons at the bottom of the page

    create_rounded_button(canvas, width - 400, height - 150, 300, 50, text="Back", command=back)
    create_rounded_button(canvas, width // 5 - 150, height - 150, 300, 50, text="Add Item", command=lambda: add_item_form(category))
    create_rounded_button(canvas, width // 2 - 150, height - 150, 300, 50, text="Delete Selected Item", command=lambda: delete_item(category))


# Add new item form
def add_item_form(category):
    clear_canvas() # remove any previous content
    pages_stack.push(lambda: open_category_page(category))

    canvas.create_text(width // 2, 50, text=f"Add new item in {category} Category:", font=("Arial", 16, "bold"))

    y_offset = 150
    fields = ["Item Name", "Item Price", "Item Brand", "Model Year", "Image Path"]
    entries = []
    # b3ml label , entry ll fields
    for i, field in enumerate(fields):  # index and the value
        label = ttk.Label(root, text=field)
        entry = ttk.Entry(root, width=30)
        canvas.create_window(width // 2 - 100, y_offset, window=label)
        canvas.create_window(width // 2 + 100, y_offset, window=entry)
        entries.append(entry)
        y_offset += 40

    btn_browse = ttk.Button(root, text="Browse", command=lambda: browse_image(entries[4]))
    canvas.create_window(width // 2 + 250, y_offset - 40, window=btn_browse)

    def save_added():
        new_item = {
            "Name": entries[0].get(),
            "Price": float(entries[1].get()),
            "Brand": entries[2].get(),
            "ModelYear": entries[3].get(),
            "ImagePath": entries[4].get(),
        }
        categories_list[category].append(new_item)
        with open("categories.json", "w") as categories_file:
            json.dump(categories_list, categories_file, indent=4)
        messagebox.showinfo("Success", "Item added successfully!")

    create_rounded_button(canvas, width // 2 - 150, y_offset + 35, 300, 50, text="Add Item", command=save_added)
    create_rounded_button(canvas, width // 2 - 150, y_offset + 100, 300, 50, text="Back", command=back)

# Update item form
def update_item_form(category, index):
    # Canvas Setup
    clear_canvas()
    pages_stack.push(lambda: open_category_page(category))

    item = categories_list[category][index]
    canvas.create_text(width // 2, 50, text=f"Update item in {category} Category:", font=("Arial", 16, "bold"))

    y_offset = 150
    fields = ["Item Name", "Item Price", "Item Brand", "Model Year", "Image Path", "Discount (%)"]
    entries = []
    for i, field in enumerate(fields):
        label = ttk.Label(root, text=field)
        entry = ttk.Entry(root, width=30)
        canvas.create_window(width // 2 - 100, y_offset, window=label)
        canvas.create_window(width // 2 + 100, y_offset, window=entry)
        entries.append(entry)
        y_offset += 40


    btn_browse = ttk.Button(root, text="Browse", command=lambda: browse_image(entries[4]))
    canvas.create_window(width // 2 + 240, y_offset - 79, window=btn_browse)

   # bmla (Pre-populates the entry fields) with the existing values of the item (retrieved from categories_list)
    entries[0].insert(0, item['Name'])
    entries[1].insert(0, item['Price'])
    entries[2].insert(0, item['Brand'])
    entries[3].insert(0, item['ModelYear'])
    entries[4].insert(0, item['ImagePath'])

    def save_update():
        item['Name'] = entries[0].get()
        item['Price'] = float(entries[1].get())
        item['Brand'] = entries[2].get()
        item['ModelYear'] = entries[3].get()
        item['ImagePath'] = entries[4].get()

        discount_str = entries[5].get()
        if discount_str:
            discount = float(discount_str)
            discounted_price = float(item['Price']) * (1 - discount / 100)
            # update price
            item['Price'] = round(discounted_price, 2)
        # item is updated with the new values entered by the user.
        categories_list[category][index] = item
        with open("categories.json", "w") as categories_file:
            json.dump(categories_list, categories_file, indent=4)

        messagebox.showinfo("Success", "Item updated successfully!")

    create_rounded_button(canvas, width // 2 - 150, y_offset + 35, 300, 50, text="Update Item", command=save_update)
    create_rounded_button(canvas, width // 2 - 150, y_offset + 100, 300, 50, text="Back", command=back)

# Delete selected item
def delete_item(category):
    clear_canvas()
    pages_stack.push(lambda: open_category_page(category))

    canvas.create_text(width // 2, 50, text=f"Delete item in {category} Category:", font=("Arial", 16, "bold"))

    x_start = width // 10
    y_start = 100
    x_offset = (width - 2 * x_start) // 3  # Adjust the width for each item
    y_offset = 200

    row_count = 0
    column_count = 0
    # loops 3l items el fe  category da  and for each item:
    for idx, item in enumerate(categories_list[category]):
        item_image_path = item.get('ImagePath')
        print(f"Loading image from: {item_image_path}")

        try:
            if item_image_path and os.path.exists(item_image_path):
                item_image = Image.open(item_image_path)
                print(f"Image loaded successfully: {item_image_path}")
            else:
                print(f"Image path is invalid or file does not exist: {item_image_path}")
                item_image = Image.new('RGB', (70, 70), color='grey')  # Placeholder image
        except Exception as e:
            print(f"Error loading image {item_image_path}: {e}")
            item_image = Image.new('RGB', (70, 70), color='grey')  # Placeholder image on error

        # Resize image to 70x70
        item_image = item_image.resize((70, 70), Image.LANCZOS)
        item_photo = ImageTk.PhotoImage(item_image)
        
        canvas.image = item_photo
        print(f"Image resized and converted to PhotoImage")

        # Calculate position
        x = width // 2 - 450 + column_count * 200  # Center items horizontally
        y = y_start + row_count * y_offset

        # Draw image as button
        create_rounded_button(canvas, x, y, 160, 250, command=lambda i=idx: confirm_delete(category, i))
        create_rounded_button_icon(canvas, x+40, y+20, 80, 80, icon=item_image_path, radius=40 )

        # Display details below the image
        details = [
            f"Name: {item['Name']}",
            f"Price: ${item['Price']}",
            f"Brand: {item['Brand']}",
            f"Model Year: {item['ModelYear']}"
        ]

        y_detail = y + 130  # Adjust y position to be below the image
        for detail in details:
            canvas.create_text (x + 70, y_detail, text=detail, font=("Arial", 10), fill="#333", tags="click_text")
            canvas.tag_bind("click_text", "<Button-1>", lambda event, cat=category, i=idx: confirm_delete(cat, i))
            y_detail += 20

        column_count += 1
        if column_count == 5:  # Move to next row after 5 columns
            column_count = 0
            row_count += 1
    create_rounded_button(canvas, width // 2 - 150, y_offset + 400, 300, 50, text="Back", command=back)

def confirm_delete(category, index):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
        del categories_list[category][index]
        with open("categories.json", "w") as categories_file:
            json.dump(categories_list, categories_file, indent=4)
        messagebox.showinfo("Success", "Item deleted successfully!")
        open_category_page(category)

def clear_canvas():
    canvas.delete("all")
    create_gradient(canvas, width, height, start_color, end_color)

# Browse image file dialog
def browse_image(entry_path):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

# Exit button
def exit_button():
    icon_path = "log_icon.jpeg" 
    create_rounded_button_icon(canvas, width - 150, height - 200, 70, 70, icon=icon_path, command=root.quit, radius=40)

# Main window setup
root.title("Admin")
root.geometry("1366x768")

width , height = 1366 , 768

# Create the gradient on the canvas
start_color = "#eebc76"
end_color = "#e54c1f"
create_gradient(canvas, width, height, start_color, end_color)

# Show categories page on startup
show_categories_page()

# Create exit button
exit_button()

# Run the main loop
root.mainloop()
