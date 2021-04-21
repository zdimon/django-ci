from modeltranslation.translator import translator, TranslationOptions
from .models import Project

class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'desc')

translator.register(Project, ProjectTranslationOptions)