# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django import template


register = template.Library()

@register.filter('in_group')
def in_group(user, group_name):
    """
    Verifies user is in a group
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False