from pathlib import Path
import json,sys,math
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/占地复核图/轮廓与道路.json');d=json.loads(p.read_text());base=json.loads(Path('/workspace/cc-practice/地图规划/地面底图R3/地面底图数据.json').read_text())
def makepoly(s):return Polygon(s['outer'],s.get('holes',[])).buffer(0)
def clean(poly,r=1.1):
 q=poly.buffer(r,join_style=2).buffer(-r,join_style=2).simplify(1.1,preserve_topology=True)
 return q if not q.is_empty else poly
out=[]
for s in d['buildings']:
 poly=makepoly(s)
 if poly.geom_type!='Polygon':continue
 rect=poly.minimum_rotated_rectangle;v=list(rect.exterior.coords);edges=[math.dist(v[i],v[i+1]) for i in range(4)];short=min(edges);long=max(edges)
 if (short<1.8 or long/max(short,.01)>38 or poly.area/max(rect.area,1)<.12 or poly.area<20) and not s['id'].startswith('SPECIAL'):continue
 poly=clean(poly,1.25)
 if poly.geom_type!='Polygon':poly=max(poly.geoms,key=lambda p:p.area)
 s['outer']=[list(x) for x in list(poly.exterior.coords)[:-1]];s['holes']=[[list(x) for x in list(h.coords)[:-1]] for h in poly.interiors];out.append(s)
d['buildings']=out
# Keep the courtyard/road topology while removing tree-crown notches on the road edges.
road=unary_union([makepoly(r) for r in d['roadSurfaces']]);road=road.buffer(1.6,quad_segs=8).buffer(-1.6,quad_segs=8).simplify(.8,preserve_topology=True)
# All retained connecting passages must remain part of the road layer.
for x in d['passages']:road=road.union(LineString(x['points']).buffer(x['width']/2))
# Difference only the physical above-ground source components; underpasses are represented separately.
blocks=unary_union([makepoly(s) for s in out]);road=road.difference(blocks)
def parts(g):
 if g.is_empty:return[]
 if g.geom_type=='Polygon':return[{'outer':[list(x) for x in list(g.exterior.coords)[:-1]],'holes':[[list(x) for x in list(h.coords)[:-1]] for h in g.interiors]}]
 return [a for p in g.geoms for a in parts(p)]
d['roadSurfaces']=parts(road);d['exclusions']=base['exclusions']
# Independent name anchors retain every original named footprint, even when sharing a continuous body.
anchors=[]
for b in base['buildings']:
 poly=Polygon(b['polygon']);pt=poly.centroid;name=b['name']
 if b['id']=='G50':name='菜鸟驿站 · 快递中心'
 if b['id']=='D03':name='运动场西侧院楼'
 anchors.append({'id':b['id'],'name':name,'x':pt.x,'y':pt.y})
# Known labels with shared geometry use their own visual anchors.
adjust={'G03':(1035,307),'G04':(981,326),'G05':(1028,338),'G06':(1058,360),'G29':(1313,466),'G30':(1287,505),'G31':(1334,535),'G32':(1395,505),'G33':(1424,540),'G37':(1590,515),'G46':(1130,615),'G48':(1175,700),'D10':(1098,955),'D09':(1165,938),'D08':(1190,879),'W20':(592,617)}
for a in anchors:
 if a['id'] in adjust:a['x'],a['y']=adjust[a['id']]
d['nameAnchors']=anchors
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('clean components',len(out),'anchors',len(anchors),'roads',len(d['roadSurfaces']))
