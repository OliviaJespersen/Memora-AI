from model import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

        self.view.bind_open_directory_button(self.on_open_directory_clicked)
        self.view.bind_search_button(self.on_search_clicked)
        self.view.bind_show_all_button(self.on_show_all_clicked)
        self.view.bind_add_button(self.on_add_clicked)
        self.view.bind_manual_add_button(self.on_manual_add_clicked)
        self.view.bind_add_all_button(self.on_add_all_clicked)
        self.view.bind_remove_button(self.on_remove_clicked)
        self.view.bind_reanalyze_button(self.on_reanalyze_clicked)
        self.view.bind_open_button(self.on_open_clicked)
        self.view.bind_edit_image_text_button(self.on_edit_image_text_clicked)
        self.view.bind_edit_tags_button(self.on_edit_tags_clicked)
        self.view.bind_change_active_file_button(self.on_change_active_file_clicked)


    def on_open_directory_clicked(self):
        new_directory = self.view.ask_for_directory()
        if not new_directory:
            return
        self.model.set_active_directory(new_directory)

        if not self.model.database_file_exists():
            if "No" == self.view.choice_message_box("A database has not yet been set up for this directory, would you like to create one?"):
                return
            create_database_file = True
        else:
            create_database_file = False

        try:
            self.model.open_database(create_database_file, False)
        except Exception as e:
            if "No" == self.view.choice_message_box(f"{str(e)}, would you like to clean the database? All your images will still be in the folder and will not be touched."):
                return
            else:
                self.model.open_database(create_database_file, True)

        active_directory = self.model.get_active_directory()
        files_in_database = self.model.get_files_in_database()
        files_not_in_database = self.model.get_files_not_in_database()

        self.view.open_directory(self, active_directory, files_in_database, files_not_in_database)

    
    def on_search_clicked(self):
        query = self.view.get_query()
        result_list = self.model.search_database(query)
        self.view.search(result_list)


    def on_show_all_clicked(self):
        self.view.show_all()


    def on_change_active_file_clicked(self, new_file_name):
        self.model.set_active_file_name(new_file_name)
        image_text = self.model.get_image_text()
        tags = self.model.get_tags()
        self.view.change_active_file(new_file_name, image_text, tags)


    def on_add_clicked(self):
        try:
            self.model.add_entry()
            image_text = self.model.get_image_text()
            tags = self.model.get_tags()
            self.view.add(image_text, tags)
        except Exception as e:
            self.view.error_message_box(str(e))


    def on_manual_add_clicked(self):
        image_text = self.view.get_new_image_text()
        tags = self.view.get_new_tags()
        self.model.manual_add_entry(image_text, tags)
        self.view.manual_add()


    def on_add_all_clicked(self):
        try:
            returns = self.model.add_all(self.view.update_task_progress)
            bad_files = returns[0]
            good_files = returns[1]
            if bad_files != []:
                self.view.error_message_box("The following files failed:\n" + "\n".join(bad_files))
        except Exception as e:
            self.view.error_message_box(str(e))

        image_text = self.model.get_image_text()
        tags = self.model.get_tags()
        calls = len(good_files+bad_files)
        self.view.add_all(good_files, image_text, tags, calls)


    def on_remove_clicked(self):
        self.model.remove_entry()
        image_text = self.model.get_image_text()
        tags = self.model.get_tags()
        self.view.remove(image_text, tags)

    
    def on_reanalyze_clicked(self):
        try:
            self.model.reanalyze_entry()
            image_text = self.model.get_image_text()
            tags = self.model.get_tags()
            self.view.reanalyze(image_text, tags)
        except Exception as e:
            self.view.error_message_box(str(e))


    def on_open_clicked(self):
        self.view.open()


    def on_edit_image_text_clicked(self):
        new_image_text = self.view.get_new_image_text()
        self.model.edit_image_text(new_image_text)
        self.view.edit_image_text()


    def on_edit_tags_clicked(self):
        new_tags = self.view.get_new_tags()
        self.model.edit_tags(new_tags)
        self.view.edit_tags()