import sys, importlib
sys.path.insert(0, '.')
import deck_lib
from deck_lib import Deck, WARNINGS
parts = []
for m in sys.argv[2:]:
    mod = importlib.import_module(m)
    parts += [v for k, v in vars(mod).items() if k.startswith('PART')][0]
d = Deck()
d.prs.core_properties.title = 'S16 · Cloud deployment: AWS basics'
d.prs.core_properties.author = 'José Antonio Nuevo'
d.prs.core_properties.subject = 'thePower · AI Engineer · S16 · 12 y 18 de noviembre de 2026'
for f in parts:
    f(d)
d.save(sys.argv[1])
print('slides', d.n)
for w in WARNINGS: print('WARN', w)
