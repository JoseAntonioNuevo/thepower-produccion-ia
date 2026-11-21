"""Versión reducida para clase: conceptos en diapositivas y detalle en la consola en vivo.

Construye primero la versión completa en memoria para leer las notas de las diapositivas
que se quitan; esas notas pasan, como ampliación, a la diapositiva que las sustituye en clase.
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

FULL = p1.PART1 + p2.PART2 + p3.PART3 + p4.PART4 + p5.PART5

# (función, inicio, fin, funciones retiradas cuyo contenido pasa a las notas)
CLASE = [
    (p1.s01_portada, "18:30", "18:31", []),
    (p1.s02_encuesta, "18:31", "18:33", [p1.s05_metodo]),
    (p1.s03_caso, "18:33", "18:35", []),
    (p1.s04_mapa, "18:35", "18:37", []),
    (p1.s08_consola, "18:37", "18:41", [p1.s09_arn]),
    (p1.s10_regiones, "18:41", "18:44", []),
    (p1.s11_responsabilidad, "18:44", "18:46", []),
    (p1.s12_iam, "18:46", "18:52", [p1.s13_privilegio]),
    (p2.s15_ec2, "18:52", "18:58", [p2.s16_launch, p2.s17_ebs]),
    (p2.s18_s3, "18:58", "19:04", [p2.s19_bucket, p2.s20_almacen]),
    (p2.s22_vpc, "19:04", "19:08", []),
    (p2.s24_recorrido, "19:08", "19:14", [p2.s23_sg]),
    (p3.s26_docker, "19:14", "19:17", [p3.s27_dockerfile]),
    (p3.s28_ecr, "19:17", "19:20", []),
    (p3.s29_ecs, "19:20", "19:25", [p3.s30_taskdef, p3.s33_cadena]),
    (p3.s31_roles, "19:25", "19:28", []),
    (p3.s32_secrets, "19:28", "19:32", []),
    (p4.s35_cloudwatch, "19:32", "19:36", [p4.s36_diagnostico]),
    (p4.s37_billing, "19:36", "19:39", []),
    (p4.s38_mes, "19:39", "19:41", []),
    (p4.s39_demo, "19:41", "19:45", [p4.s40_calculadora, p4.s41_optimizar]),
    (p5.s43_alojar, "19:45", "19:49", [p5.s44_bedrock]),
    (p5.s45_nubes, "19:49", "19:52", [p1.s07_proveedores]),
    (p5.s46_practica, "19:52", "19:54", []),
    (p5.s47_cierre, "19:54", "20:00", []),
    (p5.s48_ruta, None, None, [p5.s50_comandos, p5.s51_fuentes]),
    (p5.s49_costes, None, None, []),
]


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


def main(out):
    d = Deck()
    d.prs.core_properties.title = "S16 · Cloud deployment: AWS basics"
    d.prs.core_properties.author = "José Antonio Nuevo"
    d.prs.core_properties.subject = "thePower · AI Engineer · S16 · 12 y 18 de noviembre de 2026"
    for fn, a, b, extra in CLASE:
        sl = fn(d)
        tf = sl.notes_slide.notes_text_frame
        t = tf.text
        if a:
            t = re.sub(r"^TIEMPO[^\n]*", f"TIEMPO {a}–{b} ({minutes(a, b)} min, incluido el recorrido en vivo por la consola).", t)
        for e in extra:
            t += f"\n\nAMPLIACIÓN PARA EL RECORRIDO EN VIVO (contenido de la diapositiva «{e.__name__.split('_', 1)[1]}» de la versión completa):\n" + notes_of(e)
        tf.text = t
    d.save(out)
    print("slides", d.n)
    for w in WARNINGS:
        print("WARN", w)


if __name__ == "__main__":
    main(sys.argv[1])
