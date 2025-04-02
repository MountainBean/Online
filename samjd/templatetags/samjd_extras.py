import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from samjd.markdown_extensions import ProjectImageExtension

register = template.Library()

@register.filter
@stringfilter
def render_markdown(value):
    md = markdown.Markdown(extensions=["fenced_code", ProjectImageExtension()])
    return mark_safe(md.convert(value))

