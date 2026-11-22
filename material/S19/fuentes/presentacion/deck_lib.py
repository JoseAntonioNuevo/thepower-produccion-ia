"""Helpers visuales para la presentación S19.

Copia adaptada de material/S17/fuentes/rediseno-visual/deck_lib.py (sistema visual del ejemplo
que marca el diseño). Cambios: bloques y pie de S19, rutas de assets, y al final los añadidos
para S19 (estilo «sencillo» del ejemplo, portada, cierre, barras y paneles de terminal).

Unidades en puntos sobre un lienzo 16:9 de 960 x 540 pt.
"""
import math
import os

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
REPO_ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))
# QR vigente de AI Engineer: copia byte a byte de material/S16/assets en material/S19/assets.
QR_PATH = os.path.join(REPO_ASSETS, "qr-ai-engineer.jpg")

# Paleta tomada de la referencia S12 (rediseño oscuro).
BG = "0F1B22"
BG_SECTION = "123630"
CARD = "18272E"
CARD2 = "1E3038"
BORDER = "33474F"
TITLE = "EAF1F2"
TEXT = "C3D0D4"
MUTED = "9AABB1"
FAINT = "6F8389"
MINT = "4FD1A1"
MINT_L = "A8F0D0"
TAKE_BG = "133A30"
BLUE = "7AB2EA"
BLUE_BG = "182C40"
AMBER = "E2B04F"
AMBER_BG = "372D18"
CORAL = "F08A6E"
CORAL_BG = "3B2520"
VIOLET = "B09CF2"
VIOLET_BG = "29233F"
PINK = "D98BBE"
PINK_BG = "38212F"
GREEN_BG = "15332B"
DARK = "0F1B22"

# Colores del esquema claro que imita una pantalla de consola (rotulado como esquema).
UI_BG = "F2F3F3"
UI_CARD = "FFFFFF"
UI_TEXT = "16191F"
UI_LABEL = "414D5C"
UI_MUTED = "5F6B7A"
UI_LINE = "C6CBD1"
UI_BLUE = "0972D3"
UI_ORANGE = "FF9900"
UI_NAV = "232F3E"

SERIF = "Georgia"
SANS = "Arial"
MONO = "Courier New"

BLOCKS = ["Qué medir", "Recuperación", "Generación", "Testing", "Producción", "Práctica y cierre"]
BLOCK_COLORS = [MINT, PINK, AMBER, VIOLET, BLUE, MINT_L]
PIE = "thePower · AI Engineer · S19"

WARNINGS = []


def P(v):
    return Emu(int(round(v * 12700)))


def rgb(h):
    return RGBColor.from_string(h)


def asset(name):
    if name == "qr-ai-engineer.jpg":
        return QR_PATH
    p = os.path.join(ASSETS, name)
    if not os.path.exists(p):
        p = os.path.join(REPO_ASSETS, name)
    return p


# ---------------------------------------------------------------- texto
CW = {SANS: 0.50, SERIF: 0.50, MONO: 0.60}


def _est_lines(text, w, size, font, bold):
    cw = CW.get(font, 0.5) * (1.06 if bold else 1.0) * size
    per_line = max(1, int(w / cw))
    lines = 0
    for para in text.split("\n"):
        lines += max(1, math.ceil(len(para) / per_line))
    return lines


def text(sl, x, y, w, h, paras, size=11, color=TEXT, font=SANS, bold=False, italic=False,
         align="l", anchor="t", lsp=None, space=0, check=True, name=None):
    """Caja de texto editable. `paras` = str | [párrafo]; párrafo = str | [(texto, estilo)] | dict."""
    tb = sl.shapes.add_textbox(P(x), P(y), P(w), P(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = paras.split("\n")
    total_lines = 0
    maxsize = size
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pal = align
        psp = space
        if isinstance(para, dict):
            pal = para.get("align", align)
            psp = para.get("space", space)
            para = para["runs"]
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[pal]
        if lsp:
            p.line_spacing = lsp
        if psp and i < len(paras) - 1:
            p.space_after = Pt(psp)
        runs = [(para, {})] if isinstance(para, str) else para
        plain = ""
        for t, st in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            sz = st.get("size", size)
            maxsize = max(maxsize, sz)
            f.size = Pt(sz)
            f.name = st.get("font", font)
            f.bold = st.get("bold", bold)
            f.italic = st.get("italic", italic)
            f.color.rgb = rgb(st.get("color", color))
            plain += t
        total_lines += _est_lines(plain, w, maxsize, font, bold)
    if check:
        need = total_lines * maxsize * 1.18 + space * (len(paras) - 1)
        if need > h + 2:
            WARNINGS.append(f"[{getattr(sl, '_tag', '?')}] posible desborde ({need:.0f}>{h:.0f}pt): {str(paras)[:70]}")
    return tb


# ---------------------------------------------------------------- formas
def box(sl, x, y, w, h, fill=CARD, line=None, lw=0.75, radius=6, dash=False, shape=None):
    if shape is None:
        shape = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    s = sl.shapes.add_shape(shape, P(x), P(y), P(w), P(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = min(0.5, radius / max(1, min(w, h)))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def circle(sl, x, y, d, fill, line=None, lw=0.75):
    return box(sl, x, y, d, d, fill=fill, line=line, lw=lw, radius=0, shape=MSO_SHAPE.OVAL)


def shape_text(s, t, size=10, color=TITLE, bold=True, font=SANS, align="c", anchor="m", ml=4):
    tf = s.text_frame
    tf.margin_left = tf.margin_right = P(ml)
    tf.margin_top = tf.margin_bottom = 0
    tf.word_wrap = True
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    lines = t.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.name = font
        r.font.color.rgb = rgb(color)
    return s


def chip(sl, x, y, w, h, t, fill=CARD2, color=TITLE, size=9.5, bold=True, line=None, radius=None, font=SANS, align="c"):
    s = box(sl, x, y, w, h, fill=fill, line=line, radius=h / 2 if radius is None else radius)
    return shape_text(s, t, size=size, color=color, bold=bold, font=font, align=align)


def badge(sl, x, y, n, fill=AMBER, color=DARK, d=16, size=9):
    s = circle(sl, x, y, d, fill)
    return shape_text(s, str(n), size=size, color=color, bold=True, ml=0)


def line(sl, x1, y1, x2, y2, color=MUTED, w=1.25, head="end", dash=False):
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, P(x1), P(y1), P(x2), P(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(w)
    if dash:
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    ln = c.line._get_or_add_ln()
    if head in ("start", "both"):
        e = etree.SubElement(ln, qn("a:headEnd"))
        e.set("type", "triangle")
        e.set("w", "med")
        e.set("len", "med")
    if head in ("end", "both"):
        e = etree.SubElement(ln, qn("a:tailEnd"))
        e.set("type", "triangle")
        e.set("w", "med")
        e.set("len", "med")
    return c


def poly(sl, pts, color=MUTED, w=1.25, dash=False, head="end"):
    for i in range(len(pts) - 1):
        hd = head if i == len(pts) - 2 else "none"
        if head == "start" and i == 0:
            hd = "start"
        elif head == "start":
            hd = "none"
        line(sl, *pts[i], *pts[i + 1], color=color, w=w, head=hd, dash=dash)


def img(sl, name, x, y, w=None, h=None):
    path = asset(name)
    iw, ih = Image.open(path).size
    if w and not h:
        h = w * ih / iw
    elif h and not w:
        w = h * iw / ih
    return sl.shapes.add_picture(path, P(x), P(y), P(w), P(h))


def img_size(name, w=None, h=None):
    iw, ih = Image.open(asset(name)).size
    if w:
        return w, w * ih / iw
    return h * iw / ih, h


# ---------------------------------------------------------------- estructura de diapositiva
class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = P(960)
        self.prs.slide_height = P(540)
        self.n = 0

    def slide(self, bg=BG, tag=""):
        sl = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        sl.background.fill.solid()
        sl.background.fill.fore_color.rgb = rgb(bg)
        self.n += 1
        sl._num = self.n
        sl._tag = f"{self.n}:{tag}"
        return sl

    def save(self, path):
        self.prs.save(path)


def notes(sl, t):
    sl.notes_slide.notes_text_frame.text = t.strip()


def header(sl, kicker, title, sub=None, sub_w=874, sub_h=36):
    text(sl, 43, 25, 874, 14, kicker.upper(), size=9, color=MINT, bold=True)
    text(sl, 43, 41, 874, 40, title, size=27, color=TITLE, font=SERIF)
    if sub:
        text(sl, 43, 85, sub_w, sub_h, sub, size=12.5, color=TEXT)


def footer(sl, n=None, block=None):
    text(sl, 43, 513, 170, 12, PIE, size=8.5, color=FAINT, check=False)
    runs = []
    for i, b in enumerate(BLOCKS, 1):
        act = i == block
        runs.append((f"{i} {b}", {"bold": act, "color": BLOCK_COLORS[i - 1] if act else FAINT}))
        if i < len(BLOCKS):
            runs.append(("   ", {"color": FAINT}))
    text(sl, 200, 513, 660, 12, [runs], size=8, align="c", check=False)
    text(sl, 870, 513, 47, 12, str(getattr(sl, "_num", n)), size=8.5, color=FAINT, align="r", check=False)


def takeaway(sl, t, label=None, y=476, h=26, fill=TAKE_BG, lab_color=MINT):
    box(sl, 43, y, 874, h, fill=fill, radius=4)
    runs = []
    if label:
        runs.append((label.upper() + "   ", {"bold": True, "color": lab_color, "size": 9}))
    runs.append((t, {}))
    text(sl, 54, y, 856, h, [runs], size=11, color=TITLE, anchor="m")


def card(sl, x, y, w, h, title=None, body=None, icon=None, accent=MINT, fill=CARD, line=None,
         tsize=13, bsize=10.5, tfont=SERIF, icon_s=28, pad=12, tcolor=TITLE, bcolor=TEXT, num=None):
    box(sl, x, y, w, h, fill=fill, line=line)
    cx = x + pad
    ty = y + pad
    if icon:
        img(sl, icon, cx, ty - 1, w=icon_s, h=icon_s)
        tx = cx + icon_s + 9
    else:
        tx = cx
    if num is not None:
        badge(sl, x + w - pad - 16, y + pad - 2, num, fill=accent)
    tw = x + w - pad - tx - (20 if num is not None else 0)
    if title:
        th = icon_s if icon else tsize * 1.4
        text(sl, tx, ty + (icon_s - tsize * 1.25) / 2 if icon else ty, tw, tsize * 1.35 * (1 if len(title) * CW.get(tfont, .5) * tsize < tw else 2),
             title, size=tsize, font=tfont, color=tcolor, bold=(tfont == SANS))
        by = ty + max(th, tsize * 1.4) + 6
    else:
        by = ty
    if body:
        text(sl, cx, by, w - 2 * pad, y + h - by - pad + 2, body, size=bsize, color=bcolor)


def divider(deck, num, block_name, title, sub, bullets, icons, minutes):
    sl = deck.slide(BG_SECTION, tag=f"div{num}")
    img(sl, "thepower-logo.png", 38, 30, h=30)
    text(sl, 43, 92, 140, 170, str(num), size=150, font=SERIF, color=MINT_L, check=False)
    x0 = 205
    text(sl, x0, 108, 560, 14, f"BLOQUE {num} · {block_name.upper()}  ·  {minutes}", size=10, color=MINT, bold=True)
    tl = _est_lines(title, 520, 29, SERIF, False)
    text(sl, x0, 126, 520, 76, title, size=29, font=SERIF, color=TITLE)
    sy = 126 + tl * 36 + 6
    text(sl, x0, sy, 520, 36, sub, size=13, color=TEXT)
    text(sl, x0, 252, 300, 12, "EN ESTE BLOQUE", size=9, color=MUTED, bold=True)
    yy = 272
    for b in bullets:
        circle(sl, x0 + 2, yy + 5, 6, MINT)
        text(sl, x0 + 18, yy, 480, 18, b, size=12.5, color=TITLE)
        yy += 24
    # iconos oficiales de los servicios del bloque
    ix = 745
    iy = 112
    for ic, lab in icons:
        img(sl, ic, ix, iy, w=46, h=46)
        text(sl, ix + 56, iy + 8, 130, 32, lab, size=11, color=TITLE, bold=True)
        iy += 64
    # navegación por bloques
    n = len(BLOCKS)
    pw = (874 - (n - 1) * 6) / n
    for i, b in enumerate(BLOCKS, 1):
        act = i == num
        chip(sl, 43 + (i - 1) * (pw + 6), 472, pw, 24, f"{i}  {b}",
             fill=MINT_L if act else "1A463C", color=DARK if act else "8FB5AA", size=8.5, bold=act)
    return sl


def console_panel(sl, x, y, w, h, path, items, title="EN LA CONSOLA", accent=MINT, size=10.5):
    """Recuadro estándar: ruta de la consola y qué señalar."""
    box(sl, x, y, w, h, fill=CARD, line=BORDER)
    img(sl, "aws-console.png", x + 10, y + 10, w=20, h=20)
    text(sl, x + 36, y + 13, w - 46, 14, title, size=9, color=accent, bold=True)
    text(sl, x + 10, y + 36, w - 20, 30, path, size=10, font=MONO, color=MINT_L, bold=True)
    pr = []
    for it in items:
        pr.append({"runs": [("›  ", {"color": accent, "bold": True}), (it, {})], "space": 3})
    text(sl, x + 10, y + 36 + 14 * max(1, _est_lines(path, w - 20, 10, MONO, True)) + 8, w - 20,
         h - (36 + 14 * max(1, _est_lines(path, w - 20, 10, MONO, True)) + 8) - 8, pr, size=size, color=TEXT, space=3)


def cost_chip(sl, x, y, w, t, h=None, size=10):
    lines = _est_lines("COSTE  " + t, w - 20, size, SANS, False)
    h = h or (lines * size * 1.2 + 12)
    box(sl, x, y, w, h, fill=AMBER_BG, radius=5)
    text(sl, x + 10, y + 6, w - 20, h - 10, [[("COSTE  ", {"bold": True, "color": AMBER, "size": 8.5}), (t, {})]], size=size, color=TITLE)
    return h


def esquema_label(sl, x, y, w=150, t="ESQUEMA · no es una captura"):
    chip(sl, x, y, w, 15, t, fill=AMBER, color=DARK, size=8, radius=3)


def ui_panel(sl, x, y, w, h, title=None, crumbs=None):
    """Panel claro que representa una pantalla de consola de forma esquemática."""
    box(sl, x, y, w, h, fill=UI_BG, line="AEB5BD", radius=4)
    bar = box(sl, x, y, w, 18, fill=UI_NAV, radius=0)
    text(sl, x + 8, y + 3, 120, 12, "aws", size=10, color="FFFFFF", bold=True, check=False)
    if crumbs:
        text(sl, x + 8, y + 22, w - 16, 12, crumbs, size=8.5, color=UI_BLUE, check=False)
    if title:
        text(sl, x + 8, y + 34, w - 16, 18, title, size=12, color=UI_TEXT, bold=True)


def ui_field(sl, x, y, w, label, value, hint=None, kind="input", lw=None):
    text(sl, x, y, w, 12, label, size=8.5, color=UI_LABEL, bold=True, check=False)
    yy = y + 13
    if hint:
        text(sl, x, yy, w, 11, hint, size=7.5, color=UI_MUTED, check=False)
        yy += 11
    if kind == "input":
        box(sl, x, yy, lw or w, 15, fill=UI_CARD, line="7D8998", lw=0.5, radius=2)
        text(sl, x + 5, yy + 2, (lw or w) - 10, 12, value, size=8.5, color=UI_TEXT, check=False)
        return yy + 15
    if kind == "select":
        box(sl, x, yy, lw or w, 15, fill=UI_CARD, line="7D8998", lw=0.5, radius=2)
        text(sl, x + 5, yy + 2, (lw or w) - 20, 12, value, size=8.5, color=UI_TEXT, check=False)
        text(sl, x + (lw or w) - 12, yy + 2, 10, 12, "▾", size=8.5, color=UI_TEXT, check=False)
        return yy + 15
    if kind == "radio":
        xx = x
        for opt, on in value:
            circle(sl, xx, yy + 3, 8, "FFFFFF" if not on else UI_BLUE, line="7D8998", lw=0.5)
            if on:
                circle(sl, xx + 2.5, yy + 5.5, 3, "FFFFFF")
            text(sl, xx + 11, yy + 1, 160, 12, opt, size=8.5, color=UI_TEXT, check=False)
            xx += 11 + len(opt) * 4.6 + 14
        return yy + 14
    if kind == "check":
        yy2 = yy
        for opt, on in value:
            box(sl, x, yy2 + 2, 8, 8, fill=UI_BLUE if on else "FFFFFF", line="7D8998", lw=0.5, radius=1)
            if on:
                text(sl, x + 0.5, yy2 + 0.5, 8, 9, "✓", size=7, color="FFFFFF", bold=True, check=False)
            text(sl, x + 12, yy2 + 0.5, w - 12, 12, opt, size=8.5, color=UI_TEXT, check=False)
            yy2 += 12
        return yy2
    return yy


def ui_button(sl, x, y, w, t, primary=False, size=8.5):
    chip(sl, x, y, w, 16, t, fill=UI_ORANGE if primary else "FFFFFF", color=UI_TEXT, size=size,
         line=None if primary else "7D8998", radius=8)


def table(sl, x, y, w, col_w, rows, header_fill=TAKE_BG, size=9.5, row_h=18, header_color=MINT_L,
          fills=(CARD, "15232A"), font_cols=None, bold_cols=(), colors=None):
    """Tabla nativa editable con bordes finos."""
    nrows = len(rows)
    ncols = len(rows[0])
    gf = sl.shapes.add_table(nrows, ncols, P(x), P(y), P(w), P(row_h * nrows))
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    for a in ("firstRow", "bandRow"):
        tblPr.set(a, "0")
    tw = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = P(w * cw / tw)
    for r in range(nrows):
        tbl.rows[r].height = P(row_h)
        for c in range(ncols):
            cell = tbl.cell(r, c)
            val = rows[r][c]
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(header_fill if r == 0 else fills[r % 2])
            cell.margin_left = cell.margin_right = P(5)
            cell.margin_top = cell.margin_bottom = P(2)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            st = {}
            if isinstance(val, tuple):
                val, st = val
            rr = p.add_run()
            rr.text = val
            rr.font.size = Pt(st.get("size", size))
            fnt = (font_cols or {}).get(c, SANS)
            rr.font.name = st.get("font", fnt)
            rr.font.bold = st.get("bold", r == 0 or c in bold_cols)
            col = header_color if r == 0 else st.get("color", (colors or {}).get(c, TEXT))
            rr.font.color.rgb = rgb(col)
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[st.get("align", "l")]
            tcPr = cell._tc.get_or_add_tcPr()
            for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                ln = etree.SubElement(tcPr, qn(tag))
                ln.set("w", str(int(0.5 * 12700)))
                sf = etree.SubElement(ln, qn("a:solidFill"))
                c_ = etree.SubElement(sf, qn("a:srgbClr"))
                c_.set("val", BORDER)
            # el orden exige que los bordes precedan al relleno
            fill_el = tcPr.find(qn("a:solidFill"))
            if fill_el is not None:
                tcPr.remove(fill_el)
                tcPr.append(fill_el)
    return gf


# ---------------------------------------------------------------- añadidos para S17
TAGS = {
    "esquema": ("ESQUEMA · no es una captura", AMBER, DARK),
    "ilustrativo": ("EJEMPLO ILUSTRATIVO · no es una medición", VIOLET, DARK),
    "doble": ("PERFIL DOBLE · no mide ningún modelo", AMBER, DARK),
    "salida": ("SALIDA REAL DEL PERFIL DOBLE · 17/11/2026", BLUE, DARK),
    "codigo": ("CÓDIGO DE LA DEMO", MINT, DARK),
    "pendiente": ("PERFIL REAL · no ejecutado", CORAL, DARK),
    "real": ("PERFIL REAL · MEDIDO EL 22/11/2026", MINT, DARK),
}


def tag(sl, x, y, kind, w=None, t=None, h=15, size=7.5):
    lab, fill, col = TAGS[kind]
    lab = t or lab
    w = w or (len(lab) * size * 0.66 + 16)
    chip(sl, x, y, w, h, lab, fill=fill, color=col, size=size, radius=3)
    return w


def code_block(sl, x, y, w, lines, size=10, pitch=None, color=TEXT, gutter=0):
    """Código con interlineado exacto para alinear marcadores con cada línea."""
    pitch = pitch or round(size * 1.3, 1)
    text(sl, x + gutter, y, w - gutter, pitch * len(lines) + 6, "\n".join(lines), size=size, font=MONO, color=color,
         bold=True, check=False, lsp=Pt(pitch))
    return pitch


def line_badge(sl, x, y0, pitch, li, n, fill, d=13):
    badge(sl, x, y0 + li * pitch + (pitch - d) / 2, n, fill=fill, d=d, size=7.5)


def shot(sl, name, x, y, w=None, h=None, kind="oficial", caption=None, cap_w=None, pad=4, tag_w=None):
    """Captura o diagrama oficial en un marco claro, con rótulo de procedencia y pie."""
    iw, ih = img_size(name, w=w - 2 * pad if w else None, h=h - 2 * pad if h else None)
    box(sl, x, y, iw + 2 * pad, ih + 2 * pad, fill="FFFFFF", radius=3)
    img(sl, name, x + pad, y + pad, w=iw, h=ih)
    tag(sl, x, y - 17, kind, w=tag_w)
    if caption:
        text(sl, x, y + ih + 2 * pad + 4, cap_w or iw + 2 * pad, 26, caption, size=8.5, color=MUTED)
    return iw + 2 * pad, ih + 2 * pad


def node(sl, x, y, w, h, icon, title, sub=None, fill=CARD, line=None, tsize=11, ssize=9, icon_s=30, tcolor=TITLE):
    """Nodo de arquitectura: icono oficial, nombre y una línea de función."""
    box(sl, x, y, w, h, fill=fill, line=line)
    img(sl, icon, x + 8, y + (h - icon_s) / 2, w=icon_s, h=icon_s)
    tx = x + icon_s + 16
    if sub:
        text(sl, tx, y + h / 2 - tsize * 1.25, w - (tx - x) - 6, tsize * 1.3, title, size=tsize, color=tcolor, bold=True)
        text(sl, tx, y + h / 2 + 1, w - (tx - x) - 6, h / 2 - 3, sub, size=ssize, color=TEXT)
    else:
        text(sl, tx, y, w - (tx - x) - 6, h, title, size=tsize, color=tcolor, bold=True, anchor="m")


def side_note(sl, x, y, w, h, label, body, fill=CARD, accent=MINT, size=10, lsize=8.5):
    """Recuadro con etiqueta en mayúsculas y un párrafo corto."""
    box(sl, x, y, w, h, fill=fill)
    box(sl, x, y, 3.5, h, fill=accent, radius=0)
    text(sl, x + 12, y + 8, w - 20, 12, label.upper(), size=lsize, color=accent, bold=True)
    text(sl, x + 12, y + 24, w - 22, h - 30, body, size=size, color=TEXT)


def bullets(sl, x, y, w, h, items, size=10.5, color=TEXT, mark="•", mark_color=MINT, space=4):
    paras = [{"runs": [(f"{mark}  ", {"color": mark_color, "bold": True})] +
              ([(it, {})] if isinstance(it, str) else it), "space": space} for it in items]
    return text(sl, x, y, w, h, paras, size=size, color=color, space=space)


def console_path(sl, x, y, w, path, label="EN LA CONSOLA", accent=MINT, h=40):
    """Ruta de la consola en una franja compacta."""
    box(sl, x, y, w, h, fill=CARD, line=BORDER)
    img(sl, "aws-console.png", x + 8, y + (h - 20) / 2, w=20, h=20)
    text(sl, x + 36, y + 6, w - 44, 11, label, size=8, color=accent, bold=True)
    text(sl, x + 36, y + 19, w - 44, h - 21, path, size=9.5, font=MONO, color=MINT_L, bold=True)


def timing_note(a, b, extra=""):
    h1, m1 = map(int, a.split(":"))
    h2, m2 = map(int, b.split(":"))
    mins = (h2 * 60 + m2) - (h1 * 60 + m1)
    return f"TIEMPO {a}–{b} ({mins} min{extra})."


# ---------------------------------------------------------------- añadidos para S19
# Estilo «sencillo» del ejemplo (diapositivas de QR, caso, código y práctica): mismas medidas.
NAV_SIMPLE = "Qué medir · Recuperación · Generación · Testing · Producción · Práctica"


def header_s(sl, kicker, title, sub=None):
    text(sl, 42.8, 25.5, 874.5, 18, kicker.upper(), size=9.75, color=MINT, bold=True)
    text(sl, 42.8, 51.8, 874.5, 43.5, title, size=27, color=TITLE, font=SERIF)
    if sub:
        text(sl, 42.8, 100.5, 874.5, 41.2, sub, size=13.5, color=TEXT)


def footer_s(sl):
    text(sl, 42.8, 511.5, 195, 13.5, PIE, size=8.25, color=MUTED, check=False)
    text(sl, 255, 511.5, 622.5, 13.5, NAV_SIMPLE, size=7.5, color=MUTED, check=False)
    text(sl, 900, 511.5, 22.5, 13.5, str(sl._num), size=8.25, color=MUTED, check=False)


def band_s(sl, t):
    box(sl, 42.8, 463.5, 874.5, 25.5, fill=TAKE_BG, line=BORDER, radius=0)
    text(sl, 52.5, 469.5, 855, 18.8, t, size=12.75, color=MINT_L)


def code_panel_s(sl, x, y, w, h, lines, size=16.5, color=MINT_L):
    box(sl, x, y, w, h, fill=CARD, line=BORDER, radius=0)
    text(sl, x + 12.8, y + 12, w - 25.6, h - 21, "\n".join(lines), size=size, font=MONO, color=color, check=False)


def kv_rows_s(sl, y, rows, pitch=48.7, size=15.75, kw=202.5):
    """Filas clave → explicación con separador fino, como las diapositivas 8, 9 y 24 del ejemplo."""
    for k, v in rows:
        text(sl, 49.5, y, kw, pitch - 9, k, size=size, color=MINT, bold=True)
        text(sl, 49.5 + kw + 10.5, y, 847.5 - kw - 10.5, pitch - 9, v, size=size, color=TEXT)
        box(sl, 49.5, y + pitch - 7.4, 847.5, 0.8, fill=BORDER, line=BORDER, radius=0)
        y += pitch
    return y


def table_s(sl, x, y, col_w, rows, row_h=32.25, size=14.25):
    """Tabla del estilo sencillo: cabecera 133A30 con texto menta, filas 18272E / 0F1B22."""
    return table(sl, x, y, sum(col_w), col_w, rows, header_fill=TAKE_BG, size=size, row_h=row_h,
                 header_color=MINT, fills=(BG, CARD))


def term(sl, x, y, w, h, lines, title=None, size=9.5, pitch=None):
    """Panel de terminal: `lines` = str | (str, color). Texto editable en Courier New."""
    box(sl, x, y, w, h, fill="0B1419", line=BORDER, radius=4)
    yy = y + 8
    if title:
        text(sl, x + 10, yy, w - 20, 12, title, size=8, color=FAINT, bold=True, check=False)
        yy += 15
    pitch = pitch or round(size * 1.32, 1)
    paras = []
    for ln in lines:
        t, c = (ln, TEXT) if isinstance(ln, str) else ln
        paras.append([(t if t else " ", {"color": c})])
    text(sl, x + 10, yy, w - 20, pitch * len(lines) + 4, paras, size=size, font=MONO, bold=True, check=False,
         lsp=Pt(pitch))


def bar(sl, x, y, w, h, frac, color=MINT, track="22353D", mark=None, mark_color=AMBER):
    """Barra horizontal nativa (0..1) con marca opcional de umbral."""
    box(sl, x, y, w, h, fill=track, radius=h / 2)
    if frac and frac > 0:
        box(sl, x, y, max(h, w * min(1.0, frac)), h, fill=color, radius=h / 2)
    if mark is not None:
        box(sl, x + w * mark - 1, y - 3, 2, h + 6, fill=mark_color, radius=0)


def tile(sl, name, x, y, s=44):
    return img(sl, name, x, y, w=s, h=s)


def doc_chip(sl, x, y, w, h, label, ok=None, sub=None, size=9.5):
    """Ficha de documento: verde si es relevante, apagada si no."""
    fill, lc, tc = (GREEN_BG, MINT, MINT_L) if ok else (CARD2, BORDER, MUTED) if ok is False else (CARD, BORDER, TITLE)
    box(sl, x, y, w, h, fill=fill, line=lc, radius=5)
    text(sl, x + 4, y + 5, w - 8, 13, label, size=size, color=tc, bold=True, align="c", font=MONO, check=False)
    if sub:
        text(sl, x + 4, y + h - 16, w - 8, 12, sub, size=8, color=tc, align="c", check=False)


def cover(deck, kicker, title, desc, panel):
    """Portada con las medidas de la portada del ejemplo. `panel(sl)` dibuja el recuadro derecho."""
    sl = deck.slide(BG_SECTION, tag="portada")
    img(sl, "thepower-logo.png", 38, 34, h=32)
    text(sl, 43, 104, 420, 14, kicker, size=10, color=MINT, bold=True)
    text(sl, 43, 124, 450, 92, title, size=36, font=SERIF, color=TITLE, check=False)
    text(sl, 43, 226, 425, 78, desc, size=12.5, color=TEXT)
    text(sl, 43, 322, 420, 16, "José Antonio Nuevo", size=12.5, color=TITLE, bold=True)
    box(sl, 497, 52, 420, 410, fill=BG, line="2A5246", radius=8)
    panel(sl)
    return sl


def closing(deck, ideas, preguntas, proxima, materiales):
    """Cierre con las medidas de la última diapositiva del ejemplo."""
    sl = deck.slide(BG_SECTION, tag="cierre")
    img(sl, "thepower-logo.png", 38, 34, h=30)
    text(sl, 43, 84, 300, 14, "CIERRE", size=10, color=MINT, bold=True)
    text(sl, 43, 102, 520, 44, "Lo que nos llevamos", size=32, font=SERIF, color=TITLE)
    y = 158
    for i, idea in enumerate(ideas, 1):
        circle(sl, 43, y, 22, MINT_L)
        text(sl, 43, y + 3, 22, 16, str(i), size=10.5, color=DARK, bold=True, align="c", check=False)
        text(sl, 76, y + 1, 470, 44, idea, size=12, color=TITLE)
        y += 50
    box(sl, 584, 130, 333, 336, fill="1A463C", radius=8)
    text(sl, 604, 146, 300, 40, "¿Preguntas?", size=30, font=SERIF, color=MINT_L)
    text(sl, 604, 198, 300, 12, "PARA COMPROBAR", size=9, color=MINT, bold=True)
    bullets(sl, 604, 216, 300, 96, preguntas, size=10.5, color=TITLE)
    text(sl, 604, 322, 300, 12, proxima[0], size=9, color=MINT, bold=True)
    text(sl, 604, 338, 300, 40, proxima[1], size=10.5, color=TITLE)
    text(sl, 604, 388, 300, 12, materiales[0], size=9, color=MINT, bold=True)
    text(sl, 604, 404, 300, 56, materiales[1], size=10.5, color=TITLE)
    return sl
