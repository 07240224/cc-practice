import json,sys,math
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/地图规划/全校布局规划.json');d=json.loads(p.read_text());B={b['id']:b for b in d['buildings']};R={r['id']:r for r in d['roads']}
B['W06']['polygon']=[[589,722],[706,678],[718,752],[614,788]]
a=math.radians(-25);B['D10']['polygon']=[[round(1104+u*math.cos(a)-v*math.sin(a),1),round(953+u*math.sin(a)+v*math.cos(a),1)] for u,v in [(-22.5,-12),(22.5,-12),(22.5,12),(-22.5,12)]]
R['W4']['points']=[[690,480],[693,489],[710,543],[736,619],[770,696],[791,716]]
R['W7']['width']=5
R['G1']['points']=[[936,363],[1095,408],[1210,491],[1230,489],[1518,489]]
R['G4']['points']=[[1390,286],[1386,402],[1367,425],[1351,480]]
R['G5']['points']=[[1572,285],[1572,396],[1600,467],[1605,477],[1605,541],[1598,550],[1597,608],[1767,616]]
R['D3']['points']=[[780,890],[864,923],[959,909],[984,892],[986,861],[1025,850],[1131,820],[1177,800]]
R['D4']['points']=[[959,909],[1009,949],[1030,950],[1080,975],[1126,982],[1202,1008]]
R['D5']['points']=[[1126,982],[1213,956]]
d['connections'][0]['points']=[[771,724],[794,716],[811,711]]
d['connections'][1]['points']=[[936,363],[909,447],[935,476],[994,466],[1025,490],[1049,555],[1081,611],[1112,687],[1158,779]]
# Boundary corner adjustments keep the actual southern projections within their parcels.
g=d['campuses'][1]['polygon'];g[g.index([1501,602])]=[1501,608];g[g.index([1440,602])]=[1436,608];g[g.index([1440,644])]=[1436,645];g[g.index([1364,644])]=[1340,645]
d['campuses'][2]['polygon'][7]=[1290,862]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ROAD INTERSECTIONS')
for r in d['roads']+[{**c,'width':6} for c in d['connections']]:
 line=LineString(r['points']).buffer(r['width']/2)
 hits=[(b['id'],round(line.intersection(Polygon(b['polygon'])).area,2)) for b in d['buildings'] if line.intersection(Polygon(b['polygon'])).area>.01]
 if hits:print(r['id'],hits)
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);print('OUTSIDE')
for b in d['buildings']:
 q=Polygon(b['polygon']);ratio=q.difference(site).area/q.area
 if ratio>.005:print(b['id'],round(ratio,3))
print('EXCLUSION')
ex=unary_union([Polygon(c['polygon']) for c in d['exclusions']])
for r in [r for r in d['roads'] if r['kind']=='internal']+[{**c,'width':6} for c in d['connections']]:
 if LineString(r['points']).buffer(r['width']/2).intersection(ex).area>1:print(r['id'],round(LineString(r['points']).buffer(r['width']/2).intersection(ex).area))
