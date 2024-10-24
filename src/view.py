import os

from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from tkinter.filedialog import askdirectory


class View:
    def __init__(self, window):
        self.window = window
        self.call_count = None
        self.active_directory = None
        self.active_file_name = None
        self.active_image_text = None
        self.active_tags = None
        self.files_in_db = None
        self.files_not_in_db = None
        self.change_active_file_button = None
    

    def build_gui(self, placeholder_image, call_count):
        frm_left_bar = ttk.Frame(master=self.window, height=700, width=400)
        frm_left_bar.pack_propagate(False)
        frm_left_bar.grid(column=0, row=0, padx=(20,6), pady=20, sticky=NSEW)
        
        frm_right_bar = ttk.Frame(master=self.window, height=700, width=400)
        frm_right_bar.pack_propagate(False)
        frm_right_bar.grid(column=1, row=0, padx=(6,20), pady=20, sticky=NSEW)

        frm_directory = ttk.Frame(master=frm_left_bar, style=SECONDARY)
        frm_directory.pack(fill=X, pady=(0,10))
        
        self.btn_open_directory = ttk.Button(master=frm_directory, style=SUCCESS, text="Open")
        self.btn_open_directory.pack(side=RIGHT)
        
        self.lbl_directory = ttk.Label(master=frm_directory, style=(INVERSE, SECONDARY), text="Open a directory")
        self.lbl_directory.pack(side=LEFT, padx=(6,0))

        frm_buttons = ttk.Frame(master=frm_left_bar)
        frm_buttons.columnconfigure([0,1,2], uniform="equal", weight=1)
        frm_buttons.pack(fill=X, side=BOTTOM)

        self.btn_add = ttk.Button(master=frm_buttons, state=DISABLED, text="Add")
        self.btn_add.grid(column=0, row=0, padx=(0,8), pady=(10,6), sticky=EW)
        
        self.btn_manual_add = ttk.Button(master=frm_buttons, state=DISABLED, text="Manual Add")
        self.btn_manual_add.grid(column=1, row=0, padx=4, pady=(10,6), sticky=EW)

        self.btn_add_all = ttk.Button(master=frm_buttons, state=DISABLED, text="Add all")
        self.btn_add_all.grid(column=2, row=0, padx=(8,0), pady=(10,6), sticky=EW)
        
        self.btn_remove = ttk.Button(master=frm_buttons, state=DISABLED, text="Remove")
        self.btn_remove.grid(column=0, row=1, padx=(0,8), pady=(6,0), sticky=EW)
        
        self.btn_reanalyze = ttk.Button(master=frm_buttons, state=DISABLED, text="Reanalyze")
        self.btn_reanalyze.grid(column=1, row=1, padx=4, pady=(6,0), sticky=EW)
        
        self.btn_open = ttk.Button(master=frm_buttons, state=DISABLED, text="Open")
        self.btn_open.grid(column=2, row=1, padx=(8,0), pady=(6,0), sticky=EW)

        self.lbl_call_counter = ttk.Label(master=frm_left_bar)
        self.call_count = call_count
        self._update_call_counter(self.call_count)
        self.lbl_call_counter.pack(side=BOTTOM)

        self.lbl_task_progress = ttk.Label(master=frm_left_bar, text="No task in progress")
        self.lbl_task_progress.pack(side=BOTTOM, pady=(10,0))

        self.frm_file_browser = ttk.Frame(master=frm_left_bar)
        self.frm_file_browser.pack(fill=X)

        frm_search = ttk.Frame(master=self.frm_file_browser)
        frm_search.pack(fill=X, pady=(10,0))
        
        self.btn_search = ttk.Button(master=frm_search, state=DISABLED, text="Search")
        self.btn_search.pack(side=LEFT)
        
        self.btn_show_all = ttk.Button(master=frm_search, state=DISABLED, text="Show all")
        self.btn_show_all.pack(side=RIGHT)
        
        self.ent_search = ttk.Entry(master=frm_search)
        self.ent_search.pack(fill=X)

        self.frm_file_list = ScrolledFrame(master=self.frm_file_browser, height=999)
        self.frm_file_list.pack(fill=X)

        frm_tags = ttk.Frame(master=frm_right_bar)
        frm_tags.columnconfigure(0, weight=1)
        frm_tags.columnconfigure(1, weight=0)
        frm_tags.pack(fill=X, side=BOTTOM, pady=(12,0))
        
        frm_tags_box = ttk.Frame(master=frm_tags)
        frm_tags_box.grid(column=0, row=0)
        
        srb_tags = ttk.Scrollbar(master=frm_tags_box, orient=HORIZONTAL)
        srb_tags.pack(fill=X, side=BOTTOM)
        
        self.ent_tags = ttk.Entry(master=frm_tags_box, width=999, xscrollcommand=srb_tags.set)
        self.ent_tags.insert(0, "Tags")
        self.ent_tags.pack(fill=X)
        srb_tags.config(command=self.ent_tags.xview)
        
        self.btn_edit_tags = ttk.Button(master=frm_tags, state=DISABLED, text="Edit")
        self.btn_edit_tags.grid(column=1, row=0, sticky=NS)

        frm_image_text = ttk.Frame(master=frm_right_bar)
        frm_image_text.columnconfigure(0, weight=1)
        frm_image_text.columnconfigure(1, weight=0)
        frm_image_text.pack(fill=X, side=BOTTOM, pady=(12,0))

        frm_image_text_box = ttk.Frame(master=frm_image_text)
        frm_image_text_box.grid(column=0, row=0)
        
        srb_image_text = ttk.Scrollbar(master=frm_image_text_box, orient=HORIZONTAL)
        srb_image_text.pack(fill=X, side=BOTTOM)

        self.ent_image_text = ttk.Entry(master=frm_image_text_box, width=999, xscrollcommand=srb_image_text.set)
        self.ent_image_text.insert(0, "Image Text")
        self.ent_image_text.pack(fill=X)
        srb_image_text.config(command=self.ent_image_text.xview)

        self.btn_edit_image_text = ttk.Button(master=frm_image_text, state=DISABLED, text="Edit")
        self.btn_edit_image_text.grid(column=1, row=0, sticky=NS)

        self.lbl_image_name = ttk.Label(master=frm_right_bar, text="Select an image to get started!")
        self.lbl_image_name.pack(pady=(0,10))

        self.lbl_image = ttk.Label(master=frm_right_bar, image=self._make_tk_image(placeholder_image))
        self.lbl_image.pack()


    def bind_open_directory_button(self, callback):
        self.btn_open_directory.config(command=callback)

    
    def bind_add_button(self, callback):
        self.btn_add.config(command=callback)

    
    def bind_manual_add_button(self, callback):
        self.btn_manual_add.config(command=callback)

    
    def bind_add_all_button(self, callback):
        self.btn_add_all.config(command=callback)

    
    def bind_remove_button(self, callback):
        self.btn_remove.config(command=callback)


    def bind_reanalyze_button(self, callback):
        self.btn_reanalyze.config(command=callback)


    def bind_open_button(self, callback):
        self.btn_open.config(command=callback)


    def bind_search_button(self, callback):
        self.btn_search.config(command=callback)


    def bind_show_all_button(self, callback):
        self.btn_show_all.config(command=callback)


    def bind_edit_tags_button(self, callback):
        self.btn_edit_tags.config(command=callback)


    def bind_edit_image_text_button(self, callback):
        self.btn_edit_image_text.config(command=callback)


    def bind_change_active_file_button(self, callback):
        self.change_active_file_button = callback


    def open_directory(self, active_directory, files_in_db, files_not_in_db):
        self.active_directory = active_directory
        self.lbl_directory.config(text=os.path.basename(self.active_directory))
        for button in [self.btn_add_all, self.btn_search, self.btn_show_all]:
            button.config(state=ACTIVE)

        self.files_in_db = files_in_db
        self.files_not_in_db = files_not_in_db

        self._update_file_list()


    def search(self, file_list):
        self._show_files(file_list, [])


    def show_all(self):
        self._update_file_list()


    def change_active_file(self, file_name, image_text, tags):
        self.active_file_name = file_name
        self.active_image_text = image_text
        self.active_tags = tags

        self.lbl_image.config(image=self._make_tk_image(self.active_directory+"/"+self.active_file_name))
        for entry in [self.ent_image_text, self.ent_tags]:
            entry.delete(0, END)
        self.ent_image_text.insert(END, self.active_image_text)
        self.ent_tags.insert(END, self.active_tags)
        self.lbl_image_name.config(text=self.active_file_name)

        states = [ACTIVE, DISABLED, DISABLED, ACTIVE, ACTIVE, ACTIVE, ACTIVE] if self.active_file_name in self.files_in_db else [ACTIVE, ACTIVE, ACTIVE, DISABLED, DISABLED, DISABLED, DISABLED]
        buttons = [self.btn_open, self.btn_manual_add, self.btn_add, self.btn_remove, self.btn_reanalyze, self.btn_edit_image_text, self.btn_edit_tags]
        for i in range(len(buttons)):
            buttons[i].config(state=states[i])


    def add(self, image_text, tags):
        self.files_in_db += [self.active_file_name]
        self.files_not_in_db.remove(self.active_file_name)
        self.change_active_file(self.active_file_name, image_text, tags)
        self._update_file_list()
        self.call_count += 1
        self._update_call_counter(self.call_count)


    def remove(self, image_text, tags):
        self.files_not_in_db += [self.active_file_name]
        self.files_in_db.remove(self.active_file_name)
        self.change_active_file(self.active_file_name, image_text, tags)
        self._update_file_list()


    def add_all(self, new_file_names, image_text, tags, calls):
        self.files_in_db += new_file_names
        self.files_not_in_db = [file_name for file_name in self.files_not_in_db if not file_name in new_file_names]
        self.change_active_file(self.active_file_name, image_text, tags)
        self._update_file_list()

        self.lbl_task_progress.config(text="No task in progress")
        self.call_count += calls
        self._update_call_counter(self.call_count)


    def manual_add(self):
        self.files_in_db += [self.active_file_name]
        self.files_not_in_db.remove(self.active_file_name)
        self.active_image_text = self.get_new_image_text()
        self.active_tags = self.get_new_tags()
        self.change_active_file(self.active_file_name, self.active_image_text, self.active_tags)
        self._update_file_list()


    def reanalyze(self, image_text, tags):
        self.change_active_file(self.active_file_name, image_text, tags)
        self.call_count += 1
        self._update_call_counter(self.call_count)


    def open(self):
        Image.open(self.active_directory+"/"+self.active_file_name).show()


    def edit_image_text(self):
        ToastNotification(title="Saved successfully", message="The edit made to the image-text were successfully saved", duration=5000, bootstyle=SUCCESS, alert=True, icon=":3").show_toast()


    def edit_tags(self):
        ToastNotification(title="Saved successfully", message="The edit made to the image tags were successfully saved", duration=5000, bootstyle=SUCCESS, alert=True, icon=":3").show_toast()


    def get_new_image_text(self):
        return self.ent_image_text.get()


    def get_new_tags(self):
        return self.ent_tags.get()


    def get_query(self):
        return self.ent_search.get()


    def info_message_box(self, message):
        Messagebox.show_info(message=message)


    def choice_message_box(self, message):
        return Messagebox.yesno(message)


    def error_message_box(self, message):
        Messagebox.show_error(message=message)


    def ask_for_directory(self):
        return askdirectory()


    def update_task_progress(self, count, total):
        self.lbl_task_progress.config(text=f"Progress: {count}/{total}")
        self.lbl_task_progress.update()


    def _make_tk_image(self, file_path):
        global tk_image

        image = Image.open(file_path)
        tk_image = ImageTk.PhotoImage(image.resize((400,int((image.height / image.width * 400)))))
        return tk_image


    def _update_file_list(self):
        self._show_files(self.files_in_db, self.files_not_in_db)


    def _show_files(self, files_in_db, files_not_in_db):
        for widget in self.frm_file_list.winfo_children():
            widget.destroy()

        for file_name in (sorted(files_in_db) + sorted(files_not_in_db)):
            label = ttk.Label(master=self.frm_file_list, text=file_name, bootstyle=SUCCESS if file_name in files_in_db else SECONDARY)
            label.pack(anchor=W)
            label.bind("<Button-1>", lambda event, new_file=file_name: self.change_active_file_button(new_file))
            separator = ttk.Separator(master=self.frm_file_list)
            separator.pack(fill=X)


    def _update_call_counter(self, count):
        self.lbl_call_counter.config(text=f"API calls today: {count}/1500")
