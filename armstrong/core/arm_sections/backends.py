from django.conf import settings
from django.db.models import Q

def find_related_models(section):
    rel = None
    filters = None
    relateds = section._meta.get_all_related_objects() + \
               section._meta.get_all_related_many_to_many_objects()
    for related in relateds:
        found = "%s.%s" % (related.model.__module__,
                related.model.__name__)
        if found == settings.ARMSTRONG_SECTION_ITEM_MODEL:
            if not rel: rel = related
            q = Q( **{related.field.name: section} )
            filters = filters | q if filters else q

    qs = rel.model.objects.filter(filters)
    if hasattr(qs, 'select_subclasses'):
        qs = qs.select_subclasses()
    return qs
