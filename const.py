LANG_FILE = "./lang/app.json"

example_input = {"en": {"welcome": "Welcome", "menu": "Menu"}, "de": {}, "fr": {}}
example_output = {
    "en": {"welcome": "Welcome", "selection": "Selection"},
    "de": {"welcome": "Willkommen", "selection": "Auswahl"},
    "fr": {"welcome": "Bienvue", "selection": "Sélection"},
    "it": {"welcome": "Benvenuto"},
    "zh": {"welcome": "歡迎"},
}


system_message = """You will translate strings kept in a json formatted input delimited by #### and generate a json formatted output.
The json input file is formatted as in this example:
{
    "welcome": "Welcome",
    "menu": "Menu"
    "options": ["red", "blue", "green"]
}

Example output:
{
    "welcome": "Willkommen",
    "menu": "Menu"
    "options": ["rot", "blau", "grün"]
}
only output the json string, nothing else.
"""
