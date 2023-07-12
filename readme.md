# PolyglotGPT - Streamlit app for language translation

## Required Input
[PolyglotGPT](https://lcalmbach-gpt-translate-app-i49g8c.streamlit.app/) is a web application built with Streamlit that allows users to translate texts across different languages. The resulting language file can be used to create multilingual applications. The input file has the following format:
```
{
  "source": {
    "language": "Language",
    "welcome": "Welcome"
    "colors": ["red", "blue", "green"]
  },
  "en": {},
  "de": {},
  "fr": {}
}
```
The source language should be listed in the first place. It is followed by a list of language 2-digit codes following the [ISO 639-1 standard](https://en.wikipedia.org/wiki/ISO_639-1) left initially empty. The first language in this list must be the primary language; it will be filled with a copy of the source object. 

During the first initial translation, PolyglotGPT will copy the source language string to the first language section, then use the OpenAI API to translate every text in the source language to all other languages, as shown below.
```
{
    "en": {
        "language": "Language",
        "welcome": "Welcome"
    },
    "en": {
        "language": "Language",
        "welcome": "Welcome"
    },
    "de": {
        "language": "Sprache",
        "welcome": "Willkommen"
        },
    "fr": {
        "language": "Langue",
        "welcome": "Bienvenue"
    }
}
```

## Editing the language file
There are two ways of editing the language file. 
1. You added a key/sentence entry to the source section or edited one of the existing sentences in the source section. PolyglotGPT will detect a difference between the source and the primary language. The main language will be overwritten with the source, and all new or changed keys are stored in a key-list during this process. For all languages, the keys marked as new or changed will be translated anew. For each key, the system checks if the keys exist in the language. If it does, and a change is detected in the key, the items are translated again. All sentences in the source section that are found to be identical to the first language are not translated. They may contain manual changes that you want to keep.

## Installation
To install PolyglotGPT locally, clone the repository to your local machine and install the dependencies using pip:
```
>git clone https://github.com/username/polyglot-gpt.git
>cd polyglot-gpt
>pip install -r requirements.txt
```
## Usage
To run the app, execute the following command:

```
>streamlit run app.py
```
Once the app starts, you can select a language and upload a JSON file containing the texts to be translated. The app will use OpenAI's GPT-3 to automatically translate the texts and return a JSON file with the translated texts.
1. drag a json language file to the upload widget
2. press the start translation key
3. press the [download translation] button to retrieve the translation result

Note that this method requires the OPENAI_API_KEY environment variable to be set with a valid API key for OpenAI's GPT-3 service.

## Contributing
We welcome contributions to PolyglotGPT! Feel free to submit bug reports or feature requests on the GitHub page, and to fork the repository and submit pull requests.

##License
This project is licensed under the MIT License. See LICENSE for more information. To use PolyglotGPT, clone the repository to your local machine and install the dependencies using pip: