"""Small inline-SVG chart helpers for the Frost Law Group search audit.

Every chart is drawn to one scale, uses thin marks, hairline gridlines and
selective direct labels; native <title> tooltips ride on every mark. Colors
follow the validated palette (blue / orange / aqua for categorical series,
one blue ramp for ordered buckets, gray for de-emphasis).
"""
import html
import math
from datetime import date

INK = "#101c2b"
INK2 = "#4a5566"
MUTED = "#7c8694"
GRID = "#e6eae8"
AXIS = "#c9cfcc"
SURF = "#ffffff"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
GRAY = "#c4c9c6"
NAVY = "#1f4e8c"
RAMP = ["#86b6ef", "#5598e7", "#256abf", "#184f95", "#0d366b"]
FONT = "'Public Sans', system-ui, -apple-system, 'Segoe UI', sans-serif"


def esc(s):
    return html.escape(str(s), quote=True)


def fmt(n):
    if n is None:
        return "–"
    if isinstance(n, float) and not n.is_integer():
        return f"{n:,.1f}"
    return f"{int(round(n)):,}"


def tw(s, size=12):
    """Rough text width for layout (Public Sans averages ~0.55em per char)."""
    return len(str(s)) * size * 0.55


def _title(t):
    return f"<title>{esc(t)}</title>" if t else ""


def bar_right(x, y, w, h, fill=BLUE, r=4, title=None):
    """Horizontal bar: square at the baseline (left), rounded at the data end."""
    w = max(w, 0)
    r = min(r, w / 2, h / 2)
    if w <= 0:
        return ""
    d = (f"M{x:.1f},{y:.1f} h{w - r:.1f} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r:.1f} "
         f"a{r},{r} 0 0 1 -{r},{r} h-{w - r:.1f} z")
    return f'<path d="{d}" fill="{fill}">{_title(title)}</path>'


def bar_up(x, y_base, w, h, fill=BLUE, r=3, title=None):
    """Column: square at the baseline (bottom), rounded at the data end (top)."""
    h = max(h, 0)
    r = min(r, w / 2, h / 2) if h > 0 else 0
    if h <= 0:
        return ""
    d = (f"M{x:.1f},{y_base:.1f} v-{h - r:.1f} a{r},{r} 0 0 1 {r},-{r} h{w - 2 * r:.1f} "
         f"a{r},{r} 0 0 1 {r},{r} v{h - r:.1f} z")
    return f'<path d="{d}" fill="{fill}">{_title(title)}</path>'


def nice_ceiling(v):
    if v <= 0:
        return 1
    mag = 10 ** math.floor(math.log10(v))
    for m in (1, 2, 2.5, 5, 10):
        if v <= m * mag:
            return m * mag
    return 10 * mag


def svg_open(w, h, aria):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" '
            f'role="img" aria-label="{esc(aria)}" style="font-family:{FONT};max-width:100%;height:auto;display:block">')


def hbar(rows, width=880, value_key="value", label_key="label", note_key="note",
         color=BLUE, highlight=None, value_fmt=fmt, aria="bar chart", row_h=30,
         bar_h=20, max_value=None, label_w=None, note_w=110):
    """Horizontal bars. rows: dicts with label/value (+ optional note, color).
    highlight: set of labels drawn in the series color while the rest go gray."""
    n = len(rows)
    lw = label_w or min(max(tw(r[label_key]) for r in rows) + 14, 300)
    vw = 70
    plot_w = width - lw - vw - (note_w if any(r.get(note_key) for r in rows) else 0) - 16
    vmax = max_value or nice_ceiling(max(r[value_key] for r in rows) or 1)
    h = n * row_h + 8
    out = [svg_open(width, h, aria)]
    for i, r in enumerate(rows):
        y = 4 + i * row_h
        lab = str(r[label_key])
        if tw(lab) > lw - 14:
            cut = int((lw - 26) / (12 * 0.55))
            lab_disp = lab[:cut].rstrip() + "…"
        else:
            lab_disp = lab
        out.append(f'<text x="{lw - 10}" y="{y + bar_h / 2 + 4}" text-anchor="end" font-size="12" fill="{INK}">'
                   f'{esc(lab_disp)}<title>{esc(lab)}</title></text>')
        w = plot_w * (r[value_key] / vmax)
        c = r.get("color") or (color if (highlight is None or lab in highlight) else GRAY)
        out.append(bar_right(lw, y + (row_h - bar_h) / 2 - 2, w, bar_h, fill=c,
                             title=f"{lab}: {value_fmt(r[value_key])}" + (f" · {r.get(note_key)}" if r.get(note_key) else "")))
        out.append(f'<text x="{lw + w + 6}" y="{y + bar_h / 2 + 4}" font-size="12" fill="{INK2}" '
                   f'font-variant-numeric="tabular-nums">{esc(value_fmt(r[value_key]))}</text>')
        if r.get(note_key):
            out.append(f'<text x="{width - 4}" y="{y + bar_h / 2 + 4}" text-anchor="end" font-size="11" fill="{MUTED}" '
                       f'font-variant-numeric="tabular-nums">{esc(r[note_key])}</text>')
    out.append(f'<line x1="{lw}" y1="2" x2="{lw}" y2="{h - 2}" stroke="{AXIS}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)


def _date_ticks(dates):
    ticks = []
    for i, d in enumerate(dates):
        if i == 0 or d.day == 1:
            ticks.append((i, d.strftime("%b %-d") if i == 0 else d.strftime("%b %-d")))
    return ticks


def line_chart(dates, series, width=880, height=250, aria="line chart", annotations=None,
               y_label="", legend=True, area=False):
    """series: list of dict(name, values, color). dates: list[date]."""
    left, right, top, bottom = 52, 24, 18, 34
    pw, ph = width - left - right, height - top - bottom
    vmax = nice_ceiling(max(max(s["values"]) for s in series) or 1)
    n = len(dates)
    xs = [left + pw * i / max(n - 1, 1) for i in range(n)]

    def ys(v):
        return top + ph - ph * v / vmax

    out = [svg_open(width, height + (26 if legend and len(series) > 1 else 0), aria)]
    steps = 4
    for k in range(steps + 1):
        v = vmax * k / steps
        y = ys(v)
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + pw}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{MUTED}" '
                   f'font-variant-numeric="tabular-nums">{fmt(v)}</text>')
    for i, lab in _date_ticks(dates):
        out.append(f'<line x1="{xs[i]:.1f}" y1="{top + ph}" x2="{xs[i]:.1f}" y2="{top + ph + 5}" stroke="{AXIS}"/>')
        anchor = "start" if i == 0 else "middle"
        out.append(f'<text x="{xs[i]:.1f}" y="{top + ph + 18}" text-anchor="{anchor}" font-size="11" fill="{MUTED}">{lab}</text>')
    out.append(f'<line x1="{left}" y1="{top + ph}" x2="{left + pw}" y2="{top + ph}" stroke="{AXIS}" stroke-width="1"/>')
    for s in series:
        pts = [(xs[i], ys(v)) for i, v in enumerate(s["values"])]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        if area:
            out.append(f'<path d="{d} L{pts[-1][0]:.1f},{top + ph} L{pts[0][0]:.1f},{top + ph} z" fill="{s["color"]}" fill-opacity="0.10"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{s["color"]}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
        # invisible hover targets with tooltips
        for i, (x, y) in enumerate(pts):
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="transparent">'
                       f'<title>{dates[i].strftime("%b %-d, %Y")} · {s["name"]}: {fmt(s["values"][i])}</title></circle>')
        ex, ey = pts[-1]
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{s["color"]}" stroke="{SURF}" stroke-width="2"/>')
    for a in (annotations or []):
        i, text, s_idx = a["index"], a["text"], a.get("series", 0)
        v = series[s_idx]["values"][i]
        x, y = xs[i], ys(v)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{series[s_idx]["color"]}" stroke="{SURF}" stroke-width="2"/>')
        tx = x - 8 if x > left + pw * 0.6 else x + 8
        anchor = "end" if x > left + pw * 0.6 else "start"
        ty = max(y - 10, top + 10)
        out.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-size="11" fill="{INK2}">{esc(text)}</text>')
    if legend and len(series) > 1:
        lx = left
        ly = height + 14
        for s in series:
            out.append(f'<rect x="{lx}" y="{ly - 8}" width="14" height="4" rx="2" fill="{s["color"]}"/>')
            out.append(f'<text x="{lx + 20}" y="{ly}" font-size="12" fill="{INK2}">{esc(s["name"])}</text>')
            lx += 30 + tw(s["name"])
    out.append("</svg>")
    return "".join(out)


def columns(dates, values, width=880, height=170, color=BLUE, aria="column chart", label_max=True):
    left, right, top, bottom = 52, 24, 14, 34
    pw, ph = width - left - right, height - top - bottom
    vmax = nice_ceiling(max(values) or 1)
    n = len(values)
    slot = pw / n
    bw = min(8, max(2, slot - 2))
    out = [svg_open(width, height, aria)]
    for k in range(0, 3):
        v = vmax * k / 2
        y = top + ph - ph * v / vmax
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + pw}" y2="{y:.1f}" stroke="{GRID}"/>')
        out.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="11" fill="{MUTED}">{fmt(v)}</text>')
    imax = max(range(n), key=lambda i: values[i])
    for i, v in enumerate(values):
        x = left + slot * i + (slot - bw) / 2
        h = ph * v / vmax
        out.append(bar_up(x, top + ph, bw, h, fill=color, title=f"{dates[i].strftime('%b %-d, %Y')}: {fmt(v)}"))
        if label_max and i == imax and v > 0:
            out.append(f'<text x="{x + bw / 2:.1f}" y="{top + ph - h - 5:.1f}" text-anchor="middle" font-size="11" fill="{INK2}">{fmt(v)}</text>')
    for i, lab in _date_ticks(dates):
        x = left + slot * i + slot / 2
        anchor = "start" if i == 0 else "middle"
        out.append(f'<text x="{x:.1f}" y="{top + ph + 18}" text-anchor="{anchor}" font-size="11" fill="{MUTED}">{lab}</text>')
    out.append(f'<line x1="{left}" y1="{top + ph}" x2="{left + pw}" y2="{top + ph}" stroke="{AXIS}"/>')
    out.append("</svg>")
    return "".join(out)


def stacked_bar(segments, width=880, height=28, aria="stacked bar", total_label=None):
    """One part-to-whole bar. segments: list of (label, value, color)."""
    total = sum(v for _, v, _ in segments) or 1
    gap = 2
    out = [svg_open(width, height + 30, aria)]
    x = 0
    for i, (lab, v, c) in enumerate(segments):
        w = (width - gap * (len(segments) - 1)) * v / total
        out.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="{height}" rx="0" fill="{c}"><title>{esc(lab)}: {fmt(v)} ({v / total:.0%})</title></rect>')
        pct = f"{v / total:.0%}"
        if w > tw(pct) + 12:
            fill = "#ffffff" if c not in (RAMP[0], GRAY, "#eda100", AQUA) else INK
            out.append(f'<text x="{x + w / 2:.1f}" y="{height / 2 + 4}" text-anchor="middle" font-size="12" font-weight="600" fill="{fill}">{pct}</text>')
        x += w + gap
    lx = 0
    ly = height + 20
    for lab, v, c in segments:
        out.append(f'<rect x="{lx}" y="{ly - 10}" width="12" height="12" rx="2" fill="{c}"/>')
        t = f"{lab} · {fmt(v)}"
        out.append(f'<text x="{lx + 17}" y="{ly}" font-size="12" fill="{INK2}">{esc(t)}</text>')
        lx += 30 + tw(t)
    out.append("</svg>")
    return "".join(out)


def dumbbell(rows, a_name, b_name, width=880, a_color=BLUE, b_color=ORANGE, xmax=100,
             aria="dumbbell chart", row_h=30, label_w=300):
    """rows: (label, a_value, b_value). Lower x = better (Google position)."""
    n = len(rows)
    left = label_w
    right = 20
    pw = width - left - right
    top = 26
    h = top + n * row_h + 56

    def xs(v):
        return left + pw * (v - 1) / (xmax - 1)

    out = [svg_open(width, h, aria)]
    ticks = [1, 10, 20, 30, 50, 75, 100]
    axis_y = top + n * row_h + 6
    out.append(f'<rect x="{xs(1):.1f}" y="{top}" width="{xs(10) - xs(1):.1f}" height="{axis_y - top:.1f}" fill="{BLUE}" fill-opacity="0.06"/>')
    out.append(f'<text x="{xs(1) + 4:.1f}" y="{top - 8}" font-size="10.5" fill="{MUTED}">page 1 (positions 1\u201310)</text>')
    out.append(f'<text x="{width - right}" y="{top - 8}" text-anchor="end" font-size="10.5" fill="{MUTED}">\u2190 better \u00b7 Google position \u00b7 worse \u2192</text>')
    for t in ticks:
        x = xs(t)
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{axis_y}" stroke="{GRID}"/>')
        out.append(f'<text x="{x:.1f}" y="{axis_y + 16}" text-anchor="middle" font-size="11" fill="{MUTED}">{t}</text>')
    for i, (lab, a, b) in enumerate(rows):
        y = top + i * row_h + row_h / 2
        out.append(f'<text x="{left - 12}" y="{y + 4}" text-anchor="end" font-size="12" fill="{INK}">{esc(lab)}</text>')
        xa, xb = xs(min(a, xmax)), xs(min(b, xmax))
        out.append(f'<line x1="{xa:.1f}" y1="{y}" x2="{xb:.1f}" y2="{y}" stroke="{AXIS}" stroke-width="2" stroke-linecap="round"/>')
        out.append(f'<circle cx="{xa:.1f}" cy="{y}" r="5" fill="{a_color}" stroke="{SURF}" stroke-width="2"><title>{esc(lab)} \u00b7 {a_name}: position {a:g}</title></circle>')
        out.append(f'<circle cx="{xb:.1f}" cy="{y}" r="5" fill="{b_color}" stroke="{SURF}" stroke-width="2"><title>{esc(lab)} \u00b7 {b_name}: position {b:g}</title></circle>')
    ly = h - 10
    out.append(f'<circle cx="{left + 6}" cy="{ly - 4}" r="5" fill="{a_color}"/><text x="{left + 16}" y="{ly}" font-size="12" fill="{INK2}">{esc(a_name)}</text>')
    lx = left + 16 + tw(a_name) + 26
    out.append(f'<circle cx="{lx}" cy="{ly - 4}" r="5" fill="{b_color}"/><text x="{lx + 10}" y="{ly}" font-size="12" fill="{INK2}">{esc(b_name)}</text>')
    out.append("</svg>")
    return "".join(out)


def bucket_bar(buckets, width=880, aria="position buckets"):
    """Ordered buckets as one stacked bar in the ordinal ramp. buckets: list of (label, value)."""
    segs = [(lab, v, RAMP[min(i, len(RAMP) - 1)]) for i, (lab, v) in enumerate(buckets)]
    return stacked_bar(segs, width=width, aria=aria)
