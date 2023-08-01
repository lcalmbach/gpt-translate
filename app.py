import streamlit as st
from helper import get_used_languages, get_lang, download_button
import const as cn
import json
from translator import Translator

__version__ = "0.0.3"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-08-02"
GIT_REPO = 'https://github.com/lcalmbach/gpt-translate'
lang = {}


def get_app_info():
    """
    Returns a string containing information about the application.
    Returns:
    - info (str): A formatted string containing details about the application.
    """
    created_by = lang["created_by"]
    powered_by = lang["powered_by"]
    version = lang["version"]

    info = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>{created_by} <a href="mailto:{__author_email__}">{__author__}</a><br>
    {version}: {__version__} ({VERSION_DATE})<br>
    {powered_by} <a href="https://streamlit.io/">Streamlit</a> and 
    <a href="https://platform.openai.com/">OpenAI API</a><br> 
    <a href="{GIT_REPO}">git-repo</a>
    """

    created_by = lang["created_by"]
    powered_by = lang["powered_by"]
    version = lang["version"]

    info = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>{created_by} <a href="mailto:{__author_email__}">{__author__}</a><br>
    {version}: {__version__} ({VERSION_DATE})<br>
    {powered_by} <a href="https://streamlit.io/">Streamlit</a> and 
    <a href="https://platform.openai.com/">OpenAI API</a><br> 
    <a href="{GIT_REPO}">git-repo</a>
    """
    return info


def refresh_lang():
    """
    The refresh_lang function is responsible for refreshing the language dictionary used 
    in the application. It updates the lang_dict variable in the session state with 
    the new language dictionary obtained from the get_lang function.

    The function then displays the updated language dictionary and finally 
    triggers a rerun of the application to refresh all language on the UI.
    """
    st.session_state["lang_dict"] = get_lang(st.session_state["lang"])
    st.write(st.session_state["lang_dict"])
    st.experimental_rerun()


def display_language_selection():
    """
    The display_info function displays information about the application. It 
    uses the st.expander container to create an expandable section for the 
    information. Inside the expander, displays the input and output format.
    """
    index = list(st.session_state["used_languages_dict"].keys()).index(
        st.session_state["lang"]
    )
    x = st.sidebar.selectbox(
        label=f'🌐{lang["language"]}',
        options=st.session_state["used_languages_dict"].keys(),
        format_func=lambda x: st.session_state["used_languages_dict"][x],
        index=index,
    )
    if x != st.session_state["lang"]:
        st.session_state["lang"] = x
        refresh_lang()


def display_info():
    with st.expander(lang["information"]):
        st.markdown(lang["app-info"])
        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"### {st.session_state['lang_dict']['input']}")
            st.json(cn.example_input)
        with cols[1]:
            st.markdown(f"### {st.session_state['lang_dict']['output']}")
            st.json(cn.example_output)


def display_upload():
    """
    Respond about this code

    This function handles the file uploading functionality. It performs the following steps:
    - Checks if a file is uploaded using the file_uploader widget.
    - If a file is uploaded, it reads the contents of the file and attempts to parse it as JSON.
    - If the JSON parsing is successful, it saves the JSON data to the "input_json" variable in the st.session_state dictionary.
    - Displays a success message if the file is loaded successfully.
    - Displays the content of the loaded JSON file in an expander widget.
    - If the "input_json" variable is present in the st.session_state dictionary, it creates a Translator object and displays its info.
    - If the "Start translation" button is clicked, it translates the input JSON using the Translator object and displays the translated result.
    - Provides a download button to download the translated JSON file.

    Parameters:
        None

    Returns:
        None
    """

    uploaded_file = st.file_uploader(lang["upload"])

    if uploaded_file:
        file_contents = uploaded_file.read()

        try:
            st.session_state["input_json"] = json.loads(file_contents)
            st.success(lang["file-load-success"])
            with st.expander(lang["input_file_content"]):
                st.write(st.session_state["input_json"])

        except json.JSONDecodeError:
            st.error(lang["file-load-error"])
            if "input_json" in st.session_state:
                del st.session_state["input_json"]

        if "input_json" in st.session_state:
            translation = Translator(st.session_state["input_json"])
            st.write(translation.info)

            if st.button("Start translation"):
                translated_page = translation.translate()
                st.write(translated_page)
                download_button(translated_page, "translated.json", lang["download-result"])


def main():
    """
    Respond about this code

    This function serves as the main entry point of the application. It performs the following steps:
    - Checks if the "lang" variable is present in the st.session_state dictionary. If not, it initializes it and other related variables.
    - Sets the global variable "lang" to the value of "lang_dict" from the st.session_state dictionary.
    - Displays the language selection in the sidebar.
    - Displays some information.
    - Displays the upload functionality.
    - Displays the app info in the sidebar.

    Parameters:
        None

    Returns:
        None
    """

    global lang

    if not ("lang" in st.session_state):
        # first item is default language
        st.session_state["used_languages_dict"] = get_used_languages()
        st.session_state["lang"] = next(
            iter(st.session_state["used_languages_dict"].items())
        )[0]
        refresh_lang()

    lang = st.session_state["lang_dict"]
    st.sidebar.markdown("## PolyglotGPT")
    display_language_selection()
    display_info()
    display_upload()
    st.sidebar.markdown(get_app_info(), unsafe_allow_html=True)


main()
