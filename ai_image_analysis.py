import json

from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as gemini
import PIL.Image


class AiImageAnalysis:
    def __init__(self, config_file_path):
        with open(config_file_path, "r") as config_file:
            config_data = json.load(config_file)
        gemini.configure(api_key=config_data["api_key"])
        
    
    def generate_description(self, file_path):
        prompt = """
        Please provide a two part description of this image.
        Separate the parts with a | character.
        Part 1: Any and all text in the image.
        Part 2: A collection of key words that comprehensively describe the contents and themes of the image.

        Follow these rules.
        Rule 1: Do not leave any text out of part 1.
        Rule 2: Use no linebreaks.
        Rule 3: If there is no text in the image, write "no text" instead.
        Rule 4: If you find that the image contains aspects that are way too inappropriate to describe, just be vague about those aspects.
        """

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
        if "|" not in response:
            error_message = response.replace("\n", " ")
            raise ValueError(f"The AI gave an unusable response:\n{error_message}")
        return [string.strip() for string in response.split("|")]

