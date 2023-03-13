from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='get_category_name')
def get_category_name(value: int) -> str:
    """
    This filter return category name from Settings
    :param value: int of category index
    :return: str of category name
    """
    category = settings.DOCUMENTS_CATEGORY.get(value)

    return category['title']


@register.filter(name='get_category_icon')
def get_category_icon(value: int) -> str:
    """
    This filter return category icon from Settings
    :param value: int of category index
    :return: str of category icon
    """
    category = settings.DOCUMENTS_CATEGORY.get(value)

    return category['icon']
