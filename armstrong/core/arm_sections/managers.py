from django.db import models
from django.db.models import Q


class SectionSlugManager(models.Manager):
    def __init__(self,
                 primary_section_field="primary_section",
                 section_field="sections",
                 slug_field="slug",
                 *args, **kwargs):
        super(SectionSlugManager, self).__init__(*args, **kwargs)
        self.primary_section_field = primary_section_field
        self.section_field = section_field
        self.slug_field = slug_field

    def get_by_slug(self, slug):
        if slug[-1] == "/":
            slug = slug[0:-1]
        if slug[0] == "/":
            slug = slug[1:]
        section_slug, content_slug = slug.rsplit("/", 1)
        section_slug += "/"

        primary = {self.slug_field: content_slug}
        secondary = primary.copy()
        primary["%s__full_slug" % self.primary_section_field] = section_slug
        secondary["%s__full_slug" % self.section_field] = section_slug

        qs = self.model.objects.filter(Q(**primary) | Q(**secondary))
        if hasattr(qs, "select_subclasses"):
            qs = qs.select_subclasses()
        try:
            return qs[0]
        except IndexError:
            raise self.model.DoesNotExist
