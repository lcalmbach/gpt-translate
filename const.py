LANG_FILE = "./lang/app.json"

example_input = {"en": {"welcome": "Welcome", "menu": "Menu"}, "de": {}, "fr": {}}
example_output = {
    "en": {"welcome": "Welcome", "selection": "Selection"},
    "de": {"welcome": "Willkommen", "selection": "Auswahl"},
    "fr": {"welcome": "Bienvue", "selection": "Sélection"},
    "es": {},
}


system_message = """You will translate strings kept in a json formatted input delimited by #### and generate a json formatted output. The json file holds a first key with the source language to be translated as a ISO 639-1 language code and all expressions to be translated in the source language. Below the source language follows a list of target languages to be translated. Each target language holds a list of keys from the source language object to be translated.

    The json input file is formatted as in this example:
    {
        "en": {
            "welcome": "Welcome",
            "menu": "Menu"
        },
        "de": ["welcome", "menu"],
        "fr": ["welcome"]
    }
    The obove object holds the following instructions:
    source language is english (en)
    the following expressions must be translated: "Welcome", "Menu"
    for German ("de") translate: the expressions: "Welcome" and "Menu", for french ("fr") translate: "Welcome"

    Generate the following json formatted output with all translated texts in the following format:
    {
        "de": {
            "welcome": "Willkommen",
            "menu": "Menu"
        },
         "fr": {
            "welcome": "Bienvenue",
            "menu": "menu"
        }
    }
    only output the json string, nothing else.
    """
