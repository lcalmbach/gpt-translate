import os
import openai
import json
from helper import get_var

import const

class Translator:
    def __init__(self, json_input: dict):
        self.language_json = json_input

    def get_completion_from_messages(
        self, messages, model="gpt-3.5-turbo", temperature=0, max_tokens=2000
    ):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"]

    def get_source_file(file_path):
        """The get_source_file function takes in a file path as an argument 
        and returns a JSON object loaded from the file. The function uses 
        the "with...as" statement to open the file, reads its contents as a JSON 
        object and finally returns the JSON object.

        Args:
            file_path (_type_): file in json fomrat

        Returns:
            obj: content from json file as object
        """
        with open(file_path, "r") as file:
            # Load the contents of the file as a JSON object
            lang = json.load(file)
        return lang

    def complete_source_to_input(self, source_dict: dict):
        result = source_dict.copy()
        source_lang = next(iter(source_dict))
        expressions_en = source_dict[source_lang]
        for lang in source_dict:
            if lang != source_lang:
                for expr_key, expr_value in expressions_en.items():
                    if not (expr_key in source_dict[lang]):
                        result[lang][expr_key] = ""
        return result

    def save_json_file(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file)

    def get_input(self, dat_dict):
        result = {}
        source_lang = next(iter(dat_dict))
        for lang, value in dat_dict.items():
            result[lang] = []
            if lang == source_lang:
                result[lang] = value
            else:
                result[lang] = []
                for expr_key, expr_value in value.items():
                    result[lang].append(expr_key)
        return result

    def parse_gpt_output(self, translated_dict: dict, source_dict: dict):
        """_summary_

        Args:
            translated_dict (dict): dict with translations: only expressions
                                    marked in the source file to be translated are
                                    included.
            source_dict (dict):     dict including all expressions this structure is overwritten with translated texts

        Returns:
            _type_: _description_
        """
        for lang, expressions in translated_dict.items():
            for expr_key, expr_value in expressions.items():
                source_dict[lang][expr_key] = expr_value
        return source_dict

    def translate(self):
        """
        Uses OpenAI's GPT-3 to automatically translate texts from one language to another.
    
        Returns a dictionary with the translated texts. Note that this method requires the
        OPENAI_API_KEY environment variable to be set with a valid API key for OpenAI's GPT-3 service.
    
        By default, this method translates texts to English (the 'en' language code). To change the
        target language, modify the `self.language_json` attribute before calling this method.
    
        This method generates a prompt message and submits it to the GPT-3 API. The prompt message
        includes the contents of `self.language_json`, which contains a list of texts to translate.
    
        The API response is parsed to obtain the translated texts, which are returned as a
        dictionary with the original texts as keys and the translated texts as values.
    
        Example usage:
        >> translator = MyTranslator()
        >> result = translator.translate()
        >> # result will be a dictionary with the translated texts
        """

        openai.api_key = get_var("OPENAI_API_KEY")
        completed_language_json = self.complete_source_to_input(self.language_json)

        gpt_input = self.get_input(completed_language_json)
        user_message = f"Translate the following texts: ####{json.dumps(gpt_input)}####"
        messages = [
            {"role": "system", "content": const.system_message},
            {"role": "user", "content": user_message},
        ]
        response = self.get_completion_from_messages(messages)
        translated_dict = self.parse_gpt_output(
            json.loads(response), completed_language_json
        )
        return translated_dict
