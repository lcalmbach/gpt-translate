LANG_FILE = "./lang/app.json"

example_input = {
    "source": {"welcome": "Welcome", "menu": "Menu"},
    "en": {},
    "de": {},
    "fr": {},
}
example_output = {
    "source": {"welcome": "Welcome", "selection": "Selection"},
    "en": {"welcome": "Welcome", "selection": "Selection"},
    "de": {"welcome": "Willkommen", "selection": "Auswahl"},
    "fr": {"welcome": "Bienvue", "selection": "Sélection"},
}

system_message = """You will translate a user text from {} to {}. Only returned the translated text, nothing else. if the input is a list, format the output as as list as well.
"""
