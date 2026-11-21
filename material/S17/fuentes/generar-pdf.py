"""Maquetación reproducible de guion y guía con ReportLab; no requiere servicios externos."""

import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    HRFlowable,
    KeepTogether,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def inline(text):
    """Conservar texto y énfasis; las rutas del repositorio se leen desde el Markdown original."""
    text = text.replace("–", "-").replace("—", "-").replace("‑", "-")
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", lambda m: m[1], text)
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`([^`]+)`", r'<font name="CursoMono" size="9">\1</font>', text)


def build(source, output):
    """Convierte un subconjunto pequeño de Markdown, con tablas que parten por filas."""
    fonts = Path("/System/Library/Fonts/Supplemental")
    for name, filename in (
        ("Curso", "Arial.ttf"),
        ("CursoBold", "Arial Bold.ttf"),
        ("CursoMono", "Courier New.ttf"),
        ("CursoCodeMono", "Courier New Bold.ttf"),
    ):
        pdfmetrics.registerFont(TTFont(name, str(fonts / filename)))
    pdfmetrics.registerFontFamily("Curso", normal="Curso", bold="CursoBold", italic="Curso")
    body = ParagraphStyle(
        "CursoBody",
        fontName="Curso",
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor("#17303d"),
        spaceAfter=8,
    )
    h1 = ParagraphStyle(
        "CursoH1", parent=body, fontName="CursoBold", fontSize=25, leading=30, spaceAfter=18
    )
    h2 = ParagraphStyle(
        "CursoH2",
        parent=body,
        fontName="CursoBold",
        fontSize=15,
        leading=20,
        spaceBefore=15,
        spaceAfter=9,
        keepWithNext=True,
    )
    code = ParagraphStyle(
        "CursoCode",
        fontName="CursoCodeMono",
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#17303d"),
        backColor=colors.HexColor("#edf4f5"),
        borderPadding=9,
        spaceAfter=12,
    )
    cell = ParagraphStyle("CursoCell", parent=body, fontSize=9.2, leading=12.5, spaceAfter=0)
    lines = source.read_text().splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            story.append(KeepTogether([Spacer(1, 4), Preformatted("\n".join(block), code)]))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", x) for x in raw):
                    rows.append([Paragraph(inline(x), cell) for x in raw])
                i += 1
            count = len(rows[0])
            widths = [180, 335] if count == 2 else [515 / count] * count
            tab = Table(rows, colWidths=widths, repeatRows=1, hAlign=TA_LEFT)
            tab.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d8efeb")),
                        (
                            "ROWBACKGROUNDS",
                            (0, 1),
                            (-1, -1),
                            [colors.white, colors.HexColor("#f3f7f8")],
                        ),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#6aa99b")),
                    ]
                )
            )
            story.extend([tab, Spacer(1, 10)])
            continue
        elif line.startswith("# "):
            story.extend(
                [
                    Paragraph(inline(line[2:]), h1),
                    HRFlowable(width="100%", thickness=2, color=colors.HexColor("#139c80")),
                    Spacer(1, 14),
                ]
            )
        elif line.startswith("## "):
            story.append(CondPageBreak(100))
            story.append(Paragraph(inline(line[3:]), h2))
        elif line.startswith("- "):
            story.append(Paragraph("• " + inline(line[2:]), body))
        else:
            paragraph = [line]
            while (
                i + 1 < len(lines)
                and lines[i + 1].strip()
                and not lines[i + 1].startswith(("#", "|", "```", "- "))
            ):
                i += 1
                paragraph.append(lines[i])
            story.append(Paragraph(inline(" ".join(paragraph)), body))
        i += 1

    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Curso", 8)
        canvas.setFillColor(colors.HexColor("#56717d"))
        canvas.drawString(40, 23, "thePower · AI Engineer · S17 · 17 / 23 noviembre 2026")
        canvas.drawRightString(A4[0] - 40, 23, str(doc.page))
        canvas.restoreState()

    SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=38,
        bottomMargin=40,
        title=source.stem,
        author="José Antonio Nuevo",
    ).build(story, onFirstPage=page, onLaterPages=page)
    print(output)


if __name__ == "__main__":
    root = Path(sys.argv[1])
    for name in ("guion-profesor", "guia-alumno"):
        build(root / f"material/S17/{name}.md", root / f"material/S17/{name}.pdf")
