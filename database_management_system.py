import json
import os

import search_engine


class DatabaseManagementSystem:
    def __init__(self, database_file_path, create_database_file, clean_database):
        self.database_file_path = database_file_path
        self.active_directory = os.path.dirname(self.database_file_path)
        self.search_engine = search_engine.SearchEngine(70)

        if create_database_file:
            self.metadata = {}
            self.save_metadata()

        with open(self.database_file_path, "r") as database_file:
            self.metadata = json.load(database_file)

        if clean_database:
            self.clean()

        for image in self.metadata:
            if not all(key in self.metadata[image] for key in ["image_text", "tags"]) or not image in os.listdir(self.active_directory):
                raise Exception("Database is corrupt")


    def save_metadata(self):
        with open(self.database_file_path, "w") as database_file:
            json.dump(self.metadata, database_file, indent=4)


    def add_entry(self, file_name, description):
        self.metadata[file_name] = {}
        self.metadata[file_name]["image_text"] = description[0]
        self.metadata[file_name]["tags"] = description[1]
        self.save_metadata()


    def remove_entry(self, file_name):
        del self.metadata[file_name]
        self.save_metadata()


    def reanalyze_entry(self, file_name, description):
        self.add_entry(file_name, description)


    def get_image_text(self, file_name):
        if file_name in self.metadata:
            return self.metadata[file_name]["image_text"]
        else:
            return "Not in database"


    def get_tags(self, file_name):
        if file_name in self.metadata:
            return self.metadata[file_name]["tags"]
        else:
            return "Not in database"


    def edit_image_text(self, file_name, new_image_text):
        self.metadata[file_name]["image_text"] = new_image_text
        self.save_metadata()


    def edit_tags(self, file_name, new_tags):
        self.metadata[file_name]["tags"] = new_tags
        self.save_metadata()


    def in_database(self, file_name):
        return file_name in self.metadata


    def search_database(self, search_query):
        return self.search_engine.search(search_query, self.metadata)
    

    def clean(self):
        for file_name in [file_name for file_name in self.metadata if not all(key in self.metadata[file_name] for key in ["image_text", "tags"]) or not file_name in os.listdir(self.active_directory)]:
            del self.metadata[file_name]
        self.save_metadata()
