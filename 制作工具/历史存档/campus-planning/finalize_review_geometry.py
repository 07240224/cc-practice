from pathlib import Path
import json,sys,math
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/占地复核图/轮廓与道路.json');d=json.loads(p.read_text())
def toshape(q):return {'outer':[list(x) for x in list(q.exterior.coords)[:-1]],'holes':[[list(x) for x in list(h.coords)[:-1]] for h in q.interiors]}
def split(q):
 if q.is_empty:return[]
 if q.geom_type=='Polygon':return[toshape(q)]
 return [s for g in q.geoms for s in split(g)]
# The beige C-shaped feature north of the orange gym is paved forecourt.
d['forecourts']=[{**s,'name':'新体育馆北侧铺装前场'} for s in d['buildings'] if s['id']=='C125'];d['buildings']=[s for s in d['buildings'] if s['id']!='C125']
# Stadium: fit the two straight sides and tangent semicircular ends to the reference long-axis envelope.
cx,cy=1044.177,752.423;angle=math.radians(65.746);length,width=201.408,101.248;half=(length-width)/2;u=(math.cos(angle),math.sin(angle));a=(cx-u[0]*half,cy-u[1]*half);b=(cx+u[0]*half,cy+u[1]*half)
inner=LineString([a,b]).buffer(width/2,quad_segs=48);outer=LineString([a,b]).buffer(width/2+7,quad_segs=48)
d['sports']=[{'name':'运动场跑道及内场','outer':toshape(outer)['outer'],'holes':[toshape(inner)['outer']],'longAxis':[list(a),list(b)],'method':'依参考图长轴与内场边界拟合直道和相切弧线，入口通道独立'}]
# Explicit upper structure/ground passage relation at the stair classroom connection.
passage={'name':'梯教—三教架空连廊下通路','points':d['redAdditions'][2][3:],'width':7,'upperStructure':'C009','type':'上层连廊，地面贯通'}
d['passages'].append(passage)
road=unary_union([Polygon(r['outer'],r['holes']) for r in d['roadSurfaces']]+[Polygon(f['outer'],f['holes']) for f in d['forecourts']]+[LineString(x['points']).buffer(x['width']/2) for x in d['passages']])
for s in d['buildings']:
 q=Polygon(s['outer'],s['holes'])
 if s['id']=='C009':
  under=LineString(passage['points']).buffer(passage['width']/2)
  s['referenceOutline']={'outer':s['outer'],'holes':s['holes']};s['groundParts']=split(q.difference(under));s['upperParts']=split(q.intersection(under));s['note']='整体参考轮廓保留，连廊处区别上层构件与地面通道'
 else:road=road.difference(q)
d['roadSurfaces']=split(road)
for s in d['spaces']:
 if s['id']=='D-COURTS':s['polygon']=[[1055,609],[1080,599],[1186,825],[1157,838]]
d['spaces'].append({'id':'G-EAST-COURTS','name':'湖东矩形场地','kind':'sport','polygon':[[1391,300],[1438,300],[1438,391],[1391,391]]})
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
print('gym forecourt separated; smooth stadium; underpass retained; sport areas restored')
