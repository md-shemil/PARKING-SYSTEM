from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create a SQLite database named parking.db
conn = sqlite3.connect('parking.db')
cursor = conn.cursor()

# Create a table to store parking records with additional columns for charge amount and total amount
cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        vehicle_registration TEXT NOT NULL,
        vehicle_type TEXT NOT NULL,
        parking_hours INTEGER NOT NULL,
        charge_per_hour REAL NOT NULL,
        total_amount REAL NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone_number = request.form['phone_number']
    vehicle_registration = request.form['vehicle_registration']
    vehicle_type = request.form['vehicle_type']
    parking_hours = int(request.form['parking_hours'])

    # Get charge per hour based on the vehicle type (add your logic here)
    charge_per_hour = get_charge_per_hour(vehicle_type)

    # Calculate total amount based on the number of parking hours
    total_amount = calculate_total_amount(parking_hours, charge_per_hour)

    # Insert the data into the database
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parking_records (name, phone_number, vehicle_registration, vehicle_type, parking_hours, charge_per_hour, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone_number, vehicle_registration, vehicle_type, parking_hours, charge_per_hour, total_amount))
    conn.commit()
    conn.close()

    return render_template('bill.html', name=name, total_amount=total_amount)

@app.route('/history')
def history():
    # Retrieve parking history from the database
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parking_records ORDER BY id DESC')
    parking_history = cursor.fetchall()
    conn.close()

    return render_template('history.html', parking_history=parking_history)

def get_charge_per_hour(vehicle_type):
    # Add your logic to get the charge per hour based on the vehicle type
    # For simplicity, let's assume different charges for car and motorcycle
    if vehicle_type == 'car':
        return 5.0
    elif vehicle_type == 'motorcycle':
        return 3.0
    else:
        return 0.0  # Default charge for unknown vehicle types

def calculate_total_amount(parking_hours, charge_per_hour):
    # Calculate the total amount based on the number of parking hours and charge per hour
    return parking_hours * charge_per_hour

if __name__ == '__main__':
    app.run(debug=True)
