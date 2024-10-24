import os
import sys

import ttkbootstrap as ttk

from model import Model
from view import View
from controller import Controller
from ai_image_analysis import AiImageAnalysis
from daily_api_call_counter import DailyApiCallCounter


def _resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def main():
    window = ttk.Window(title="Memora AI", themename="darkly", resizable=(False, False))
    view = View(window)
    icon = _resource_path("resources/boykisser.ico")
    window.iconbitmap(bitmap=icon)
    window.iconbitmap(default=icon)

    try:
        gemini_ai = AiImageAnalysis(_resource_path("config/config.json"))
        call_counter = DailyApiCallCounter(_resource_path("data/calls.json"))
        view.build_gui(_resource_path("resources/placeholder.png"), call_counter.get_count())
        model = Model(gemini_ai, call_counter)
        Controller(model, view)
    except Exception as e:
        view.error_message_box(str(e))
        quit()

    window.mainloop()

if __name__ == "__main__":
    main()