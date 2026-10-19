from datetime import datetime
import os
import json
from dateutil import parser

DATA_FILE = "flux_data.json"

# AUTO-FORMAT FOR DATE
def auto_format_date(user_input):
    try:
        parsed_date = parser.parse(user_input, fuzzy=True) #fuzzy=true allows for more flexible parsing to avoid crashing
        return parsed_date.strftime("%Y-%m-%d")
    except (ValueError, OverflowError):
        return None

# AUTO-FORMAT FOR TIME
def auto_format_time(user_input):
    try:
        clean_input = user_input.replace(" ", ":", 1)
        parsed_time = parser.parse(clean_input, fuzzy=True) 
        return parsed_time.strftime("%I:%M %p")
    except (ValueError, OverflowError):
        return None    


def get_timestamp():
    print("Select logging time: ")
    print("[1] Right now")
    print("[2] A previous time")

    while True:
        choice = input("Choice: ").strip()
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.\n")

    if choice=="1":
            now = datetime.now()
            timestamp_type = "Right Now"
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%I:%M %p")
            return timestamp_type, date, time

    else:
            timestamp_type = "A Previous Time"

            while True:  #DATE INPUT LOOP
                date_input = input("Enter date (any format): ").strip()
                formatted_date = auto_format_date(date_input)

                if formatted_date is not None:
                    break

                print("Invalid date format. Please try again.\n")   

            while True:  #TIME INPUT LOOP
                time_input = input("Enter time (any format): ").strip().upper() 
                formatted_time = auto_format_time(time_input)      

                if formatted_time is not None:
                    break          

                print("Invalid time format. Please try again.\n")

            return timestamp_type, formatted_date, formatted_time


def get_metrics():

     # 1. Sleep hours (float between 0 and 24)
    while True:
        raw_val = input("Enter sleep duration in hours: ").strip() 
        try:
               sleep_hours = float(raw_val)
               if 0.0 <= sleep_hours <= 24.0:
                    break
               print("Sleep duration must be between 0 and 24 hours.\n")

        except ValueError:
            print("Please enter a valid number for sleep duration.\n")

    # 2. Sleep Quality (integer between 1 and 5)
    while True:
        raw_val = input(
            "\nRate your sleep quality:\n"
            " [1] Terrible (Restless)\n"
            " [2] Poor (Woke up often)\n"
            " [3] Okay (Average)\n"
            " [4] Good (Rested)\n"
            " [5] Excellent (Fully energized)\n"
            "Choice (1-5): "
            ).strip()
        try:
            sleep_quality = int(raw_val)
            if 1 <= sleep_quality <= 5:
                break
            print("Sleep quality must be an integer between 1 and 5.\n")
        except ValueError:
            print("Please enter a valid integer for sleep quality.\n") 

    # 3. Energy & Clarity (integer between 1 and 5)
    while True:
        raw_val = input(
            "\nRate your energy and clarity:\n"
            " [1] Very Low (Foggy)\n"
            " [2] Low (Tired)\n"
            " [3] Moderate (Average)\n"
            " [4] High (Alert)\n"
            " [5] Very High (Focused)\n"
            "Choice (1-5): "
            ).strip()
        try:
            energy_clarity = int(raw_val)
            if 1 <= energy_clarity <= 5:
                break
            print("Energy & clarity must be an integer between 1 and 5.\n")
        except ValueError:
            print("Please enter a valid integer for energy & clarity.\n")

    return sleep_hours, sleep_quality, energy_clarity


def load_records(filepath):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding = "utf-8") as f: #utf-8 encoding to support special characters for python to read the file correctly
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)

            if not isinstance(data, list):
                print(f"[ERROR] '{filepath}' does not contain a JSON list. Aborting to prevent data loss.")
                return None
            return data
    except json.JSONDecodeError:
        print(f"[ERROR] '{filepath}' contains invalid JSON. Fix or back up the file manually before writing.")
        return None

def save_records(filepath, records):
    try:
        with open(filepath, "w", encoding = "utf-8") as f:
            json.dump(records, f, indent=4)
            return True
    except OSError as err:
        print(f"[ERROR] Unable to write to '{filepath}': {err}")
        return False


def main():
    print("=== FLUX habit-tracker ===\n")

    # 1. Get timestamp
    timestamp_type, date, time = get_timestamp()

    # 2. Get metrics
    print("\n--- Core Metrics ---:")
    sleep_hours, sleep_quality, energy_clarity = get_metrics()

    # 3. Build record dictionary
    record = {
        "timestamp_type": timestamp_type,
        "date": date,
        "time": time,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "energy_clarity": energy_clarity
    }

    # 4. Load existing records, append new record, and save back to file
    records = load_records(DATA_FILE)
    if records is None:
        print("lowk couldnt save records. Aborting to prevent data loss.")
        return

    records.append(record)

    if save_records(DATA_FILE, records):
        print(f"\n[INFO] Record saved successfully to '{DATA_FILE}'.")

if __name__ == "__main__":
    main()