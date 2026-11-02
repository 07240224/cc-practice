import json,sys,math
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/地图规划/全校布局规划.json');d=json.loads(p.read_text());B={b['id']:b for b in d['buildings']};R={r['id']:r for r in d['roads']}
def rect(id,x,y,w,h,a):
 a=math.radians(a);B[id]['polygon']=[[round(x+u*math.cos(a)-v*math.sin(a),2),round(y+u*math.sin(a)+v*math.cos(a),2)] for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
rect('W02',405,542,72,32,-23);rect('G12',1067,481,40,20,-25);rect('D06',1068,887,78,32,-25);rect('D05',1011,878,28,26,-25)
R['W3']['points']=[[503,435],[533,473],[540,513],[542,560],[570,615],[598,678],[609,699]]
R['D2']['points']=[[1085,611],[1121,687],[1166,779],[1189,819],[1218,880],[1228,961],[1208,1015]]
R['D3']['points']=R['D3']['points'][:6]
c=d['connections'][1];c['points']=[[936,363],[909,447],[935,469],[994,467],[1025,490],[1049,555],[1085,611],[1121,687],[1166,779]]
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);ex=unary_union([Polygon(c['polygon']) for c in d['exclusions']])
for b in d['buildings']:
 q=Polygon(b['polygon']);cl=q.intersection(site)
 if q.difference(site).area>.0001:
  assert cl.geom_type=='Polygon' and cl.area/q.area>.98,(b['id'],cl.area/q.area)
  b['polygon']=[[x,y] for x,y in list(cl.exterior.coords)[:-1]]
groups=[('体育馆及附属体块',['W07','W20']),('第十一宿舍组',['G03','G04']),('第九十宿舍组',['G05','G06']),('育衡与档案组',['G37','G38']),('科研实验楼组',['G43','G44']),('三教与信息管理组',['D09','D10'])]
for name,ids in groups:
 for id in ids:B[id]['connectedGroup']=name
report={'roadBuildingIntersections':[],'excludedIntrusions':[],'waterOrSportsIntrusions':[],'outOfSite':[],'unrelatedBuildingOverlaps':[],'connectedVolumes':groups}
for r in d['roads']+[{**c,'width':6} for c in d['connections']]:
 line=LineString(r['points']).buffer(r['width']/2)
 for b in d['buildings']:
  a=line.intersection(Polygon(b['polygon'])).area
  if a>.001:report['roadBuildingIntersections'].append([r['id'],b['id'],round(a,4)])
 if r.get('kind')!='external':
  if line.intersection(ex).area>.001:report['excludedIntrusions'].append([r['id'],round(line.intersection(ex).area,4)])
  for s in d['spaces']:
   if s['kind'] in ['water','sport','track'] and line.intersection(Polygon(s['polygon'])).area>.001:report['waterOrSportsIntrusions'].append([r['id'],s['id'],round(line.intersection(Polygon(s['polygon'])).area,4)])
for b in d['buildings']:
 a=Polygon(b['polygon']).difference(site).area
 if a>.001:report['outOfSite'].append([b['id'],round(a,4)])
for i,b in enumerate(d['buildings']):
 for c in d['buildings'][i+1:]:
  a=Polygon(b['polygon']).intersection(Polygon(c['polygon'])).area
  if a>1 and not (b.get('connectedGroup') and b.get('connectedGroup')==c.get('connectedGroup')):report['unrelatedBuildingOverlaps'].append([b['id'],c['id'],round(a,3)])
d['scope']='三大片区与一处独立附属地块；建筑以平面占位登记，数量不等同实际栋数。内部主通路为规划通行带，细支路及门位在P02核对。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));(p.parent/'布局几何检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
