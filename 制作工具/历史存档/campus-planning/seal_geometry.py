import json,sys,math
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/地图规划/全校布局规划.json');d=json.loads(p.read_text());B={b['id']:b for b in d['buildings']};R={r['id']:r for r in d['roads']}
def rect(id,x,y,w,h,a):
 a=math.radians(a);B[id]['polygon']=[[round(x+u*math.cos(a)-v*math.sin(a),2),round(y+u*math.sin(a)+v*math.cos(a),2)] for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
rect('D15',1127,1005,174,14,21);rect('D10',1104,953,45,22,-25)
R['G5']['points'][2]=[1599,467]
R['W5']['points'][-1]=[790,720]
d['connections'][1]['points'][2]=[935,468]
g=d['campuses'][1]['polygon'];i=g.index([1511,598]);j=g.index([1436,608]);g[i:j+1]=[[1520,600],[1520,608],[1446,608]];g[g.index([1436,645])]=[1446,645]
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);ex=unary_union([Polygon(c['polygon']) for c in d['exclusions']])
for id in ['W18','G18']:
 q=Polygon(B[id]['polygon']).intersection(site);assert q.geom_type=='Polygon';B[id]['polygon']=[[round(x,3),round(y,3)] for x,y in list(q.exterior.coords)[:-1]]
report={'roadBuildingIntersections':[],'excludedIntrusions':[],'outOfSite':[],'buildingOverlaps':[]}
for r in d['roads']+[{**c,'width':6} for c in d['connections']]:
 l=LineString(r['points']).buffer(r['width']/2)
 for b in d['buildings']:
  a=l.intersection(Polygon(b['polygon'])).area
  if a>.001:report['roadBuildingIntersections'].append([r['id'],b['id'],round(a,4)])
 if r.get('kind')!='external' and l.intersection(ex).area>.001:report['excludedIntrusions'].append([r['id'],round(l.intersection(ex).area,3)])
for b in d['buildings']:
 a=Polygon(b['polygon']).difference(site).area
 if a>.1:report['outOfSite'].append([b['id'],round(a,3)])
for i,b in enumerate(d['buildings']):
 for c in d['buildings'][i+1:]:
  a=Polygon(b['polygon']).intersection(Polygon(c['polygon'])).area
  if a>1:report['buildingOverlaps'].append([b['id'],c['id'],round(a)])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));(p.parent/'布局几何检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
