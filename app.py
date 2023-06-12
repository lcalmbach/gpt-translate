import streamlit as st
from helper import get_used_languages, get_lang, download_button
import const as cn
import json
from translator import Translator


def refresh_lang():
    st.session_state["lang_dict"] = get_lang(st.session_state["lang"])
    st.write(st.session_state["lang_dict"])
    st.experimental_rerun()


def display_language_selection():

    index = list(st.session_state["used_languages_dict"].keys()).index(
        st.session_state["lang"]
    )
    x = st.sidebar.selectbox(
        label=st.session_state["lang_dict"]["language"],
        options=st.session_state["used_languages_dict"].keys(),
        format_func=lambda x: st.session_state["used_languages_dict"][x],
        index=index,
    )
    if x != st.session_state["lang"]:
        st.session_state["lang"] = x
        refresh_lang()


def display_info():
    with st.expander(st.session_state["lang_dict"]["information"]):
        st.markdown(lang["app-info"])
        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"### {st.session_state['lang_dict']['input']}")
            st.json(cn.example_input)
        with cols[1]:
            st.markdown(f"### {st.session_state['lang_dict']['output']}")
            st.json(cn.example_output)


def display_upload():
    uploaded_file = st.file_uploader(lang["upload"])
    if uploaded_file:
        file_contents = uploaded_file.read()
        # Parse the JSON data
        try:
            st.session_state["input_json"] = json.loads(file_contents)
            st.success(lang["file-load-success"])
        except json.JSONDecodeError:
            st.error(lang["file-load-error"])
            if "input_json" in st.session_state:
                del st.session_state["input_json"]
        if "input_json" in st.session_state:
            if st.button("Start translation"):
                translation = Translator(st.session_state["input_json"])
                translated_page = translation.translate()
                st.write(translated_page)
                download_button(
                    translated_page, "translated.json", lang["download-result"]
                )


def main():
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
    display_upload()
    display_info()

main()
