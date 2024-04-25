import json
import os

from typing import List

from {{ADDON_NAME_PACKAGE}}.utils.file_utils import FileUtils # type: ignore

LANG: str = 'en'
loaded_translations: List = None

def load_translations(language: str) -> None:
    languages_folder = os.path.join(FileUtils.get_addon_root_dir(), "translation/languages")
    translations_file = os.path.join(languages_folder, f"{language}.json")
    
    with open(translations_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_translation(key: str):
    k: str = loaded_translations.get(key, key)
    return k

def register():
    global loaded_translations
    loaded_translations = load_translations(LANG)

def unregister():
    global loaded_translations
    loaded_translations = None



