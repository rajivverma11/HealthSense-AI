import pandas as pd
import random
from datetime import datetime, timedelta

class DoctorSlotGenerator:
    def __init__(self, doctor_data_df: pd.DataFrame):
        """
        doctor_data_df: DataFrame with at least one column: 'doctor_id'
        """
        self.doctor_data_df = doctor_data_df
        self.doctor_ids = self.doctor_data_df['doctor_id'].unique()

    def generate_slots(
        self,
        days_ahead: int = 90,
        work_start_hour: int = 8,
        work_end_hour: int = 17,
        interval_minutes: int = 30,
        exclude_weekends: bool = True
    ) -> pd.DataFrame:
        """
        Generate doctor slot data for each doctor for the next `days_ahead` days.
        Slots are within working hours and optionally exclude weekends.

        Returns:
            pd.DataFrame with columns: ['id', 'doctor_id', 'datetime', 'is_available']
        """
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        all_slots = []
        slot_id = 0

        for doctor_id in self.doctor_ids:
            for day_offset in range(days_ahead):
                day = today + timedelta(days=day_offset)

                # Skip weekends if required
                if exclude_weekends and day.weekday() >= 5:
                    continue

                start_time = day + timedelta(hours=work_start_hour)
                end_time = day + timedelta(hours=work_end_hour)

                # Generate slots in the work hour range
                slot_time = start_time
                while slot_time < end_time:
                    all_slots.append({
                        'id': slot_id,
                        'doctor_id': doctor_id,
                        'datetime': slot_time.strftime('%Y-%m-%d %I:%M %p'),
                        'is_available': random.randint(0, 1)
                    })
                    slot_id += 1
                    slot_time += timedelta(minutes=interval_minutes)

        return pd.DataFrame(all_slots)
