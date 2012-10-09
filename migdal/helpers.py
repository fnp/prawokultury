# -*- coding: utf-8 -*-
# This file is part of PrawoKultury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
class EntryType(object):
    def __init__(self, db, slug, commentable=False, on_main=False,
            promotable=False, categorized=False):
        self.db = db
        self.slug = slug
        self.commentable = commentable
        self.on_main = on_main
        self.promotable = promotable
        self.categorized = categorized

    def __unicode__(self):
        return unicode(self.slug)
