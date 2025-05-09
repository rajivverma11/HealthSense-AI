import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("appointments.db")
cursor = conn.cursor()

# Create patients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT
)
""")

# Create appointments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    appointment_date TEXT,
    doctor TEXT,
    reason TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
)
""")

# Insert sample data into patients
cursor.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", ("John Doe", 30, "Male"))
cursor.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", ("Jane Smith", 25, "Female"))

# Get inserted patient IDs
cursor.execute("SELECT id FROM patients WHERE name='John Doe'")
john_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM patients WHERE name='Jane Smith'")
jane_id = cursor.fetchone()[0]

# Insert sample data into appointments
cursor.execute("INSERT INTO appointments (patient_id, appointment_date, doctor, reason) VALUES (?, ?, ?, ?)",
               (john_id, "2025-05-05", "Dr. House", "Flu symptoms"))

cursor.execute("INSERT INTO appointments (patient_id, appointment_date, doctor, reason) VALUES (?, ?, ?, ?)",
               (jane_id, "2025-05-06", "Dr. Grey", "Annual checkup"))

# Commit changes
conn.commit()

# Print the data to confirm
print("Patients:")
cursor.execute("SELECT * FROM patients")
for row in cursor.fetchall():
    print(row)

print("\nAppointments:")
cursor.execute("SELECT * FROM appointments")
for row in cursor.fetchall():
    print(row)

# Close connection
conn.close()
