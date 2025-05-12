import pandas as pd
from .doctor_slot_generator import DoctorSlotGenerator

# Load seed doctor data
seed_df = pd.read_csv("data/doctors_slots_data.csv")

# Generate slots
generator = DoctorSlotGenerator(seed_df)
slots_df = generator.generate_slots(
    days_ahead=90,
    work_start_hour=9,
    work_end_hour=17,
    interval_minutes=30,
    exclude_weekends=True
)

# Save to file
#slots_df.to_csv("generated_doctor_slots.csv", index=False)
print(f"✅ Generated doctor slots for working days and count is : {len(slots_df)}")


if __name__ == "__main__":
     print("Running main.py...")
     print(f"✅ Generated doctor slots for working days and count is : {len(slots_df)}")

