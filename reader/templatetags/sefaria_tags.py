# -*- coding: utf-8 -*-
import re
import dateutil.parser

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.template import Library
from django.contrib.auth.models import User

from sefaria.texts import url_ref as url
from sefaria.texts import parse_ref
from sefaria.util import user_link as ulink

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def url_ref(value):
	if not value:
		return ""
	pRef = parse_ref(value, pad=False)
	if "error" in pRef:
		return value
	link = '<a href="/' + url(value) + '">' + value + '</a>'
	return mark_safe(link)


@register.filter(is_safe=True)
@stringfilter
def url_safe(value):
	safe = value.replace(" ", "_")
	return mark_safe(safe)


@register.filter(is_safe=True)
def user_link(uid):
	return mark_safe(ulink(uid))


@register.filter(is_safe=True)
def strip_html_entities(text):
	text = text if text else ""
	text = text.replace("<br>", "\n")
	text = text.replace("&amp;", "&")
	text = text.replace("&nbsp;", " ")
	return mark_safe(text)


@register.filter(is_safe=True)
def strip_tags(value):
    """
    Returns the given HTML with all tags stripped.

    This is a copy of django.utils.html.strip_tags, except that it adds some
    whitespace in between replaced tags to make sure words are not erroneously
    concatenated.
    """
    return re.sub(r'<[^>]*?>', ' ', force_unicode(value))


@register.filter(is_safe=True)
@stringfilter
def trim_mishneh_torah(value):
	safe = value.replace("Mishneh Torah, ", "")
	safe = safe.replace(u"משנה תורה, ", "")
	return mark_safe(safe)


@register.filter(is_safe=True)
def sum_counts(counts):
	return sum(counts.values()) / 350.0


@register.filter(is_safe=True)
def text_progress_bars(text):
	if text.percentAvailable:
		html = """
		<div class="progressBar heAvailable" style="width:{{ text.percentAvailable.he|floatformat|default:'0' }}%">
		</div>
		<div class="progressBar enAvailable" style="width:{{ text.percentAvailable.en|floatformat|default:'0' }}%">
		</div>
		"""
	else:
		html = """
		<div class="progressBar heAvailable" style="width:{{ text.availableCounts.he|sum_counts }}%">
		</div>
		<div class="progressBar enAvailable" style="width:{{ text.availableCounts.en|sum_counts }}%">
		</div>
		"""
	return sum(counts.values())


@register.filter(is_safe=True)
def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))


@register.simple_tag 
def get_private_attribute(model_instance, attrib_name): 
        return getattr(model_instance, attrib_name, '') 


@register.filter(is_safe=True)
def nice_timestamp(timestamp):
	return dateutil.parser.parse(timestamp).strftime("%m/%d/%y")