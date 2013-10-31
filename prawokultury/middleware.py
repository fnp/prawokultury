from honeypot.middleware import HoneypotViewMiddleware

def honeypot_exempt(view):
    view.honeypot_exempt = True
    return view

class ExemptableHoneypotViewMiddleware(HoneypotViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if hasattr(callback, 'honeypot_exempt'):
            return None
        return super(ExemptableHoneypotViewMiddleware, self).process_view(
            request, callback, callback_args, callback_kwargs)
