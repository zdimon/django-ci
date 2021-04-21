from modeltranslation.translator import translator, TranslationOptions
from .models import Page, Task

class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

translator.register(Page, PageTranslationOptions)

class TaskTranslationOptions(TranslationOptions):
    fields = ('title', 'desc')

translator.register(Task, TaskTranslationOptions)