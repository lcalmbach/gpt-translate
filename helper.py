import streamlit as st
import iso639
import json
from io import BytesIO
import os
import socket

import const as cn


def get_lang_dict_complete():
    with open(cn.LANG_FILE, "r") as file:
        # Load the contents of the file as a JSON object
        lang = json.load(file)
    return lang


def get_all_language_dict():
    keys = [lang["iso639_1"] for lang in iso639.data if lang["iso639_1"] != ""]
    values = [lang["name"] for lang in iso639.data if lang["iso639_1"] != ""]
    language_dict = dict(zip(keys, values))
    return language_dict


def get_used_languages():
    language_dict = get_all_language_dict()
    used_languages = list(lang_dict_complete.keys())
    extracted_dict = {
        key: language_dict[key] for key in used_languages if key in language_dict
    }
    return extracted_dict


def get_lang(lang_code: str):
    return lang_dict_complete[lang_code]


def download_button(data, download_filename, button_text):
    """
    Function to create a download button for a given object.

    Parameters:
    - object_to_download: The object to be downloaded.
    - download_filename: The name of the file to be downloaded.
    - button_text: The text to be displayed on the download button.
    """
    # Create a BytesIO buffer
    json_bytes = json.dumps(data).encode("utf-8")
    buffer = BytesIO(json_bytes)

    # Set the appropriate headers for the browser to recognize the download
    st.set_option("deprecation.showfileUploaderEncoding", False)
    st.download_button(
        label=button_text,
        data=buffer,
        file_name=download_filename,
        mime="application/json",
    )


def get_var(varname: str):
    if socket.gethostname().lower() == LOCAL_HOST:
        return os.environ[varname]
    else:
        return st.secrets[varname]


LOCAL_HOST = 'liestal'
# list of all iso639 languages
lang_dict_complete = get_lang_dict_complete()

