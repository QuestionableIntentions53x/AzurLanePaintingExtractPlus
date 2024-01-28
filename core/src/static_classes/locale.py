import gettext

class Translator:
    def __init__(self):
        self.selected_language = "en"
        self.languages = [str("en"), str("zh")]
        self.locale_directory = "core\\assets\\localization"
        self.loaded_locale = gettext.gettext
        self._ = gettext.gettext

    def t(self, string: str):
        out = self.loaded_locale(string)
        if out == string:
            return string
        return out

    def set_locale_from_index(self, index: int):
        return self.set_locale(self.languages[index])

    def set_locale(self, language_code: str):
        if language_code == self.selected_language:
            return self._("Language already selected!")

        if not language_code in self.languages:
            return self._("Localization [{}] does not exist!").format(language_code)

        exists = gettext.find(
            "messages",
            languages = [language_code],
            localedir = self.locale_directory)
        
        if exists == None and language_code != "en":
            return self._("Localization [{}] does not exist!").format(language_code)

        language = gettext.translation(
            "messages",
            languages = [language_code],
            localedir = self.locale_directory,
            fallback = True)
        
        language.install()
        self.loaded_locale = language.gettext
        self.selected_language = language_code