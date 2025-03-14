import tagulous.models


class Topic(tagulous.models.TagModel):
    class TagMeta:
        autocomplete_view = "topic_autocomplete"
        force_lowercase = True
