"""Allow-list HTML sanitizer for rich-text fields (product descriptions).

Descriptions are written in the Oscar dashboard (HTML editor) and rendered by the
storefront with dangerouslySetInnerHTML, so they are sanitized here, on output.
Only simple formatting tags are kept; scripts, event handlers, styles, iframes and
non-http(s)/mailto links are dropped.
"""

from html import escape
from html.parser import HTMLParser

ALLOWED_TAGS = {
    "p", "br", "strong", "b", "em", "i", "u", "ul", "ol", "li",
    "h2", "h3", "h4", "blockquote", "span", "a", "table", "thead",
    "tbody", "tr", "th", "td",
}
VOID_TAGS = {"br"}
DROP_CONTENT_TAGS = {"script", "style", "iframe", "object", "embed", "noscript", "template"}
SAFE_SCHEMES = ("http://", "https://", "mailto:", "tel:", "/", "#")


class _Sanitizer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.open_tags = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_CONTENT_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth or tag not in ALLOWED_TAGS:
            return
        if tag == "a":
            href = dict(attrs).get("href") or ""
            if not href.strip().lower().startswith(SAFE_SCHEMES):
                self.out.append("<a>")
            else:
                self.out.append(f'<a href="{escape(href.strip(), quote=True)}" rel="noopener noreferrer nofollow">')
            self.open_tags.append("a")
            return
        self.out.append(f"<{tag}>")
        if tag not in VOID_TAGS:
            self.open_tags.append(tag)

    def handle_endtag(self, tag):
        if tag in DROP_CONTENT_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth or tag not in self.open_tags:
            return
        while self.open_tags:
            last = self.open_tags.pop()
            self.out.append(f"</{last}>")
            if last == tag:
                break

    def handle_data(self, data):
        if not self.skip_depth:
            self.out.append(escape(data, quote=False))

    def result(self):
        while self.open_tags:
            self.out.append(f"</{self.open_tags.pop()}>")
        return "".join(self.out)


def sanitize_html(value):
    if not value:
        return ""
    parser = _Sanitizer()
    parser.feed(str(value))
    parser.close()
    return parser.result()
