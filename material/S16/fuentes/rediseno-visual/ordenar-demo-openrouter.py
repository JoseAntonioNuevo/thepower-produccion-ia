import sys
from pathlib import Path
import zipfile,xml.etree.ElementTree as E
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
src=Path(sys.argv[1]);dst=Path(sys.argv[2])
with zipfile.ZipFile(src) as zin:
 data={n:zin.read(n) for n in zin.namelist()}
root=E.fromstring(data['ppt/presentation.xml']);lst=root.find('{'+P+'}sldIdLst');slides=list(lst)
assert len(slides)==33
order=list(range(23))+list(range(27,33))+list(range(23,27))
lst[:]=[slides[i] for i in order]
data['ppt/presentation.xml']=E.tostring(root,encoding='utf-8',xml_declaration=True)
rels={e.attrib['Id']:e.attrib['Target'] for e in E.fromstring(data['ppt/_rels/presentation.xml.rels'])}
for no,item in enumerate(lst,1):
 target=rels[item.attrib['{'+R+'}id']];path='ppt/'+target.lstrip('/') if not target.startswith('/ppt/') else target.lstrip('/')
 if path not in data:
  path='ppt/'+target
 x=E.fromstring(data[path])
 for sh in x.findall('.//{'+P+'}sp'):
  ts=sh.findall('.//{'+A+'}t');text=''.join(t.text or '' for t in ts)
  off=sh.find('.//{'+A+'}off')
  if text.isdigit() and len(text)<=2 and off is not None and int(off.get('y','0'))>=6400000:
   ts[0].text=str(no)
  if text=='0' and off is not None and int(off.get('y','0'))>=6400000:ts[0].text=str(no)
 for t in x.findall('.//{'+A+'}t'):
  if t.text and 'request_id' in t.text:
   t.text=t.text.replace('Retención, streams, request_id','Retención, streams, arranque')
 data[path]=E.tostring(x,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as zout:
 for n,b in data.items():zout.writestr(n,b)
print('Orden final: 23 conceptos + 6 demo + práctica, cierre y 2 consultas.')
