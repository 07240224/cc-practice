import json,sys,base64,math
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString,Point,mapping
from shapely.ops import unary_union,nearest_points
from shapely.prepared import prep
out=Path('/workspace/cc-practice/可行走底图');d=json.loads(Path('/workspace/cc-practice/地图规划/地面底图R3/地面底图数据.json').read_text());B={b['id']:b for b in d['buildings']}
roads=[r for r in d['roads'] if r['kind']=='internal' and r['id']!='D7']
for r in roads:
 if r['id']=='D4':r['points']=r['points'][:5]
 if r['id']=='D2':r['points']=r['points'][:-1]
roads += [{'id':'RED1','name':'球场北侧补路','points':[[1030,611],[1034,598],[1061,583],[1067,583]],'width':7}, {'id':'RED2','name':'商学院南侧—梯教北侧补路','points':[[998,941],[1038,925],[1103,896],[1154,868],[1201,844]],'width':7}, {'id':'RED3','name':'三教北侧补路','points':[[1051,957],[1097,938],[1154,916],[1177,907],[1190,900.6],[1220,893]],'width':7}]
# Align the short red north connection to the existing inner campus axis, never crossing a wall.
axis=d['connections'][1];roads.append({**axis,'id':'INNER_AXIS','kind':'internal','width':7})
# White ground route access from each gate goes only towards its own internal spawn.
roads.append({'id':'W-PORTAL','name':'武川侧传送门前场','points':[[770,696],[776,697]],'width':9})
roads.append({'id':'E-PORTAL','name':'国定武东侧传送门前场','points':[[838,701],[829,706]],'width':9})
def poly(b):return unary_union([Polygon(b['polygon'],b.get('holes'))]+[Polygon(a['polygon'],a.get('holes')) for a in b.get('additionalFootprints',[])])
def rings(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [{'outer':list(g.exterior.coords),'holes':[list(h.coords) for h in g.interiors]}]
 return [p for x in g.geoms for p in rings(x)]
world={'scale':10,'projection':{'a':.9,'b':1.15,'c':-.12,'d':.65,'z':.92},'maps':{},'revision':'walkable-base-v1','corrections':{'added':['RED1','RED2','RED3'],'removed':['D7','D4 south-east tail','D2 south tip'],'crossCampus':'C01 removed; two-way portals only'}}
for mid,zones,spawn,portal in [('wuchuan',['W'],[770,696],[776,697]),('guoding',['G','D'],[838,701],[829,706])]:
 site=unary_union([Polygon(c['polygon']) for c in d['campuses'] if c['id'] in zones])
 # G and D are adjoining parts of the same game map; their union forms the surrounding wall.
 buildings=[b for b in d['buildings'] if b['zone'] in zones]
 solid=unary_union([poly(b) for b in buildings]+[Polygon(s['polygon']) for s in d['spaces'] if s['kind'] in ['water'] and Polygon(s['polygon']).intersects(site)]+[Polygon(x['polygon']) for x in d['exclusions']])
 walk=site.buffer(-1.8).difference(solid.buffer(1.2));pr=prep(walk)
 rr=[];roadshapes=[];hits=[]
 for r in roads:
  line=LineString(r['points']);surface=line.buffer(r['width']/2,join_style=1)
  if not surface.intersects(site):continue
  clipped=surface.intersection(site).difference(solid)
  rr.append(r);roadshapes.append(clipped)
  if r['id'].startswith('RED'):
   a=surface.intersection(solid).area
   if a>.01:hits.append([r['id'],round(a,3)])
 surface=unary_union(roadshapes)
 minx,miny,maxx,maxy=site.bounds;step=2;cols=math.ceil((maxx-minx)/step)+1;rows=math.ceil((maxy-miny)/step)+1
 grid=bytearray(cols*rows)
 for j in range(rows):
  for i in range(cols):
   x=minx+i*step;y=miny+j*step
   if pr.contains(Point(x,y)):grid[j*cols+i]=1 if surface.distance(Point(x,y))<.5 else 2
 if not pr.contains(Point(spawn)):
  q=nearest_points(walk,Point(spawn))[0];spawn=[q.x,q.y]
 world['maps'][mid]={'name':'武川校区' if mid=='wuchuan' else '国定—武东校区','site':rings(site),'bounds':[minx,miny,maxx,maxy],'buildings':buildings,'roads':rr,'roadSurface':rings(surface),'walkSurface':rings(walk),'spaces':[s for s in d['spaces'] if Polygon(s['polygon']).intersects(site)],'spawn':spawn,'portal':portal,'grid':{'origin':[minx,miny],'step':step,'cols':cols,'rows':rows,'data':base64.b64encode(grid).decode()},'redRoadObstacleOverlap':hits}
 print(mid,'site',site.geom_type,'spawn',spawn,'redconflicts',hits,'grid',cols,rows)
(out/'地图数据.json').write_text(json.dumps(world,ensure_ascii=False,separators=(',',':')))
a=json.loads(Path('/workspace/scratch/campus-planning/sample-assets.json').read_text())
assets=out/'assets';assets.mkdir(exist_ok=True)
for key in ['student','grass']:
 (assets/(key+'.png')).write_bytes(base64.b64decode(a[key].split(',')[1]))
(out/'人物帧.json').write_text(json.dumps(a['frames']))
