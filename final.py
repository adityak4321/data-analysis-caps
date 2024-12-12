import tkinter as tk
from tkinter import messagebox
import pandas as pd
import threading

# Load the Excel data
file_path = r"C:\Users\TechSolutions\OneDrive - Blue Valley School District\python codes\pythonProject\personal project\predictedd.xlsx"


def load_data():
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Error loading file: {e}")
        return None

def calculate_average_price(bedrooms, bathrooms, area_min, area_max, school, city, year, result_label):
    # Load the data
    data = load_data()
    if data is None:
        return

    # Filter data based on user input
    filtered_data = data[
        (data['bedroom'] == bedrooms) &
        (data['bathroom'] == bathrooms) &
        (data['area'] >= area_min) &
        (data['area'] <= area_max) &
        (data['school'].str.contains(school, case=False)) &
        (data['city'].str.contains(city, case=False))
    ]

    # Check if the year column is available in the data
    year_column = f"Value {year}"
    if year_column not in data.columns:
        messagebox.showerror("Error", f"Year {year} is not available in the data.")
        return

    # Calculate the average price for the filtered data
    if filtered_data.empty:
        result_label.config(text="No matching data found.")
    else:
        average_price = filtered_data[year_column].mean()
        result_label.config(text=f"Average Price: ${average_price:,.2f}")

# Create the main application window
root = tk.Tk()
root.title("Price Prediction App")
root.geometry("450x600")  # Adjusted window size
root.configure(bg='white')  # White background

# Custom styles
input_font = ('Helvetica', 14)
label_font = ('Helvetica', 14, 'bold')
button_font = ('Helvetica', 14, 'bold')
entry_width = 20  # Set width for the entry fields

# Function to create a label and entry box inside the gray background box
def create_input_field(parent, label_text, entry_var):
    label = tk.Label(parent, text=label_text, bg='#E6E6E6', fg='#F8C300', font=label_font)
    label.pack(pady=5, anchor='w', padx=15)
    
    entry = tk.Entry(parent, textvariable=entry_var, font=input_font, width=entry_width, bd=0, relief="flat", borderwidth=2)
    entry.pack(pady=5, padx=15)

# Create the gray background frame for all inputs
input_frame = tk.Frame(root, bg='#E6E6E6', bd=0, relief="flat", padx=20, pady=20)
input_frame.pack(fill='x', padx=20, pady=20)

# Create and place the labels and input fields inside the gray box
bedrooms_var = tk.DoubleVar()
bathrooms_var = tk.DoubleVar()
area_min_var = tk.DoubleVar()
area_max_var = tk.DoubleVar()
school_var = tk.StringVar()
city_var = tk.StringVar()
year_var = tk.IntVar()

create_input_field(input_frame, "Enter the number of bedrooms:", bedrooms_var)
create_input_field(input_frame, "Enter the number of bathrooms:", bathrooms_var)
create_input_field(input_frame, "Enter the minimum area (sqft):", area_min_var)
create_input_field(input_frame, "Enter the maximum area (sqft):", area_max_var)
create_input_field(input_frame, "Enter the school name:", school_var)
create_input_field(input_frame, "Enter the city name:", city_var)
create_input_field(input_frame, "Enter the year (2020-2028):", year_var)

# Label to display the result (price)
result_label = tk.Label(root, text="", bg='white', fg='#F8C300', font=('Helvetica', 16, 'bold'))
result_label.pack(pady=20)

# Function to handle button click
def on_submit():
    try:
        bedrooms = bedrooms_var.get()
        bathrooms = bathrooms_var.get()
        area_min = area_min_var.get()
        area_max = area_max_var.get()
        school = school_var.get()
        city = city_var.get()
        year = year_var.get()
        
        # Disable the button while the calculation is running
        submit_button.config(state="disabled")
        
        # Start a new thread to calculate the average price
        threading.Thread(target=calculate_average_price, args=(bedrooms, bathrooms, area_min, area_max, school, city, year, result_label)).start()

        # Re-enable the button after the thread finishes (but this will be handled in the thread)
        submit_button.config(state="normal")
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for bedrooms, bathrooms, and areas.")

# Create the submit button with rounded corners
submit_button = tk.Button(root, text="Get Average Price", bg='#F8C300', fg='black', font=button_font, command=on_submit, relief="flat", padx=20, pady=10)
submit_button.pack(pady=20)

# Run the application
root.mainloop()
