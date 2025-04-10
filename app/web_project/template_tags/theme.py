
from django import template

register = template.Library()


@register.filter
def filter_by_url(submenu, url):
    if submenu:
        for subitem in submenu:
            subitem_url = subitem.get("url")
            if subitem_url == url.path or subitem_url == url.resolver_match.url_name:
                return True

            # Recursively check for submenus
            elif subitem.get("submenu"):
                if filter_by_url(subitem["submenu"], url):
                    return True

@register.simple_tag
def current_url(request):
    return request.build_absolute_uri()

