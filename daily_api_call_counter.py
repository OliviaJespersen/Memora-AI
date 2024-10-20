from datetime import date
import json
import os


class DailyApiCallCounter:
    def __init__(self, storage_file_path):
        self.storage_file_path = storage_file_path
        self.today = date.today().strftime("%d/%m/%Y")

        try:
            with open(self.storage_file_path, "r") as storage_file:
                self.call_data = json.load(storage_file)
        except FileNotFoundError:
            raise Exception("calls file was not found.")
        except json.JSONDecodeError:
            raise Exception("calls file was corrupted.")
        self.clean()


    def save_metadata(self):
        with open(self.storage_file_path, "w") as storage_file:
            json.dump(self.call_data, storage_file, indent=4)


    def new_call(self):
        self.call_data[self.today] += 1
        self.save_metadata()


    def get_count(self):
        return self.call_data[self.today]


    def clean(self):
        for day in [day for day in self.call_data if day != self.today]:
            del self.call_data[day]
        if not self.today in self.call_data or not isinstance(self.call_data[self.today], int):
            self.call_data[self.today] = 0
        self.save_metadata()
