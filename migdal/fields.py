# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.db import models

class SlugNullField(models.SlugField):
    description = "SlugField that stores NULL instead of blank value."

    def to_python(self, value, **kwargs):
        value = super(SlugNullField, self).to_python(value, **kwargs)
        return value if value is not None else u""

    def get_prep_value(self, value, **kwargs):
        value = super(SlugNullField, self).get_prep_value(value, **kwargs)
        return value or None


try:
    # check for south
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ["^migdal\.fields\.SlugNullField"])
