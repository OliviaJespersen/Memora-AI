import os

from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from tkinter.filedialog import askdirectory


class GraphicalUserInterface:
    def __init__(self, open_directory, search, show_all, change_active_file, add, remove, add_all, manual_add, reanalyze, open, edit_image_text, edit_tags):
        self.open_directory_button = open_directory
        self.search_button = search
        self.show_all_button = show_all 
        self.change_active_file_button = change_active_file
        self.add_button = add
        self.remove_button = remove
        self.add_all_button = add_all
        self.manual_add_button = manual_add
        self.reanalyze_button = reanalyze
        self.open_button = open
        self.edit_image_text_button = edit_image_text
        self.edit_tags_button = edit_tags

        self.call_count = None
        self.active_directory = None
        self.active_file_name = None
        self.active_image_text = None
        self.active_tags = None
        self.files_in_db = None
        self.files_not_in_db = None
    

    def build_gui(self, placeholder_image, icon, call_count):
        window = ttk.Window(title="Memora AI", themename="darkly", resizable=(False, False))
        window.iconbitmap(icon)

        frm_left_bar = ttk.Frame(master=window, height=700, width=400)
        frm_left_bar.pack_propagate(False)
        frm_left_bar.grid(column=0, row=0, padx=(20,6), pady=20, sticky=NSEW)
        
        frm_right_bar = ttk.Frame(master=window, height=700, width=400)
        frm_right_bar.pack_propagate(False)
        frm_right_bar.grid(column=1, row=0, padx=(6,20), pady=20, sticky=NSEW)

        frm_directory = ttk.Frame(master=frm_left_bar, style=SECONDARY)
        frm_directory.pack(fill=X, pady=(0,10))
        
        btn_directory_open = ttk.Button(master=frm_directory, command=self.open_directory_button, style=SUCCESS, text="Open")
        btn_directory_open.pack(side=RIGHT)
        
        self.lbl_directory = ttk.Label(master=frm_directory, style=(INVERSE, SECONDARY), text="Open a directory")
        self.lbl_directory.pack(side=LEFT, padx=(6,0))

        frm_buttons = ttk.Frame(master=frm_left_bar)
        frm_buttons.columnconfigure([0,1,2], uniform="equal", weight=1)
        frm_buttons.pack(fill=X, side=BOTTOM)

        self.btn_add = ttk.Button(master=frm_buttons, command=self.add_button, state=DISABLED, text="Add")
        self.btn_add.grid(column=0, row=0, padx=(0,8), pady=(10,6), sticky=EW)
        
        self.btn_manual_add = ttk.Button(master=frm_buttons, command=self.manual_add_button, state=DISABLED, text="Manual Add")
        self.btn_manual_add.grid(column=1, row=0, padx=4, pady=(10,6), sticky=EW)

        self.btn_add_all = ttk.Button(master=frm_buttons, command=self.add_all_button, state=DISABLED, text="Add all")
        self.btn_add_all.grid(column=2, row=0, padx=(8,0), pady=(10,6), sticky=EW)
        
        self.btn_remove = ttk.Button(master=frm_buttons, command=self.remove_button, state=DISABLED, text="Remove")
        self.btn_remove.grid(column=0, row=1, padx=(0,8), pady=(6,0), sticky=EW)
        
        self.btn_reanalyze = ttk.Button(master=frm_buttons, command=self.reanalyze_button, state=DISABLED, text="Reanalyze")
        self.btn_reanalyze.grid(column=1, row=1, padx=4, pady=(6,0), sticky=EW)
        
        self.btn_open = ttk.Button(master=frm_buttons, command=self.open_button, state=DISABLED, text="Open")
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
        
        self.btn_search = ttk.Button(master=frm_search, command=self.search_button, state=DISABLED, text="Search")
        self.btn_search.pack(side=LEFT)
        
        self.btn_show_all = ttk.Button(master=frm_search, command=self.show_all_button, state=DISABLED, text="Show all")
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
        
        self.btn_tags_edit = ttk.Button(master=frm_tags, command=self.edit_tags_button, state=DISABLED, text="Edit")
        self.btn_tags_edit.grid(column=1, row=0, sticky=NS)

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

        self.btn_image_text_edit = ttk.Button(master=frm_image_text, command=self.edit_image_text_button, state=DISABLED, text="Edit")
        self.btn_image_text_edit.grid(column=1, row=0, sticky=NS)

        self.lbl_image_name = ttk.Label(master=frm_right_bar, text="Select an image to get started!")
        self.lbl_image_name.pack(pady=(0,10))

        self.lbl_image = ttk.Label(master=frm_right_bar, image=self._make_tk_image(placeholder_image))
        self.lbl_image.pack()

        window.mainloop()


    def open_directory(self, active_directory, files_in_db, files_not_in_db):
        self.active_directory = active_directory
        self.lbl_directory.configure(text=os.path.basename(self.active_directory))
        for button in [self.btn_add_all, self.btn_search, self.btn_show_all]:
            button.configure(state=ACTIVE)

        self.files_in_db = files_in_db
        self.files_not_in_db = files_not_in_db

        self._update_file_list()


    def search(self, file_list):
        self._update_file_list(file_list)


    def show_all(self):
        self._update_file_list()


    def change_active_file(self, file_name, image_text, tags):
        self.active_file_name = file_name
        self.active_image_text = image_text
        self.active_tags = tags

        self.lbl_image.configure(image=self._make_tk_image(self.active_directory+"/"+self.active_file_name))
        for entry in [self.ent_image_text, self.ent_tags]:
            entry.delete(0, END)
        self.ent_image_text.insert(END, self.active_image_text)
        self.ent_tags.insert(END, self.active_tags)
        self.lbl_image_name.configure(text=self.active_file_name)

        states = [ACTIVE, DISABLED, DISABLED, ACTIVE, ACTIVE, ACTIVE, ACTIVE] if self.active_file_name in self.files_in_db else [ACTIVE, ACTIVE, ACTIVE, DISABLED, DISABLED, DISABLED, DISABLED]
        buttons = [self.btn_open, self.btn_manual_add, self.btn_add, self.btn_remove, self.btn_reanalyze, self.btn_image_text_edit, self.btn_tags_edit]
        for i in range(len(buttons)):
            buttons[i].configure(state=states[i])


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


    def add_all(self, new_file_names, image_text, tags, call_count):
        self.files_in_db += new_file_names
        self.files_not_in_db = [file_name for file_name in self.files_not_in_db if not file_name in new_file_names]
        self.change_active_file(self.active_file_name, image_text, tags)
        self._update_file_list()

        self.lbl_task_progress.configure(text="No task in progress")
        self.call_count = call_count
        self._update_call_counter(self.call_count)


    def manual_add(self):
        self.files_in_db += [self.active_file_name]
        self.files_not_in_db.remove(self.active_file_name)
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
        self.lbl_task_progress.configure(text=f"Progress: {count}/{total}")
        self.lbl_task_progress.update()


    def setup_error(self, error_message):
        window = ttk.Window(title="Critical Error", themename="darkly", size=(200,100))
        label = ttk.Label(master=window, text=f"An error was encountered:\n{error_message}")
        label.place(relx=0.5, rely=0.5, anchor=CENTER)
        window.mainloop()


    def _make_tk_image(self, file_path):
        global tk_image

        image = Image.open(file_path)
        tk_image = ImageTk.PhotoImage(image.resize((400,int((image.height / image.width * 400)))))
        return tk_image


    def _update_file_list(self, file_list=None):
        for widget in self.frm_file_list.winfo_children():
            widget.destroy()

        for file_name in (sorted(self.files_in_db) + sorted(self.files_not_in_db) if not file_list else file_list):
            label = ttk.Label(master=self.frm_file_list, text=file_name, bootstyle=SUCCESS if file_name in self.files_in_db else SECONDARY)
            label.pack(anchor=W)
            label.bind("<Button-1>", lambda event, new_file=file_name: self.change_active_file_button(new_file))
            separator = ttk.Separator(master=self.frm_file_list)
            separator.pack(fill=X)


    def _update_call_counter(self, count):
        self.lbl_call_counter.configure(text=f"API calls today: {count}/1500")
