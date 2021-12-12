# language-explainer

A tool for defining/translating hard words for language learners.

This tool helps you find and extract hard words 
(based on their [CEFR](https://www.coe.int/en/web/common-european-framework-reference-languages/level-descriptions) levels) 
from a `TEXT` or `PDF` file (maybe `audio files` in future).
Ultimately, it would download words' definition from [Google](translate.google.com)/[FreeDictionaryAPI](https://dictionaryapi.dev/) and save it to file in either JSON or CSV format.

## How to install
1. Clone this project 
``` bash
git clone git@github.com:soheilrt/language-explainer
```
2. Go to project path 
``` bash
cd <project_path>
```
3. Create new python virtual environment 
```bash
virtualenv venv
```
Activate the virtual environment 
```bash
source <virtual_env_path>/bin/activate
```
4. Install requirements
```bash
pip install -r requirements.txt
```

5. Run 
```bash
python explain --input-type (url|pdf|text) -input <file_name|url_address> -output <output_file_name) -output-type (csv|json)
```

## Simple JSON output format
```json
{
"preferences": [
  {
    "language": "en",
    "meanings": [
      {
        "definitions": [
          {
            "antonyms": [],
            "definition": "a greater liking for one alternative over another or others.",
            "example": "her preference for white wine",
            "synonyms": [
              "liking",
              "partiality",
              "predilection",
              "proclivity",
              "fondness",
              "taste",
              "inclination",
              "leaning",
              "bias",
              "bent",
              "penchant",
              "predisposition",
              "desire",
              "wish",
              "rather than",
              "instead of",
              "in place of",
              "sooner than",
              "above",
              "before",
              "over"
            ]
          },
          {
            "antonyms": [],
            "definition": "a prior right or precedence, especially in connection with the payment of debts.",
            "example": "debts owed to the community should be accorded a preference",
            "synonyms": []
          }
        ],
        "parOfSpeech": "noun"
      }
    ],
    "origin": "late Middle English (in the sense ‘promotion’): from Old French, from medieval Latin praeferentia, from Latin praeferre ‘carry in front’ (see prefer).",
    "phonetics": [
      {
        "audio": "//ssl.gstatic.com/dictionary/static/sounds/20200429/preference--_gb_1.mp3",
        "language": "en",
        "phonetic": "ˈprɛf(ə)r(ə)ns",
        "word": "preferences"
      }
    ],
    "source": "free_dictionary",
    "translations": [],
    "word": "preferences"
  }
]
}
```

## CSV output example


|phoneme|ˈfəʊniːm                     |https://ssl.gstatic.com/dictionary/static/sounds/20200429/phoneme--_gb_1.mp3|noun                                         |any of the perceptually distinct units of sound in a specified language that distinguish one word from another, for example p, b, d, and t in the English words pad, pat, bad, and bat.|                                       |                                                                                                                                                                                                                                                                                                                                                                    |            |
|-------|-----------------------------|----------------------------------------------------------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
|stored |stɔː                         |https://ssl.gstatic.com/dictionary/static/sounds/20200429/store--_gb_1.mp3  |verb                                         |keep or accumulate (something) for future use.                                                                                                                                         |a small room used for storing furniture|keep, keep in reserve, stow, stockpile, lay in/aside, set aside, put away, put down, put to one side, deposit, save, hoard, cache, stock up with/on, get in supplies of, collect, gather, accumulate, cumulate, amass, husband, reserve, preserve, put away for a rainy day, squirrel away, salt away, stash, put into storage, put in store, stow (away), warehouse|use, discard|



