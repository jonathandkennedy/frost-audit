"""Page registry and small HTML helpers shared by every content module.

Content modules call ``page(...)`` to register a page. Internal links are written
as ``[[slug]]`` (``[[home]]`` for the front page) and images as ``[[img:name]]``;
the builder resolves them per output mode (production URLs or the single-file preview).
Other tokens the builder expands: ``[[cards:slug,slug]]``, ``[[postcards:slug,slug]]``,
``[[reviews:n]]``, ``[[team]]``, ``[[nap]]``, ``[[map]]``, ``[[findus]]``, ``[[hours]]``,
``[[citylist]]``, ``[[courts:key,key]]``, ``[[author:key]]``, ``[[latestposts:n]]``.
"""
import html as _html

PAGES = []
BY_SLUG = {}

KINDS = ("home", "page", "hub", "spoke", "city", "post", "attorney")


def esc(s):
    return _html.escape(str(s), quote=True)


def page(slug, *, title, description, h1, body, kind="page", eyebrow="", lead="", hub=None,
         summary="", related=(), faqs=(), author=None, reviewer=None, date=None, modified=None,
         category=None, hero_image=None, hero_caption="", quote="", kicker="", noindex=False,
         layout="two", cta=None, nav_label=None, card_new=False, sources=(), county=None,
         section_label=None, priority=0.6, changefreq="monthly", tags=()):
    """Register a page. ``layout``: two (main + aside), one (single column), raw (body has its own sections)."""
    assert kind in KINDS, kind
    if slug in BY_SLUG:
        raise ValueError(f"duplicate slug: {slug}")
    try:
        from .meta import META
    except ImportError:
        META = {}
    if slug in META:
        title, description = META[slug]
    p = dict(slug=slug, title=title, description=description, h1=h1, body=body, kind=kind,
             eyebrow=eyebrow, lead=lead, hub=hub, summary=summary, related=list(related), faqs=list(faqs),
             author=author, reviewer=reviewer, date=date, modified=modified or date, category=category,
             hero_image=hero_image, hero_caption=hero_caption, quote=quote, kicker=kicker, noindex=noindex,
             layout=layout, cta=cta, nav_label=nav_label or h1, card_new=card_new, sources=list(sources),
             county=county, section_label=section_label, priority=priority, changefreq=changefreq, tags=list(tags))
    PAGES.append(p)
    BY_SLUG[slug] = p
    return p


# ---------- HTML helpers (return strings) ----------

def A(slug, text, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="[[{slug}]]"{c}>{text}</a>'


def ext(url, text, nofollow=False):
    rel = "noopener nofollow" if nofollow else "noopener"
    return f'<a href="{esc(url)}" rel="{rel}" target="_blank">{text}</a>'


def img(name, alt, cls="", lazy=True):
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="[[img:{name}]]" alt="{esc(alt)}"{c}{l}>'


def p(text):
    return f"<p>{text}</p>"


def ul(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def checks(items):
    return ul(items, "checks")


def steps(items):
    """items: list of (bold title, text)."""
    return '<ol class="steps">' + "".join(f"<li><b>{t}</b>{x}</li>" for t, x in items) + "</ol>"


def callout(text, blue=False):
    return f'<div class="callout{" blue" if blue else ""}"><p>{text}</p></div>'


def answer(text, label="The short answer"):
    return f'<div class="answer"><div class="eyebrow">{esc(label)}</div><p>{text}</p></div>'


def section(inner, cls="", label=None, title=None, lead=None, wrap=True):
    head = ""
    if title:
        head = '<div class="section-head">' + (f'<div class="eyebrow">{esc(label)}</div>' if label else "") + f"<h2>{title}</h2>" + (f'<p class="lead">{lead}</p>' if lead else "") + "</div>"
    body = f'<div class="wrap">{head}{inner}</div>' if wrap else head + inner
    return f'<section class="section {cls}">{body}</section>'


def band(title, text, primary=("contact-us", "Schedule a consultation"), phone=True):
    from . import firm
    btns = f'<a class="btn light" href="[[{primary[0]}]]">{primary[1]}</a>'
    if phone:
        btns += f'<a class="btn ghost light-ghost" style="color:#fff;border-color:rgba(255,255,255,.6)" href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
    return f'<div class="band"><div><h3>{title}</h3><p>{text}</p></div><div class="actions">{btns}</div></div>'


def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def twocol(left, right):
    return f'<div class="twocol"><div>{left}</div><div>{right}</div></div>'


def sources(items):
    """items: list of (label, url, nofollow?)"""
    lis = []
    for it in items:
        label, url = it[0], it[1]
        nofollow = len(it) > 2 and it[2]
        lis.append(f"<li>{ext(url, esc(label), nofollow)}</li>")
    return '<div class="sources"><h3>Sources and further reading</h3><ul>' + "".join(lis) + "</ul></div>"


def statute(cite, url, text=None):
    return ext(url, esc(text or cite))
