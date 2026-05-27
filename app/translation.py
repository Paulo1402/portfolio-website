from modeltranslation.translator import TranslationOptions, translator

from app.models import (
    Certification,
    Experience,
    Formation,
    Profile,
    Project,
    Skill,
    SkillArea,
)


class ExperienceTranslationOptions(TranslationOptions):
    fields = ("title", "description")


class FormationTranslationOptions(TranslationOptions):
    fields = ("title", "description")


class ProfileTranslationOptions(TranslationOptions):
    fields = ("description",)


class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "description")


class SkillAreaTranslationOptions(TranslationOptions):
    fields = ("name",)


class SkillTranslationOptions(TranslationOptions):
    fields = ("name",)


class CertificationTranslationOptions(TranslationOptions):
    fields = ("title", "description")


translator.register(Experience, ExperienceTranslationOptions)
translator.register(Formation, FormationTranslationOptions)
translator.register(Profile, ProfileTranslationOptions)
translator.register(Project, ProjectTranslationOptions)
translator.register(SkillArea, SkillAreaTranslationOptions)
translator.register(Skill, SkillTranslationOptions)
translator.register(Certification, CertificationTranslationOptions)
