from datetime import datetime
import json
import os

DATA_FILE = "flux_data.json"


def get_timestamp():
    """Prompt the user for timestamp mode and return timestamp metadata."""
    print("Select logging time:")
    print("[1] Right Now")
    print("[2] A Previous Time")

    while True:
        choice = input("Choice: ").strip()
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.\n")

    if choice == "1":
        now = datetime.now()
        timestamp_type = "Right Now"
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%I:%M %p")
        return timestamp_type, date_str, time_str

    else:
        timestamp_type = "A Previous Time"

        # Validate manual date input
        while True:
            date_input = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                parsed_date = datetime.strptime(date_input, "%Y-%m-%d")
                date_str = parsed_date.strftime("%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD (e.g., 2026-10-18).\n")

        # Validate manual time input
        while True:
            time_input = input("Enter time (hh:mm AM/PM): ").strip().upper()
            try:
                parsed_time = datetime.strptime(time_input, "%I:%M %p")
                time_str = parsed_time.strftime("%I:%M %p")
                break
            except ValueError:
                print("Invalid time format. Please use hh:mm AM/PM (e.g., 08:30 AM or 11:15 PM).\n")

        return timestamp_type, date_str, time_str


def get_metrics():
    """Prompt for and validate the three habit metrics."""
    # 1. Sleep hours (float between 0 and 24)
    while True:
        raw_val = input("Enter sleep duration in hours (e.g., 7.5): ").strip()
        try:
            sleep_hours = float(raw_val)
            if 0.0 <= sleep_hours <= 24.0:
                break
            print("Sleep duration must be between 0 and 24 hours.\n")
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 7 or 7.5).\n")

    # 2. Sleep quality (int from 1 to 5)
    while True:
        raw_val = input("Enter sleep quality rating (1-5): ").strip()
        try:
            sleep_quality = int(raw_val)
            if 1 <= sleep_quality <= 5:
                break
            print("Rating must be a whole number between 1 and 5.\n")
        except ValueError:
            print("Invalid input. Please enter an integer from 1 to 5.\n")

    # 3. Energy & clarity (int from 1 to 5)
    while True:
        raw_val = input("Enter energy and clarity rating (1-5): ").strip()
        try:
            energy_clarity = int(raw_val)
            if 1 <= energy_clarity <= 5:
                break
            print("Rating must be a whole number between 1 and 5.\n")
        except ValueError:
            print("Invalid input. Please enter an integer from 1 to 5.\n")

    return sleep_hours, sleep_quality, energy_clarity


def load_records(filepath):
    """
    Safely load existing records from the JSON file.
    Returns a list of records, or None if the file is corrupted.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                # File is empty
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                print(f"[ERROR] '{filepath}' does not contain a JSON list. Aborting to prevent data loss.")
                return None
            return data
    except json.JSONDecodeError:
        print(f"[ERROR] '{filepath}' contains invalid JSON. Fix or back up the file manually before writing.")
        return None
    except OSError as err:
        print(f"[ERROR] Unable to read '{filepath}': {err}")
        return None


def save_records(filepath, records):
    """Write records list back to the JSON file with indentation."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
        return True
    except OSError as err:
        print(f"[ERROR] Unable to save to '{filepath}': {err}")
        return False


def main():
    print("=== FLUX Habit Tracker ===\n")

    # 1. Gather timestamp
    timestamp_type, date_str, time_str = get_timestamp()

    # 2. Gather metrics
    print("\n--- Core Metrics ---")
    sleep_hours, sleep_quality, energy_clarity = get_metrics()

    # 3. Build record dictionary
    record = {
        "timestamp_type": timestamp_type,
        "date": date_str,
        "time": time_str,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "energy_clarity": energy_clarity,
    }

    # 4. Load existing data, append new entry, and save
    records = load_records(DATA_FILE)
    if records is None:
        print("[ABORTED] Record was not saved.")
        return

    records.append(record)

    if save_records(DATA_FILE, records):
        print(f"\n[SUCCESS] Record saved for {date_str} at {time_str}")


if __name__ == "__main__":
    main()