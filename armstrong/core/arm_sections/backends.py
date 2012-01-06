from django.conf import settings
from django.db.models.query import QuerySet


def find_related_models(section, targetModel=None):
    rel = None
    relateds = section._meta.get_all_related_objects() + \
               section._meta.get_all_related_many_to_many_objects()
    for related in relateds:
        found = "%s.%s" % (related.model.__module__,
                related.model.__name__)
        if found == settings.ARMSTRONG_SECTION_ITEM_MODEL:
            rel = related
            break
    kwargs = {rel.field.name: section}

    if not targetModel:
        targetModel = rel.model
    elif not issubclass(targetModel, rel.model):
        return QuerySet().none()

    qs = targetModel.objects.filter(**kwargs)
    if hasattr(qs, 'select_subclasses'):
        qs = qs.select_subclasses()
    return qs
