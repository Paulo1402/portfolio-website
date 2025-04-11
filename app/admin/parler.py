from django.contrib import admin

# from modeltranslation.admin import TranslationAdmin
from parler.admin import TranslatableAdmin

from app.models.parler import News


# class NewsAdmin(TranslationAdmin):
#     pass
class NewsAdmin(TranslatableAdmin):
    pass


admin.site.register(News, NewsAdmin)
