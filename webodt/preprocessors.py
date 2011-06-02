# -*- coding: utf-8 -*-
from django.utils.importlib import import_module
import re


def list_preprocessors(preprocessors):
    """Create and return list of preprocessor functions
    On a basis parameters:
        `preprocessors` - list of preprocessor function names
    """
    ret = []
    for preprocessor in preprocessors:
        module_name, class_name = preprocessor.rsplit('.', 1)
        mod = import_module(module_name)
        preprocessor_func = getattr(mod, class_name)
        ret.append(preprocessor_func)
    return ret


def unescape_templatetags(template_content):
    replace_map = [
        ('&quot;', '"'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&amp;', '&'),
    ]
    for from_sym, to_sym in replace_map:
        for include_text in re.findall(r'{%([^}]+)%}', template_content):
            new_include_text = include_text.replace(from_sym, to_sym)
            template_content = template_content.replace(
                '{%%%s%%}' % include_text, '{%%%s%%}' % new_include_text
            )
    return template_content
