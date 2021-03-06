from django.db.models import Q

from .utils import get_section_relations, get_item_model_class


class ItemFilter(object):
    manager_attr = 'objects'

    def get_manager(self, model):
        """Return the desired manager for the item model."""
        return getattr(model, self.manager_attr)

    def get_section_relations(self, section):
        return get_section_relations(section.__class__)

    def filter_objects_by_section(self, rels, section):
        """Build a queryset containing all objects in the section subtree."""

        subtree = section.get_descendants(include_self=True)
        kwargs_list = [{'%s__in' % rel.field.name: subtree} for rel in rels]
        q = Q(**kwargs_list[0])
        for kwargs in kwargs_list[1:]:
            q |= Q(**kwargs)
        return self.get_manager(get_item_model_class()).filter(q).distinct()

    def process_items(self, items):
        """
        Perform extra actions on the filtered items.

        Example: Further filtering items in the section to meet a custom need.
        """
        if hasattr(items, 'select_subclasses'):
            items = items.select_subclasses()
        return items

    def __call__(self, section):
        relations = self.get_section_relations(section)
        items = self.filter_objects_by_section(relations, section)
        return self.process_items(items)


class PublishedItemFilter(ItemFilter):
    manager_attr = 'published'


# DEPRECATED: To be removed in ArmSections 2.0
import warnings


class DeprecatedItemFilter(ItemFilter):  # pragma: no cover
    def __call__(self, *args, **kwargs):
        msg = ("find_related_models() is deprecated and will be removed in " +
               "ArmSections 2.0. Use ItemFilter.")
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        return super(DeprecatedItemFilter, self).__call__(*args, **kwargs)
find_related_models = DeprecatedItemFilter
