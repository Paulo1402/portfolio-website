import tagulous.admin


class TaggedModelAdminCompat(tagulous.admin.TaggedModelAdmin):
    def formfield_for_dbfield(self, db_field, request=None, **kwargs):
        # modeltranslation passes `request` positionally, while tagulous expects kwargs
        return super().formfield_for_dbfield(db_field, request=request, **kwargs)
