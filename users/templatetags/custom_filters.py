from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter(name="split")
def split(value, delimiter="/"):
    """Разбивает строку по разделителю и возвращает список."""
    return value.split(delimiter)


@register.filter
def reject(value, arg):
    """Удаляет указанный элемент из списка"""
    return [item for item in value if item != arg]
