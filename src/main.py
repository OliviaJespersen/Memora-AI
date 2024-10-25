import json
import os
import sys

import ttkbootstrap as ttk

from model import Model
from view import View
from controller import Controller
from ai_image_analysis import AiImageAnalysis
from daily_api_call_counter import DailyApiCallCounter


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def read_config_file(file_path):
    try:
        with open(file_path, "r") as config_file:
            config_data = json.load(config_file)
    except FileNotFoundError:
        raise Exception("Config file was not found")
    except json.JSONDecodeError:
        raise Exception("Config file was corrupted")
    if not "api_key" in config_data or not config_data["api_key"] or config_data["api_key"] == "Your Gemini API key goes here":
        raise Exception("API key was not set in config file")
    if not "theme" in config_data or not config_data["theme"]:
        raise Exception("Theme was not set in the config file")
    
    return config_data


def main():

    try:
        config_data = read_config_file(resource_path("config/config.json"))
        
        gemini_ai = AiImageAnalysis(config_data["api_key"])
        call_counter = DailyApiCallCounter(resource_path("data/calls.json"))
        model = Model(gemini_ai, call_counter)

        window = ttk.Window(title="Memora AI", themename=config_data["theme"], resizable=(False, False))
        view = View(window)
        icon = resource_path("resources/boykisser.ico")
        window.iconbitmap(bitmap=icon)
        window.iconbitmap(default=icon)
        view.build_gui(resource_path("resources/placeholder.png"), call_counter.get_count())
        
        Controller(model, view)
    except Exception as e:
        window = ttk.Window(title="ERROR!", themename="darkly")
        view = View(window)
        view.error_message_box(str(e))
        quit()

    window.mainloop()

if __name__ == "__main__":
    main()