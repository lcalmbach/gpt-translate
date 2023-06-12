# PolyglotGPT - Streamlit app for language translation

PolyglotGPT is a web application built with Streamlit that allows users to translate texts across different languages. The resulting langauge file can be used to create multilingual application. The input file has the following format:
```
{
  "en": {
    "language": "Language",
    "welcome": "Welcome"
  },
  "de": {},
  "fr": {}
}
```
The first language must be filled with texts, while all following language keys are generally empty. PolyglotGPT will translate all missing tags in the subsequent language sections. Texts that are found in the languages to be translated will not be translated again. You may therefore manually edit translated texts and these edits will be kept when resubmitting the json file for translation of new texts.
```
{
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

## Installation
To use PolyglotGPT, clone the repository to your local machine and install the dependencies using pip:
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
Once the app starts, you will be able to select a language and upload a JSON file containing the texts to be translated. The app will use OpenAI's GPT-3 to automatically translate the texts and return a JSON file with the translated texts.
1. drag a json language file to the upload widget
2. press the start translation key
3. press the [download translation] button to retrieve the translation result

Note that this method requires the OPENAI_API_KEY environment variable to be set with a valid API key for OpenAI's GPT-3 service.

## Contributing
We welcome contributions to PolyglotGPT! Feel free to submit bug reports or feature requests on the GitHub page, and to fork the repository and submit pull requests.

##License
This project is licensed under the MIT License. See LICENSE for more information.