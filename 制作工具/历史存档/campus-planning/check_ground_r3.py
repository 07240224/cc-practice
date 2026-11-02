import json,sys
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/地图规划/地面底图R3/地面底图数据.json');d=json.loads(p.read_text());B={b['id']:unary_union([Polygon(b['polygon'],b.get('holes'))]+[Polygon(a['polygon'],a.get('holes')) for a in b.get('additionalFootprints',[])]) for b in d['buildings']};roads=d['roads']+[{**r,'kind':'connection'} for r in d['connections']]
report={'invalid':[],'roadBuildingIntersections':[],'roadExclusions':[],'roadWaterSport':[],'buildingOverlaps':[],'outsideSite':[]}
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);ex=unary_union([Polygon(x['polygon']) for x in d['exclusions']]);obs=[s for s in d['spaces'] if s['kind'] in ['water','sport','track']]
for id,g in B.items():
 if not g.is_valid:report['invalid'].append(id)
 if g.difference(site).area>.5:report['outsideSite'].append([id,round(g.difference(site).area,2)])
for r in roads:
 g=LineString(r['points']).buffer(r['width']/2)
 for id,b in B.items():
  a=g.intersection(b).area
  if a>.01:report['roadBuildingIntersections'].append([r['id'],id,round(a,2)])
 if g.intersection(ex).area>.1:report['roadExclusions'].append([r['id'],round(g.intersection(ex).area,2)])
 for s in obs:
  a=g.intersection(Polygon(s['polygon'])).area
  if a>.01:report['roadWaterSport'].append([r['id'],s['id'],round(a,2)])
for i,b in enumerate(d['buildings']):
 for c in d['buildings'][i+1:]:
  a=B[b['id']].intersection(B[c['id']]).area
  if a>1 and not (b.get('connectedGroup') and b.get('connectedGroup')==c.get('connectedGroup')):report['buildingOverlaps'].append([b['id'],c['id'],round(a,2)])
for z in ['W','G','D']:
 rs=[r for r in d['roads'] if r['id'].startswith(z) and r['kind']=='internal']+[r for r in d['connections'] if (z=='W' and r['id']=='C01') or (z in ['G','D'] and r['id']=='C02')];surface=unary_union([LineString(r['points']).buffer(r['width']/2) for r in rs]);report[z+'RoadComponents']=len(surface.geoms) if surface.geom_type=='MultiPolygon' else 1
print(json.dumps(report,ensure_ascii=False,indent=2));(p.parent/'几何检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
