import os
import time

from daily_api_call_counter import DailyApiCallCounter
from database_management_system import DatabaseManagementSystem
from ai_image_analysis import AiImageAnalysis


class Model:
    def __init__(
        self, gemini_ai: AiImageAnalysis, call_counter: DailyApiCallCounter, auto_clean
    ):
        self.gemini_ai = gemini_ai
        self.call_counter = call_counter
        self.active_directory = None
        self.active_file_name = None
        self.image_database: DatabaseManagementSystem = None
        self.auto_clean = auto_clean

    def open_database(self, create_database_file):
        database_file_path = self.active_directory + "/" + "database.json"
        self.image_database = DatabaseManagementSystem(
            database_file_path, create_database_file, self.auto_clean
        )
        self.active_file_name = None

    def database_file_exists(self):
        return os.path.exists(self.active_directory + "/" + "database.json")

    def search_database(self, query):
        return self.image_database.search_database(query)

    def add_entry(self):
        self.call_counter.new_call()
        ai_description = self._generate_description(self.active_file_name)
        self.image_database.add_entry(self.active_file_name, ai_description)

    def manual_add_entry(self, image_text, tags):
        self.image_database.add_entry(self.active_file_name, [image_text, tags])

    def add_all(self, update_task_progress):
        cut_list = [
            file
            for file in os.listdir(self.active_directory)
            if self._file_is_supported(file)
            and not self.image_database.in_database(file)
        ][: 1500 - self.call_counter.get_count()]
        chunk_list = [cut_list[i : i + 15] for i in range(0, len(cut_list), 15)]
        bad_files = []
        file_counter = 0

        for chunk_nr in range(len(chunk_list)):
            start_time = time.time()
            for file_name in chunk_list[chunk_nr]:
                update_task_progress(file_counter, len(cut_list))
                try:
                    self.call_counter.new_call()
                    self.image_database.add_entry(
                        file_name, self._generate_description(file_name)
                    )
                except ValueError as e:
                    bad_files += [f"{file_name}: {str(e)}"]
                file_counter += 1
            end_time = time.time()

            if chunk_nr != len(chunk_list) - 1 and end_time - start_time < 60:
                time.sleep(60 - (end_time - start_time))

        return bad_files

    def remove_entry(self):
        self.image_database.remove_entry(self.active_file_name)

    def reanalyze_entry(self):
        self.call_counter.new_call()
        self.image_database.reanalyze_entry(
            self.active_file_name, self._generate_description(self.active_file_name)
        )

    def edit_image_text(self, new_image_text):
        self.image_database.edit_image_text(self.active_file_name, new_image_text)

    def edit_tags(self, new_tags):
        self.image_database.edit_tags(self.active_file_name, new_tags)

    def get_active_directory(self):
        return self.active_directory

    def set_active_directory(self, new_directory):
        self.active_directory = new_directory

    def get_active_file_name(self):
        return self.active_file_name

    def set_active_file_name(self, new_file_name):
        self.active_file_name = new_file_name

    def get_files_in_database(self):
        return [
            file_name
            for file_name in self._get_supported_file_list()
            if self.image_database.in_database(file_name)
        ]

    def get_files_not_in_database(self):
        return [
            file_name
            for file_name in self._get_supported_file_list()
            if not self.image_database.in_database(file_name)
        ]

    def get_image_text(self):
        return self.image_database.get_image_text(self.active_file_name)

    def get_tags(self):
        return self.image_database.get_tags(self.active_file_name)

    def get_call_count(self):
        return self.call_counter.get_count()

    def _get_supported_file_list(self):
        return [
            file_name
            for file_name in os.listdir(self.active_directory)
            if self._file_is_supported(file_name)
        ]

    def _file_is_supported(self, file_name):
        return os.path.splitext(file_name)[1].lower() in [
            ".jpeg",
            ".jpg",
            ".png",
            ".webp",
        ]

    def _generate_description(self, file_name):
        return self.gemini_ai.generate_description(
            self.active_directory + "/" + file_name
        )
