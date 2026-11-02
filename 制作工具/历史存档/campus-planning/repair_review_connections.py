from pathlib import Path
import json,sys
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/占地复核图/轮廓与道路.json');d=json.loads(p.read_text())
links=[{'name':'十九号楼西侧开口连接主路','points':[[917,422],[942,422],[948,421]],'width':4}, {'name':'湖侧纵路连续连接','points':[[1374,425],[1365,442],[1355,470]],'width':4}]
# Cross under the right-hand elevated link, rather than walking along its roof.
d['passages']=[x for x in d['passages'] if x['name']!='一教二教连廊下通路']
ped={'name':'一教二教连廊下地面通路','points':[[1682,430],[1720,430]],'width':4,'upperStructure':'C113','type':'架空连接下方的东西通行'};d['passages'].append(ped)
road=unary_union([Polygon(s['outer'],s['holes']) for s in d['roadSurfaces']]+[LineString(x['points']).buffer(x['width']/2) for x in links+[ped]])
def parts(g):
 if g.geom_type=='Polygon':return[{'outer':[list(x) for x in list(g.exterior.coords)[:-1]],'holes':[[list(x) for x in list(h.coords)[:-1]] for h in g.interiors]}]
 return[s for q in g.geoms for s in parts(q)]
for s in d['buildings']:
 if s['id']=='C113':
  q=Polygon(s['outer'],s['holes']);u=LineString(ped['points']).buffer(ped['width']/2);s['referenceOutline']={'outer':s['outer'],'holes':s['holes']};s['groundParts']=parts(q.difference(u));s['upperParts']=parts(q.intersection(u));s['note']='保留上层连廊，地面通路贯通'
d['roadSurfaces']=parts(road);d['connectivityRepairs']=links+[ped]
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('repaired nineteen entrance, lake-side narrow joint, classroom underpass')
