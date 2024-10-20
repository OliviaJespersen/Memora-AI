from datetime import date
import json
import os


class DailyApiCallCounter:
    def __init__(self, storage_file_path):
        self.storage_file_path = storage_file_path

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
        today = date.today().strftime("%d/%m/%Y")
        if today in self.call_data:
            self.call_data[today] += 1
        else:
            self.call_data[today] = 1
        self.save_metadata()


    def get_count(self):
        today = date.today().strftime("%d/%m/%Y")
        if not today in self.call_data:
            self.call_data[today] = 0
            self.save_metadata()
        return self.call_data[today]


    def clean(self):
        today = date.today().strftime("%d/%m/%Y")
        for day in [day for day in self.call_data if day != today]:
            del self.call_data[day]
        self.save_metadata()
