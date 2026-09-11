"""Static explanatory diagrams (inline SVG) for the Frost Law Group search audit."""
import math
from charts import esc, tw, svg_open, INK, INK2, MUTED, GRID, AXIS, BLUE, ORANGE, AQUA, NAVY, GRAY, SURF

PAPER = "#f3f0fa"
AZALEA = "#a855f7"


def wrap(text, w, fs=12):
    words, lines, cur = str(text).split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(t, fs) > w - 18 and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def box(x, y, w, h, text, fill=SURF, stroke=AXIS, fs=12, weight=400, color=INK, r=6, sub=None, sw=1):
    lines = wrap(text, w, fs)
    sub_lines = wrap(sub, w, fs - 1) if sub else []
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    total = len(lines) * (fs + 3) + len(sub_lines) * (fs - 1 + 3)
    ty = y + h / 2 - total / 2 + fs
    for ln in lines:
        out.append(f'<text x="{x + w / 2:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="{fs}" font-weight="{weight}" fill="{color}">{esc(ln)}</text>')
        ty += fs + 3
    for ln in sub_lines:
        out.append(f'<text x="{x + w / 2:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="{fs - 1}" fill="{MUTED if color == INK else color}" fill-opacity="{1 if color == INK else 0.85}">{esc(ln)}</text>')
        ty += fs - 1 + 3
    return "".join(out)


def arrow(x1, y1, x2, y2, color=AXIS, width=1.5):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 7 * math.cos(ang), y2 - 7 * math.sin(ang)
    p1 = (hx + 4 * math.sin(ang), hy - 4 * math.cos(ang))
    p2 = (hx - 4 * math.sin(ang), hy + 4 * math.cos(ang))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{color}" stroke-width="{width}"/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')


def flow(steps, width=880, h=96, aria="flow diagram"):
    """steps: list of (title, subtitle, fill). Horizontal boxes joined by arrows."""
    n = len(steps)
    gap = 26
    bw = (width - gap * (n - 1)) / n
    out = [svg_open(width, h, aria)]
    for i, (t, s, fill) in enumerate(steps):
        x = i * (bw + gap)
        color = "#ffffff" if fill in (NAVY, BLUE, AZALEA, ORANGE) else INK
        out.append(box(x, 8, bw, h - 16, t, fill=fill, stroke=fill if fill != SURF else AXIS, fs=13, weight=600, color=color, sub=s))
        if i < n - 1:
            out.append(arrow(x + bw + 3, h / 2, x + bw + gap - 3, h / 2, color=MUTED))
    out.append("</svg>")
    return "".join(out)


def hub_spoke(hub, spokes, width=880, aria="topic map", hub_fill=NAVY, spoke_fill=SURF, accent=BLUE):
    """Hub in the middle, spokes on a ring. spokes: list of str or (str, 'new'|'existing')."""
    n = len(spokes)
    sw, sh = 168, 42
    rows_per_side = math.ceil(n / 2)
    height = max(rows_per_side * (sh + 12) + 40, 260)
    cx, cy = width / 2, height / 2
    out = [svg_open(width, height, aria)]
    hw, hh = 190, 66
    out.append(box(cx - hw / 2, cy - hh / 2, hw, hh, hub, fill=hub_fill, stroke=hub_fill, fs=14, weight=700, color="#ffffff", r=10))
    left = spokes[:rows_per_side]
    right = spokes[rows_per_side:]
    for side, items in (("L", left), ("R", right)):
        total_h = len(items) * (sh + 12) - 12
        y0 = cy - total_h / 2
        for j, it in enumerate(items):
            label, kind = (it if isinstance(it, tuple) else (it, "existing"))
            y = y0 + j * (sh + 12)
            x = 20 if side == "L" else width - 20 - sw
            fill = spoke_fill if kind == "existing" else "#eef4fb"
            stroke = AXIS if kind == "existing" else accent
            out.append(box(x, y, sw, sh, label, fill=fill, stroke=stroke, fs=11.5, weight=500, r=6, sub=("new page" if kind == "new" else None)))
            if side == "L":
                out.append(f'<line x1="{x + sw:.1f}" y1="{y + sh / 2:.1f}" x2="{cx - hw / 2:.1f}" y2="{cy:.1f}" stroke="{GRID}" stroke-width="1.2"/>')
            else:
                out.append(f'<line x1="{x:.1f}" y1="{y + sh / 2:.1f}" x2="{cx + hw / 2:.1f}" y2="{cy:.1f}" stroke="{GRID}" stroke-width="1.2"/>')
    # redraw hub on top of lines
    out.append(box(cx - hw / 2, cy - hh / 2, hw, hh, hub, fill=hub_fill, stroke=hub_fill, fs=14, weight=700, color="#ffffff", r=10))
    out.append("</svg>")
    return "".join(out)


def fanout(question, subs, width=880, aria="query fan-out diagram"):
    """One big question splits into sub-questions; each sub-question needs one page.
    subs: list of (sub_question, page_label, status) where status in ('have','gap')."""
    n = len(subs)
    top_h = 60
    row_y = 110
    bw = min(200, (width - 20 * (n - 1)) / n)
    total = n * bw + 20 * (n - 1)
    x0 = (width - total) / 2
    height = row_y + 118 + 60
    out = [svg_open(width, height, aria)]
    out.append(box(width / 2 - 260, 6, 520, top_h, question, fill=NAVY, stroke=NAVY, fs=14, weight=600, color="#ffffff", r=10, sub="what the person actually types or says"))
    for i, (sq, page, status) in enumerate(subs):
        x = x0 + i * (bw + 20)
        out.append(arrow(width / 2, 6 + top_h, x + bw / 2, row_y - 4, color=MUTED))
        out.append(box(x, row_y, bw, 62, sq, fill="#eef4fb", stroke=BLUE, fs=11, weight=500, r=6))
        fill = "#e8f7f0" if status == "have" else "#fdf1ec"
        stroke = AQUA if status == "have" else ORANGE
        out.append(arrow(x + bw / 2, row_y + 62, x + bw / 2, row_y + 62 + 22, color=MUTED))
        out.append(box(x, row_y + 86, bw, 50, page, fill=fill, stroke=stroke, fs=11, weight=600, r=6, sub=("page exists" if status == "have" else "page missing → build it")))
    out.append(f'<text x="{width / 2:.1f}" y="{height - 8}" text-anchor="middle" font-size="11" fill="{MUTED}">Google\'s AI runs the small questions, then stitches the answers — one clean page per small question is how you get picked.</text>')
    out.append("</svg>")
    return "".join(out)


def cycle(steps, width=880, aria="content flywheel"):
    """steps: list of (title, sub, fill). Laid out on a ring with arrows between neighbours."""
    n = len(steps)
    height = 420
    cx, cy = width / 2, height / 2
    rx, ry = width / 2 - 120, height / 2 - 50
    bw, bh = 170, 58
    out = [svg_open(width, height, aria)]
    pts = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        # shorten to box edges
        ang = math.atan2(y2 - y1, x2 - x1)
        sx, sy = x1 + math.cos(ang) * 96, y1 + math.sin(ang) * 40
        ex, ey = x2 - math.cos(ang) * 96, y2 - math.sin(ang) * 40
        out.append(arrow(sx, sy, ex, ey, color=MUTED))
    for i, (t, s, fill) in enumerate(steps):
        x, y = pts[i]
        color = "#ffffff" if fill in (NAVY, BLUE, AZALEA, ORANGE) else INK
        out.append(box(x - bw / 2, y - bh / 2, bw, bh, t, fill=fill, stroke=fill if fill != SURF else AXIS, fs=12.5, weight=600, color=color, sub=s, r=8))
    out.append(box(cx - 90, cy - 26, 180, 52, "One piece of work, seven places", fill=PAPER, stroke=PAPER, fs=12, weight=600, r=26))
    out.append("</svg>")
    return "".join(out)


def gantt(rows, weeks=13, width=880, aria="90-day plan", label_w=300):
    """rows: list of (label, start_week, end_week, color, phase)."""
    row_h = 26
    top = 30
    h = top + len(rows) * row_h + 14
    pw = width - label_w - 16
    ww = pw / weeks
    out = [svg_open(width, h, aria)]
    for k in range(weeks):
        x = label_w + k * ww
        out.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{h - 10}" stroke="{GRID}"/>')
        out.append(f'<text x="{x + ww / 2:.1f}" y="{top - 12}" text-anchor="middle" font-size="10.5" fill="{MUTED}">W{k + 1}</text>')
    for i, (label, s, e, color, phase) in enumerate(rows):
        y = top + i * row_h
        if label.startswith("##"):
            out.append(f'<text x="0" y="{y + 17}" font-size="11" font-weight="700" fill="{INK2}" letter-spacing="0.06em">{esc(label[2:].strip().upper())}</text>')
            continue
        out.append(f'<text x="{label_w - 12}" y="{y + 17}" text-anchor="end" font-size="12" fill="{INK}">{esc(label)}</text>')
        x1 = label_w + (s - 1) * ww + 2
        x2 = label_w + e * ww - 2
        out.append(f'<rect x="{x1:.1f}" y="{y + 5}" width="{x2 - x1:.1f}" height="16" rx="4" fill="{color}"><title>{esc(label)}: weeks {s}–{e}</title></rect>')
    out.append("</svg>")
    return "".join(out)


def two_sites(width=880, aria="two-site architecture"):
    h = 420
    out = [svg_open(width, h, aria)]
    lw = 380
    # main site
    out.append(f'<rect x="10" y="10" width="{lw}" height="{h - 20}" rx="12" fill="#ffffff" stroke="{AXIS}"/>')
    out.append(f'<text x="{10 + lw / 2}" y="36" text-anchor="middle" font-size="14" font-weight="700" fill="{NAVY}">frostlawgroupsc.com</text>')
    out.append(f'<text x="{10 + lw / 2}" y="54" text-anchor="middle" font-size="11" fill="{MUTED}">the firm · estate planning · probate · criminal defense</text>')
    items = ["Estate Planning hub", "Probate hub", "Criminal Defense + DUI hub", "Guardianship & conservatorship", "County court guides", "Attorney bios · reviews · contact"]
    for i, it in enumerate(items):
        y = 70 + i * 46
        out.append(box(30, y, lw - 40, 36, it, fill="#eef4fb", stroke=BLUE, fs=12, weight=500))
    # PI site
    rx0 = width - 10 - lw
    out.append(f'<rect x="{rx0}" y="10" width="{lw}" height="{h - 20}" rx="12" fill="#ffffff" stroke="{AXIS}"/>')
    out.append(f'<text x="{rx0 + lw / 2}" y="36" text-anchor="middle" font-size="14" font-weight="700" fill="{ORANGE}">summervilleaccidentattorney.com</text>')
    out.append(f'<text x="{rx0 + lw / 2}" y="54" text-anchor="middle" font-size="11" fill="{MUTED}">injury only · car · truck · motorcycle · dog bite · wrongful death</text>')
    items2 = ["Car accident hub (+ rideshare, hit-and-run, DUI victims)", "Truck · motorcycle · pedestrian hubs", "Dog bite hub (SC strict liability)", "City pages: Goose Creek, Ladson, Moncks Corner, N. Charleston…", "Spanish: abogado de accidentes", "After-the-crash guides · case results · bios"]
    for i, it in enumerate(items2):
        y = 70 + i * 46
        out.append(box(rx0 + 20, y, lw - 40, 36, it, fill="#fdf1ec", stroke=ORANGE, fs=12, weight=500))
    # middle links
    mx = width / 2
    out.append(box(mx - 52, 140, 104, 44, "cross-links in header + footer", fill=PAPER, stroke=PAPER, fs=10.5, weight=600, r=8))
    out.append(arrow(10 + lw, 162, mx - 54, 162, color=MUTED))
    out.append(arrow(rx0, 162, mx + 54, 162, color=MUTED))
    out.append(box(mx - 52, 220, 104, 44, "same name, address, phone + schema", fill=PAPER, stroke=PAPER, fs=10.5, weight=600, r=8))
    out.append(box(mx - 52, 300, 104, 56, "Google Business Profile → main site only", fill="#fff7e6", stroke="#eda100", fs=10.5, weight=600, r=8))
    out.append(arrow(mx - 54, 328, 10 + lw + 4, 328, color="#eda100"))
    out.append(f'<text x="{mx}" y="{h - 12}" text-anchor="middle" font-size="11" fill="{MUTED}">Rule 1: no page on either site targets the other site\'s subject.</text>')
    out.append("</svg>")
    return "".join(out)


def serp_zones(width=880, aria="where you can appear on a results page"):
    h = 300
    out = [svg_open(width, h, aria)]
    out.append(f'<rect x="0" y="0" width="{width}" height="{h}" rx="12" fill="#ffffff" stroke="{AXIS}"/>')
    out.append(f'<rect x="20" y="16" width="{width - 40}" height="34" rx="17" fill="{PAPER}"/>')
    out.append(f'<text x="40" y="38" font-size="13" fill="{INK2}">probate attorney summerville sc</text>')
    zones = [
        ("AI answer (AI Overview / AI Mode)", "built from many pages · the fan-out questions live here", "#eef4fb", BLUE),
        ("Map pack (3 Business Profiles)", "your Google Business Profile + reviews + photos", "#fff7e6", "#eda100"),
        ("Blue links (10 pages)", "your website pages · titles · descriptions", "#e8f7f0", AQUA),
    ]
    y = 64
    for t, s, fill, stroke in zones:
        out.append(box(20, y, width - 40, 62, t, fill=fill, stroke=stroke, fs=13, weight=600, sub=s, r=8))
        y += 74
    out.append("</svg>")
    return "".join(out)
