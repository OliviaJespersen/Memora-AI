import ast
import json

from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as gemini
import PIL.Image


class AiImageAnalysis:
    def __init__(self, config_file_path):
        try:
            with open(config_file_path, "r") as config_file:
                config_data = json.load(config_file)
        except FileNotFoundError:
            raise Exception("Config file was not found")
        except json.JSONDecodeError:
            raise Exception("Config file was corrupted")
        if not "api_key" in config_data or not config_data["api_key"] or config_data["api_key"] == "Your Gemini API key goes here":
            raise Exception("API key was not set in config file")
        try:
            gemini.configure(api_key=config_data["api_key"])
        except:
            raise Exception("Gemini failed to set the API key")

    
    def generate_description(self, file_path):
        prompt = """Please provide a two part description of this image with the following structure like a python list tuple(str, list[str]):
("Any and all text in the image", [A collection of key words that comprehensively describe the contents and themes of the image])
Follow these rules.
Rule 1: Use no line breaks.
Rule 2: Do not leave any image text out of the first string. Make sure you have it all.
Rule 3: If two parts of the image have separate text, separate them with a comma in the first string.
Rule 4: If there is no text in the image, write "no text" instead for the first string.
Rule 5: If you find that the image contains aspects that are way too inappropriate to describe, just be vague about those aspects."""

        try:
            response = gemini.GenerativeModel("gemini-1.5-flash").generate_content([prompt, PIL.Image.open(file_path)],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }).text
        except:
            raise Exception("Fuck! Looks like the AI pissed itself")
        
        try:
            return self.response_to_description(response)
        except:
            error_message = response.replace("\n", " ")
            raise ValueError(f"The AI gave an unusable response:\n{error_message}")


    def response_to_description(self, response):
        object = ast.literal_eval(response)

        if isinstance(object, tuple):
            if isinstance(object[0], str): 
                if isinstance(object[1], list):
                    if all(isinstance(tag, str) for tag in object[1]):
                        return (object[0], ', '.join(object[1]))
        raise Exception()
