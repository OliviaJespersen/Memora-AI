import os
import time

import daily_api_call_counter
import database_management_system
import ai_image_analysis
import graphical_user_interface

gemini_ai = ai_image_analysis.AiImageAnalysis("/Users/oliviajespersen/Documents/Memora AI/config.json")
call_counter = daily_api_call_counter.DailyApiCallCounter("/Users/oliviajespersen/Documents/Memora AI/calls.json")
active_directory = None
active_file_name = None
image_database = None
user_interface = None


def open_directory():
    global active_directory
    global image_database

    new_directory = user_interface.ask_for_directory()
    if not new_directory:
        return
    
    database_file_path = new_directory+"/"+"database.json"
    if not os.path.exists(database_file_path):
        if "No" == user_interface.choice_message_box("A database has not yet been set up for this directory, would you like to create one?"):
            return
        image_database = database_management_system.DatabaseManagementSystem(database_file_path, True)
    else:
        image_database = database_management_system.DatabaseManagementSystem(database_file_path, False)
    
    active_directory = new_directory

    supported_file_list = [file for file in os.listdir(active_directory) if _is_supported_file(file)]
    files_in_db = [file for file in supported_file_list if image_database.in_database(file)]
    files_not_in_db = [file for file in supported_file_list if not image_database.in_database(file)]
    user_interface.open_directory(active_directory, files_in_db, files_not_in_db)


def search():
    user_interface.search(image_database.search_database(user_interface.get_query()))


def show_all():
    user_interface.show_all()


def change_active_file(new_file_name):
    global active_file_name

    active_file_name = new_file_name
    user_interface.change_active_file(new_file_name, image_database.get_image_text(new_file_name), image_database.get_tags(new_file_name))


def add():
    try:
        call_counter.new_call()
        image_database.add_entry(active_file_name, gemini_ai.generate_description(active_directory+"/"+active_file_name))
        user_interface.add(image_database.get_image_text(active_file_name), image_database.get_tags(active_file_name))
    except Exception as e:
        user_interface.error_message_box(str(e))


def remove():
    image_database.remove_entry(active_file_name)
    user_interface.remove(image_database.get_image_text(active_file_name), image_database.get_tags(active_file_name))


def add_all():
    try:
        cut_list = [file for file in os.listdir(active_directory) if _is_supported_file(file) and not image_database.in_database(file)][:1500 - call_counter.get_count()]
        chunk_list = [cut_list[i:i + 15] for i in range(0, len(cut_list), 15)]
        bad_files = []
        good_files = []
        file_counter = 0

        for chunk_nr in range(len(chunk_list)):
            start_time = time.time()
            for file_name in chunk_list[chunk_nr]:
                user_interface.update_task_progress(file_counter, len(cut_list))
                try:
                    call_counter.new_call()
                    image_database.add_entry(file_name, gemini_ai.generate_description(active_directory+"/"+file_name))
                    good_files += [file_name]
                except ValueError as e:
                    bad_files += [f"{file_name}: {str(e)}"]
                file_counter += 1
            end_time = time.time()

            if chunk_nr != len(chunk_list) - 1 and end_time - start_time < 60:
                time.sleep(60 - (end_time - start_time))

        if bad_files != []:
            user_interface.error_message_box("The following files failed:\n" + "\n".join(bad_files))
    except Exception as e:
        user_interface.error_message_box(str(e))
    
    user_interface.add_all(good_files, image_database.get_image_text(active_file_name), image_database.get_tags(active_file_name), call_counter.get_count())


def manual_add():
    image_database.add_entry(active_file_name, [user_interface.get_new_image_text(), user_interface.get_new_tags()])
    user_interface.manual_add()


def reanalyze():
    try:
        call_counter.new_call()
        image_database.reanalyze_entry(active_file_name)
        user_interface.reanalyze(image_database.get_image_text(active_file_name), image_database.get_tags(active_file_name))
    except Exception as e:
        user_interface.error_message_box(str(e))


def clean():
    nr_cleaned = image_database.clean()
    user_interface.clean(nr_cleaned)


def edit_image_text():
    image_database.edit_image_text(active_file_name, user_interface.get_new_image_text())
    user_interface.edit_image_text()


def edit_tags():
    image_database.edit_tags(active_file_name, user_interface.get_new_tags())
    user_interface.edit_tags()


def _is_supported_file(file_name):
    return os.path.splitext(file_name)[1].lower() in ['.jpeg', '.jpg', '.png', '.webp']


def main():
    global user_interface

    call_counter.clean()
    user_interface = graphical_user_interface.GraphicalUserInterface(open_directory, search, show_all, change_active_file, add, remove, add_all, manual_add, reanalyze, clean, edit_image_text, edit_tags, call_counter.get_count())
    user_interface.build_gui("/Users/oliviajespersen/Documents/Memora AI/placeholder.png")


if __name__ == "__main__":
    main()
