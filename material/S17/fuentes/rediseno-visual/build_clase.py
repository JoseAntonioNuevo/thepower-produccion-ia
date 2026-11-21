"""Versión reducida para clase: conceptos en diapositivas y detalle en la consola en vivo.

La versión completa (build.py, 49 diapositivas) queda como consulta regenerable. Aquí cada bloque
conserva solo las diapositivas que explican conceptos; las pantallas que se enseñan en vivo
(ficha del modelo, playground, página de la función, formularios, rutas e integraciones,
CloudWatch) pasan, con sus notas completas, a las notas de la diapositiva que las sustituye.
Los separadores de bloque se retiran: el bloque activo sigue indicado en el pie de cada diapositiva.

Uso: python build_clase.py SALIDA.pptx
"""
import re
import sys

sys.path.insert(0, ".")
from deck_lib import WARNINGS, Deck  # noqa: E402
import deck_part1 as p1  # noqa: E402
import deck_part2 as p2  # noqa: E402
import deck_part3 as p3  # noqa: E402
import deck_part4 as p4  # noqa: E402
import deck_part5 as p5  # noqa: E402
import deck_part6 as p6  # noqa: E402

# (función, inicio, fin, funciones retiradas cuyo contenido pasa a las notas)
CLASE = [
    (p1.s01_portada, "18:30", "18:31", []),
    (p1.s02_encuesta, "18:31", "18:33", []),
    (p1.s03_caso, "18:33", "18:35", []),
    # 1 · Serverless (sin consola)
    (p1.s05_comparacion, "18:35", "18:39", [p1.s07_ciclo]),
    (p1.s06_responsabilidades, "18:39", "18:42", []),
    (p1.s08_mapa, "18:42", "18:45", []),
    # 2 · Bedrock: conceptos y después la consola
    (p2.s10_bedrock, "18:45", "18:48", []),
    (p2.s11_ids, "18:48", "18:54", [p2.s12_ficha, p2.s14_playground]),
    (p2.s13_regiones, "18:54", "19:00", []),
    # 3 · Lambda y API Gateway
    (p3.s18_handler, "19:00", "19:09", [p3.s17_lambda_consola, p3.s19_config, p3.s21_operar, p2.s15_estructura]),
    (p3.s22_apigw, "19:09", "19:16", [p3.s23_rutas, p3.s23b_integracion]),
    (p3.s24_autorizar, "19:16", "19:20", []),
    # 4 · IAM y CloudWatch
    (p4.s26_permisos, "19:20", "19:25", [p3.s20_permisos, p6.s46_politica]),
    (p4.s27_sigv4, "19:25", "19:30", [p4.s28_cloudwatch, p4.s29_diagnostico]),
    # 5 · Latencia y límites
    (p4.s31_frio, "19:30", "19:33", []),
    (p4.s32_relojes, "19:33", "19:35", []),
    (p4.s33_timeouts, "19:35", "19:38", []),
    (p4.s34_concurrencia, "19:38", "19:40", []),
    # 6 · Costes y alternativas
    (p5.s37_coste, "19:40", "19:44", []),
    (p5.s39_alternativas, "19:44", "19:47", []),
    (p5.s40_elegir, "19:47", "19:50", []),
    # 7 · Práctica y cierre
    (p6.s43_practica, "19:50", "19:53", [p6.s42_evidencias]),
    (p6.s44_cierre, "19:53", "20:00", []),
    # Consulta
    (p6.s45_ruta, None, None, [p6.s47_empaquetado, p6.s48_fuentes]),
    (p4.s35_limites, None, None, []),
    (p5.s38_calculo, None, None, []),
]

# Diapositivas tras las que se abre la consola en vivo (el tiempo indicado lo incluye).
LIVE = {p2.s10_bedrock, p2.s11_ids, p2.s13_regiones, p3.s18_handler, p3.s22_apigw, p3.s24_autorizar,
        p4.s26_permisos, p4.s27_sigv4}

# Sin separadores: la primera diapositiva de cada bloque recuerda el bloque en sus notas.
BLOCK_START = {
    p1.s05_comparacion: "BLOQUE 1 de 7 · Serverless (18:35–18:45). Tres diapositivas de conceptos, sin consola.",
    p2.s10_bedrock: "BLOQUE 2 de 7 · Bedrock (18:45–19:00). Tres diapositivas de conceptos; después, catálogo, ficha, "
                    "Cross-Region inference y playground en la consola, sin pulsar Run.",
    p3.s18_handler: "BLOQUE 3 de 7 · Lambda y API Gateway (19:00–19:20). Cada diapositiva introduce una pieza y se abre su consola: "
                    "función (Code, Configuration, Monitor, Aliases), después API Gateway (Routes, Integrations, Stages).",
    p4.s26_permisos: "BLOQUE 4 de 7 · IAM y CloudWatch (19:20–19:30). IAM › Roles en vivo tras la primera; CloudWatch Logs tras la segunda.",
    p4.s31_frio: "BLOQUE 5 de 7 · Latencia y límites (19:30–19:40). Cuatro infografías, sin consola salvo un REPORT si existe.",
    p5.s37_coste: "BLOQUE 6 de 7 · Costes y alternativas (19:40–19:50). Sin consola; el cálculo detallado queda en consulta.",
    p6.s43_practica: "BLOQUE 7 de 7 · Práctica y cierre (19:50–20:00).",
}

# Referencias que cambian de sentido al mover notas entre diapositivas.
REPLACE = {
    "el detalle está en el anexo.": "el extracto de la política está en la ampliación de estas notas.",
    "La política detallada está en el anexo de consulta.": "La política detallada está más abajo, en estas notas.",
    "Empaquetado y publicación del ZIP, en el anexo.": "Empaquetado y publicación del ZIP: notas de la consulta «recorrido por la consola».",
    "que veremos en la diapositiva siguiente.": "que se ve en Integrations a continuación.",
    "la captura de log streams de la diapositiva anterior.": "la captura oficial de log streams de la Lambda Developer Guide.",
}


def minutes(a, b):
    h1, m1 = map(int, a.split(":"))
    h2, m2 = map(int, b.split(":"))
    return (h2 * 60 + m2) - (h1 * 60 + m1)


def notes_of(fn):
    """Notas que genera una diapositiva, sin su línea de tiempo."""
    d = Deck()
    sl = fn(d)
    t = sl.notes_slide.notes_text_frame.text
    return re.sub(r"^TIEMPO[^\n]*\n?", "", t).strip()


def mark_consulta(sl):
    """Las diapositivas de clase que pasan a consulta se rotulan como tal en su antetítulo."""
    for sh in sl.shapes:
        if sh.has_text_frame and sh.top < 12700 * 40 and sh.text_frame.text.isupper() and sh.text_frame.text.strip():
            r = sh.text_frame.paragraphs[0].runs[0]
            if not r.text.startswith("CONSULTA"):
                r.text = "CONSULTA · " + r.text
            return


def main(out):
    d = Deck()
    d.prs.core_properties.title = "S17 · Serverless AI: AWS Bedrock y Lambda"
    d.prs.core_properties.author = "José Antonio Nuevo"
    d.prs.core_properties.subject = "thePower · AI Engineer · S17 · 17 y 23 de noviembre de 2026"
    for fn, a, b, extra in CLASE:
        sl = fn(d)
        tf = sl.notes_slide.notes_text_frame
        t = tf.text
        if a:
            suffix = ", incluido el recorrido en vivo por la consola" if fn in LIVE else ""
            t = re.sub(r"^TIEMPO[^\n]*", f"TIEMPO {a}–{b} ({minutes(a, b)} min{suffix}).", t)
            if fn in BLOCK_START:
                t = BLOCK_START[fn] + "\n" + t
        elif t.startswith("TIEMPO"):
            t = re.sub(r"^TIEMPO[^\n]*", "CONSULTA (no se proyecta en el directo salvo que se pida).", t)
            mark_consulta(sl)
        for e in extra:
            t += (f"\n\nAMPLIACIÓN PARA EL RECORRIDO EN VIVO (contenido de la diapositiva «{e.__name__.split('_', 1)[1]}» "
                  "de la versión completa):\n" + notes_of(e))
        for k, v in REPLACE.items():
            t = t.replace(k, v)
        tf.text = t
    d.save(out)
    print("slides", d.n)
    for w in WARNINGS:
        print("WARN", w)


if __name__ == "__main__":
    main(sys.argv[1])
