class MenuItem(object):
    html_id = None

    class InvalidMenuItem(BaseException):
        pass

    def __init__(self, url, title, html_id=None, more_urls=None):
        self.url = url
        self.title = title
        self.html_id = html_id
        self.more_urls = more_urls or set()

    def is_valid(self):
        return True

    def is_active(self, request, value):
        url = request.get_full_path()
        return url == str(self.url) or url in set(str(url) for url in self.more_urls)

    def check_active(self, request, value):
        try:
            self.active = self.is_active(request, value)
        except self.InvalidMenuItem, e:
            pass

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title


class ObjectMenuItem(MenuItem):
    """Menu item corresponding to an object.

    If no url or title is provided, get_absolute_url and __unicode__ are used.
    You can also provide a reverse lookup dictionary, as in {model: field_name}.
    """
    def __init__(self,
            obj=None, obj_get=None,
            url=None, rev_lookups=None, title=None, html_id=None):
        super(ObjectMenuItem, self).__init__(url=url, title=title, html_id=html_id)
        self.obj = obj
        self.obj_get = obj_get
        self.rev_lookups = rev_lookups

    def get_object(self):
        try:
            return self.obj or self.obj_get()
        except BaseException, e:
            raise self.InvalidMenuItem(e)

    def get_title(self):
        return self.title or unicode(self.get_object())

    def get_url(self):
        return self.url or self.get_object().get_absolute_url()

    def is_valid(self):
        try:
            obj = self.get_object()
        except self.InvalidMenuItem, e:
            return False
        return True

    def is_active(self, request, value):
        if value == self.get_object():
            return True
        if self.rev_lookups:
            for model, manager in self.rev_lookups.items():
                if (isinstance(value, model) and 
                        self.get_object() in getattr(value, manager).all()):
                    return True
        return False


class ModelMenuItem(MenuItem):
    """Menu item corresponding to a model, optionally filtered by some fields."""

    def __init__(self, model, url, field_lookups=None, title=None, html_id=None):
        if title is None:
            title = unicode(model)
        super(ModelMenuItem, self).__init__(title=title, url=url, html_id=html_id)
        self.model = model
        self.field_lookups = field_lookups

    def is_active(self, request, value):
        if value == self.model and not self.field_lookups:
            return True
        if str(self.url) == request.get_full_path():
            return True
        if isinstance(value, self.model) and self.field_lookups:
            lookups_ok = True
            for field, lookup in self.field_lookups.items():
                if getattr(value, field) != lookup:
                    lookups_ok = False
            if lookups_ok:
                return True
        return False

    def get_title(self):
        return self.title or unicode(self.model)
