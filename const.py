LANG_FILE = "./lang/app.json"

example_input = {"source": {"welcome": "Welcome", "menu": "Menu"}, "en": {}, "de": {}, "fr": {}}
example_output = {
    "source": {"welcome": "Welcome", "selection": "Selection"},
    "en": {"welcome": "Welcome", "selection": "Selection"},
    "de": {"welcome": "Willkommen", "selection": "Auswahl"},
    "fr": {"welcome": "Bienvue", "selection": "Sélection"},
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
