from django.conf import settings
from django_comments.signals import comment_will_be_posted
import re

def spamfilter(sender, comment, **kwargs):
    return False
    ban = [
'cialis', 
'viagra', 'generic', 'first time', 'genital', 'ficken', 'cheap', 'affiliate', 'herpes', ' your blog '
'priceless',
'find out more',
' product ',
' concerns ',
'cheats',
'this site',
'fantastic read',
'features',
'your website',
'this blog',
'this info',
'thank you',
'thanks',
'tips and tricks',
]
    for b in ban:
        if b in comment.user_name.lower(): return False
        if b in comment.user_url.lower(): return False
        if b in comment.comment.lower(): return False
    if 'http://' in comment.user_name.lower(): return False
    return comment.ip_address not in getattr(settings, 'COMMENTS_IP_BLOCKED', ())
comment_will_be_posted.connect(spamfilter)


