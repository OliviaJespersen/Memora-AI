import os

from model import Model
from view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

        self.view.bind_buttons("open_directory", self.on_open_directory_clicked)
        self.view.bind_buttons("search", self.on_search_clicked)
        self.view.bind_buttons("show_all", self.on_show_all_clicked)
        self.view.bind_buttons("add", self.on_add_clicked)
        self.view.bind_buttons("manual_add", self.on_manual_add_clicked)
        self.view.bind_buttons("add_all", self.on_add_all_clicked)
        self.view.bind_buttons("remove", self.on_remove_clicked)
        self.view.bind_buttons("reanalyze", self.on_reanalyze_clicked)
        self.view.bind_buttons("open", self.on_open_clicked)
        self.view.bind_buttons("edit_image_text", self.on_edit_image_text_clicked)
        self.view.bind_buttons("edit_tags", self.on_edit_tags_clicked)
        self.view.set_file_change_command(self.on_change_active_file_clicked)

        self.update_view(reset=True)

    def on_open_directory_clicked(self):
        new_directory = self.view.ask_for_directory()
        if not new_directory:
            return
        self.model.set_active_directory(new_directory)

        if not self.model.database_file_exists():
            if "No" == self.view.choice_message_box(
                "A database has not yet been set up for this directory, would you like to create one?"
            ):
                return
            create_database_file = True
        else:
            create_database_file = False

        try:
            self.model.open_database(create_database_file)
        except Exception as e:
            self.view.error_message_box(str(e))

        self.update_view(reset=True, interface=True, file_list=True)

    def on_search_clicked(self):
        query = self.view.get_query()
        result_list = self.model.search_database(query)

        self.update_view(file_list=True, search=True, result_list=(result_list, []))

    def on_show_all_clicked(self):
        self.update_view(file_list=True)

    def on_change_active_file_clicked(self, new_file_name):
        self.model.set_active_file_name(new_file_name)

        self.update_view(file=True)

    def on_add_clicked(self):
        try:
            self.model.add_entry()

            self.update_view(interface=True, file=True, file_list=True)
        except Exception as e:
            self.view.error_message_box(str(e))

    def on_manual_add_clicked(self):
        image_text = self.view.get_new_image_text()
        tags = self.view.get_new_tags()
        self.model.manual_add_entry(image_text, tags)

        self.update_view(file=True, file_list=True)

    def on_add_all_clicked(self):
        try:
            bad_files = self.model.add_all(self.view.update_task_progress)
            if bad_files != []:
                self.view.error_message_box(
                    "The following files failed:\n" + "\n".join(bad_files)
                )
        except Exception as e:
            self.view.error_message_box(str(e))

        if self.model.get_active_file_name():
            self.update_view(file=True)
        self.update_view(interface=True, file_list=True)

    def on_remove_clicked(self):
        self.model.remove_entry()

        self.update_view(file=True, file_list=True)

    def on_reanalyze_clicked(self):
        try:
            self.model.reanalyze_entry()

            self.update_view(interface=True, file=True)
        except Exception as e:
            self.view.error_message_box(str(e))

    def on_open_clicked(self):
        image_path = (
            self.model.get_active_directory() + "/" + self.model.get_active_file_name()
        )
        self.view.open(image_path)

    def on_edit_image_text_clicked(self):
        new_image_text = self.view.get_new_image_text()
        self.model.edit_image_text(new_image_text)

        self.view.toast_message_box("Saved successfully")

    def on_edit_tags_clicked(self):
        new_tags = self.view.get_new_tags()
        self.model.edit_tags(new_tags)

        self.view.toast_message_box("Saved successfully")

    def update_view(
        self,
        reset=False,
        interface=False,
        file=False,
        file_list=False,
        search=False,
        result_list=([], []),
    ):
        if reset:
            self.view.set_directory_name("Open a directory")
            self.view.update_buttons("reset")
            self.view.show_files([], [])
            self.view.reset_task_progress()
            self.view.update_call_counter(self.model.get_call_count())
            self.view.set_image()
            self.view.set_image_text("Image text")
            self.view.set_tags("Tags")

        if interface:
            active_directory = self.model.get_active_directory()
            self.view.set_directory_name(os.path.basename(active_directory))
            self.view.update_buttons("open_database")
            self.view.reset_task_progress()
            self.view.update_call_counter(self.model.get_call_count())

        if file:
            in_database = (
                self.model.get_active_file_name() in self.model.get_files_in_database()
            )
            self.view.update_buttons(
                "in_database" if in_database else "not_in_database"
            )
            image_path = (
                self.model.get_active_directory()
                + "/"
                + self.model.get_active_file_name()
            )
            self.view.set_image(image_path, self.model.get_active_file_name())
            image_text = self.model.get_image_text()
            self.view.set_image_text(image_text)
            tags = self.model.get_tags()
            self.view.set_tags(tags)

        if file_list:
            if search:
                self.view.show_files(result_list[0], result_list[1])
            else:
                files_in_database = self.model.get_files_in_database()
                files_not_in_database = self.model.get_files_not_in_database()
                self.view.show_files(files_in_database, files_not_in_database)
