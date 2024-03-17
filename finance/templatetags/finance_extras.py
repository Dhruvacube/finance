import datetime
import re

from django import template
from django.conf import settings
from django.http import QueryDict
from django.template.defaultfilters import stringfilter
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def order_queryset_by(queryset, order):
    return queryset.order_by(order)


@register.filter
def attrsum(container, attr_name):
    return sum(getattr(e, attr_name) for e in container)


@register.filter
def currency(amount):
    return settings.CURRENCY_PREFIX + str(amount) + settings.CURRENCY_SUFFIX


@register.simple_tag
def setvar(val=None):
    return val


@register.filter
def italic_if_future(string, date):
    # XXX: `string` is not necessarily safe
    return (
        mark_safe(f'<span class="font-italic">{string}</span>')
        if date > datetime.datetime.now().date()
        else string
    )


@register.filter
def is_current_month(date):
    today = datetime.datetime.today()
    return date.month == today.month and date.year == today.year


@register.filter
def override_query_dict(query_dict, parameters):
    query_dict = query_dict.copy()
    query_dict.update(QueryDict(parameters))
    return "&".join(f"{k}={v}" for k, v in query_dict.items())


@register.filter
@stringfilter
def highlight_text(text, term):
    return (
        mark_safe(
            re.sub(
                term,
                lambda matchobj: f'<span class="text-highlight">{matchobj.group(0)}</span>',  # noqa: E501
                text,
                flags=re.I,
            )
        )
        if term
        else text
    )


@register.simple_tag
def theme_range():
    a = f'<a class="dropdown-item" href="{reverse("changetheme")}?theme=default">Default</a><div class="dropdown-divider"></div>'
    for i in settings.THEME_DICT:
        a += f'<a class="dropdown-item" href="{reverse("changetheme")}?theme={i}"><i class="bi bi-circle-fill" style="color: #{settings.THEME_DICT[i]}"></i> {i.title()}</a>'
    return mark_safe(a)


@register.filter
def display_color(amount_deposited, amount_threshold):
    account_percentage = abs(amount_threshold / amount_deposited)
    if account_percentage < 0.75 and account_percentage > 0.5:
        return "#08cf3d"
    if account_percentage < 0.5 and account_percentage > 0.25:
        return "#ffc000"
    if account_percentage < 0.25:
        return "#ff0000"
