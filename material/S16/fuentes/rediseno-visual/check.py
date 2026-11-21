import os, sys, hashlib
from pptx import Presentation
from pptx.util import Emu
p = Presentation(sys.argv[1])
W, H = p.slide_width, p.slide_height
qr = hashlib.sha256(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'qr-ai-engineer.jpg'),'rb').read()).hexdigest()
logo = hashlib.sha256(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'thepower-logo.png'),'rb').read()).hexdigest()
print('slides', len(p.slides), 'size', W, H)
qr_found = 0; logo_found = 0; issues = 0; words = 0
for i, s in enumerate(p.slides, 1):
    n = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
    if len(n) < 200: print('short notes', i, len(n)); issues += 1
    if 'TIEMPO' not in n and 'CONSULTA' not in n: print('no timing', i); issues += 1
    if 'FUENTES' not in n and 'IMÁGENES' not in n and 'CONSULTA' not in n: print('no sources', i); issues += 1
    for sh in s.shapes:
        if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W + 12700 or sh.top + sh.height > H + 12700:
            print('out of bounds', i, sh.name, sh.left/12700, sh.top/12700, (sh.left+sh.width)/12700, (sh.top+sh.height)/12700); issues += 1
        if sh.shape_type == 13:
            h = hashlib.sha256(sh.image.blob).hexdigest()
            if h == qr: qr_found += 1
            if h == logo: logo_found += 1
        if sh.has_text_frame:
            words += len(sh.text_frame.text.split())
print('QR identical images:', qr_found, '| thePower logo identical:', logo_found, '| visible words:', words, '| issues:', issues)
