from modeltranslation.translator import translator, TranslationOptions
from .models.parler import News


class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "text")


print("Registering NewsTranslationOptions with the translator")

translator.register(News, NewsTranslationOptions)
