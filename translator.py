import openai
import json
from helper import get_var, get_lang_name
import const


class Translator:
    def __init__(self, json_input: dict):
        self.language_json = json_input
        keys = json_input.keys()
        self.lang_list = list(keys)[1:]
        self.source_lang = self.lang_list[0]
        self.changed_items = self.get_changed_items()
        self.source_lang_full = get_lang_name(self.source_lang)
        self.info = self.get_info()

    def get_info(self):
        text = f"Target languages: {', '.join(self.lang_list)}"
        text += f"\n\r{len(self.changed_items)} changed items found"
        text += f"\n\rTranslation from {self.source_lang_full}"
        return text

    def get_changed_items(self):
        changes_items = []
        source = self.language_json["source"]
        source_lang = self.language_json[self.source_lang]
        for k, v in source.items():
            if k not in source_lang:
                changes_items.append(k)
            elif type(source[k]) == list:
                if not (k in source_lang):
                    changes_items.append(k)
                    break
                else:
                    for item in source[k]:
                        if not item.encode("utf-8") in [x.encode("utf-8") for x in source_lang[k]]:
                            changes_items.append(k)
                            break

            else:
                if v.encode("utf-8") != source_lang[k].encode("utf-8"):
                    changes_items.append(k)
        return changes_items

    def get_completion_from_messages(
        self, messages, model="gpt-3.5-turbo", temperature=0, max_tokens=3000
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

    def save_json_file(file_path, data):
        with open(file_path, "w") as file:
            json.dump(data, file)

    def parse_gpt_output(self, translated_dict: dict, source_dict: dict, lang):
        """_summary_

        Args:
            translated_dict (dict): dict with translations: only expressions
                                    marked in the source file to be translated are
                                    included.
            source_dict (dict):     dict including all expressions this structure is overwritten with translated texts

        Returns:
            _type_: _description_
        """
        result = {}
        for key in list(self.language_json["source"].keys()):
            # if key has been translated, use it is as previously translated
            if type(self.language_json["source"][key]) == list:
                if key in source_dict.keys():
                    result[key] = translated_dict[key]
                else:
                    result[key] = self.language_json[lang][key]
            else:
                if key in source_dict.keys():
                    result[key] = translated_dict[key]
                else:
                    result[key] = self.language_json[lang][key]
        return result

    def init_translation(self):
        translated = {}
        translated["source"] = self.language_json["source"]
        translated[self.source_lang] = self.language_json["source"]
        return translated

    def get_items_to_translate(self, lang):
        result = {}
        source = self.language_json["source"]
        target = self.language_json[lang]
        in_keys = list(source.keys())
        out_keys = list(target.keys())
        for key in in_keys:
            if type(source[key]) == list:
                if not key in out_keys or key in self.changed_items:
                    result[key] = source[key]
                elif target[key] == []:
                    result[key] = source[key]
            else:
                # item has not been created yet
                if not key in out_keys or key in self.changed_items:
                    result[key] = source[key]
                elif target[key] == "":
                    result[key] = source[key]
        return result

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
        translated = self.init_translation()

        for lang in self.lang_list:
            if lang != self.source_lang:
                items_to_translate = self.get_items_to_translate(lang)
                target_lang_full = get_lang_name(lang)
                user_message = json.dumps(items_to_translate)
                messages = [
                    {"role": "system", "content": const.system_message.format(self.source_lang_full, target_lang_full)},
                    {"role": "user", "content": user_message},
                ]
                response = self.get_completion_from_messages(messages)
                translated[lang] = self.parse_gpt_output(
                    json.loads(response), items_to_translate, lang
                )

        return translated
