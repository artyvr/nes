import re
from html import escape

def strip_tags(text):
    return escape(re.sub(r'<[^>]+>', '', text))