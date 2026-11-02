from pathlib import Path
import json,sys,math,base64
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union,nearest_points
from shapely.prepared import prep
out=Path('/workspace/cc-practice/正交可行走底图');f=json.loads(Path('/workspace/cc-practice/占地复核图/轮廓与道路.json').read_text());old=json.loads(Path('/workspace/cc-practice/可行走底图/地图数据.json').read_text());scale=1
# Real calibration volumes have independent, editable local geometry; no extrusion of reference outlines.
models=[{'id':'lecture','label':'武东路梯教','map':'guoding','center':[1190,879],'rotation':25,'width':48,'depth':16,'height':22.2,'entryLocal':[-6.5,10.6],'kind':'painted'}, {'id':'teaching3','label':'第三教学楼','map':'guoding','center':[1154,939],'rotation':25,'width':64,'depth':20,'height':22.2,'entryLocal':[-20,13],'kind':'painted'}, {'id':'student_center','label':'学生中心 · 体块校准','map':'guoding','center':[1175,700],'rotation':25,'width':30,'depth':44,'height':10.8,'kind':'calibration'}]
def world(m,x,z):
 t=math.radians(m['rotation']);return [m['center'][0]+math.cos(t)*x+math.sin(t)*z,m['center'][1]-math.sin(t)*x+math.cos(t)*z]
def rect(m,x,z,w,h):return Polygon([world(m,x,z),world(m,x+w,z),world(m,x+w,z+h),world(m,x,z+h)])
solids=[]
for m in models:
 if m['id']=='lecture':parts=[rect(m,-24,-8,48,16)]
 elif m['id']=='teaching3':parts=[rect(m,-32,-10,10,21.2),rect(m,-22,-10,54,20)]
 else:parts=[rect(m,-15,-22,30,7),rect(m,-15,-15,5,37),rect(m,8,-5,7,17),rect(m,-10,0,18,6),rect(m,-15,15,30,7)]
 m['actualBuildingFootprint']=[list(q.exterior.coords)[:-1] for q in parts];solids.extend(parts)
 if 'entryLocal'in m:m['entry']=world(m,*m['entryLocal'])
 if m['kind']=='painted':
  x=m['entryLocal'][0];z=m['depth']/2+2
  postx=[x-3.4,x+3.4] if m['id']=='lecture' else [x-3.5]
  m['posts']=[{'center':world(m,p,z),'size':.42 if m['id']=='lecture' else .65} for p in postx]
  for post in m['posts']:
   xx,zz=post['center'];s=post['size'];solids.append(Polygon([[xx-s/2,zz-s/2],[xx+s/2,zz-s/2],[xx+s/2,zz+s/2],[xx-s/2,zz+s/2]]))
# A raised corridor connects real faces; four feet remain outside the cross road.
bridge={'start':world(models[0],-17,8),'end':world(models[1],30,-10),'width':4,'deckHeight':6.2,'clearance':5.85,'posts':[]}
for end in [bridge['start'],bridge['end']]:
 for dx in [-2.2,2.2]:
  p=[end[0]+dx,end[1]];bridge['posts'].append(p);solids.append(Point(p).buffer(.3))
# Road centerlines consist only of straight segments. Only actual junction nodes receive rounded corners.
roads=[]
seen=set()
for mid,mp in old['maps'].items():
 for r in mp['roads']:
  if r['id'] in seen:continue
  seen.add(r['id']);r=dict(r);r['points']=[list(p) for p in LineString(r['points']).simplify(1.2).coords];r['map']='wuchuan' if mid=='wuchuan' else 'guoding';roads.append(r)
R={r['id']:r for r in roads}
R['D1']['points']=[[811,711],[913,675],[975,625],[1027,604],[1034,598]]
R['D2']['points']=[[1096,611],[1132,687],[1173,779],[1195,819],[1224,880],[1234,961]]
R['RED2']['points'][-1]=[1207,844];R['RED3']['points'][-1]=[1226,893];R['D5']['points'][-1]=[1233,956]
R['D3']['points'][-1]=[1013,850];R['D6']['points']=[[913,675],[942,690],[1013,850]]
R['INNER_AXIS']['points']=[[936,363],[909,447],[924,467],[960,477],[994,467],[1025,490],[1049,555],[1067,583],[1083,581],[1096,611],[1132,687],[1173,779]]
# Reservation envelopes remain ground planning aids and are never blocking volumes.
ref=[]
for a in f['nameAnchors']:
 # Explicit box is only a parcel marker; real buildings can replace it with their own footprint.
 ref.append({'id':a['id'],'name':a['name'],'center':[a['x'],a['y']],'reservationEnvelope':[[a['x']-12,a['y']-6],[a['x']+12,a['y']-6],[a['x']+12,a['y']+6],[a['x']-12,a['y']+6]],'collidable':False})
wall=unary_union([LineString(s) for s in f['sportsEnclosure']['wallSegments']]);obstacles=unary_union(solids+[wall.buffer(.3)])
def rings(q):
 if q.is_empty:return[]
 if q.geom_type=='Polygon':return[{'outer':list(q.exterior.coords)[:-1],'holes':[list(h.coords)[:-1] for h in q.interiors]}]
 return[p for g in q.geoms for p in rings(g)]
D={'revision':'ortho-ground-v2','camera':{'type':'OrthographicCamera','elevationFromHorizontal':35,'azimuthFromSouth':12.5,'viewHeight':80},'scale':{'referenceToWorld':1,'characterHeight':2.5,'characterRadius':.6,'doorHeight':3.1,'floorHeight':3.7,'units':'统一游戏单位；不宣称测绘米制'},'models':models,'bridge':bridge,'maps':{},'sportsEnclosure':f['sportsEnclosure'],'sports':f['sports'],'spaces':f['spaces'],'reservations':ref,'referenceFootprints':f['buildings']}
for mid,zones,spawn,portal in [('wuchuan',['W'],[770,696],[776,697]),('guoding',['G','D'],[1140,972],[829,706])]:
 site=unary_union([Polygon(c['polygon']) for c in f['campuses'] if c['id'] in zones]);water=unary_union([Polygon(s['polygon']) for s in f['spaces'] if s['kind']=='water' and Polygon(s['polygon']).intersects(site)]);ex=unary_union([Polygon(s['polygon']) for s in f['exclusions']]);obs=(obstacles if mid=='guoding' else Polygon()).union(water).union(ex)
 walk=site.buffer(-.85).difference(obs.buffer(.65));pw=prep(walk)
 rr=[r for r in roads if r['map']==mid];lines=[LineString(r['points']) for r in rr]
 asphalt=unary_union([line.buffer(r['width']/2,cap_style=2,join_style=2) for line,r in zip(lines,rr)])
 # Round only intersections between different straight road segments.
 junctions=[]
 for i,a in enumerate(lines):
  for b in lines[i+1:]:
   hit=a.intersection(b)
   pp=[hit] if hit.geom_type=='Point' else list(hit.geoms) if hit.geom_type=='MultiPoint' else []
   for pt in pp:
    if not any(pt.distance(p)<2 for p in junctions):junctions.append(pt)
 for pt in junctions:asphalt=asphalt.union(pt.buffer(4.4,quad_segs=10))
 paving=asphalt.buffer(1.4,join_style=2)
 if mid=='guoding':
  # Door aprons connect from real entries to the straight road system.
  for m in models[:2]:
   dest=nearest_points(asphalt,Point(m['entry']))[0]
   path=LineString([m['entry'],[dest.x,dest.y]])
   paving=paving.union(path.buffer(2.5,cap_style=2,join_style=2)).union(rect(m,m['entryLocal'][0]-6,m['depth']/2,12,6))
  for g in f['sportsEnclosure']['gates']:
   p=g['point'];paving=paving.union(Point(p).buffer(g['width']/2))
 asphalt=asphalt.intersection(site);paving=paving.intersection(site)
 # Never hide a road/building mistake by clipping asphalt to guessed building outlines.
 road_hits=[]
 if mid=='guoding':
  for m in models:
   q=unary_union([Polygon(p) for p in m['actualBuildingFootprint']]);area=q.intersection(asphalt).area
   if area>.01:road_hits.append([m['id'],round(area,3)])
 x0,y0,x1,y1=site.bounds;step=1.5;cols=math.ceil((x1-x0)/step)+1;rows=math.ceil((y1-y0)/step)+1;grid=bytearray(cols*rows);prs=prep(asphalt.buffer(.2))
 for y in range(rows):
  for x in range(cols):
   p=Point(x0+x*step,y0+y*step)
   if pw.contains(p):grid[y*cols+x]=1 if prs.contains(p) else 2
 assert pw.contains(Point(spawn)),(mid,'bad spawn');assert pw.contains(Point(portal)),(mid,'bad portal')
 D['maps'][mid]={'name':'武川校区' if mid=='wuchuan' else '国定—武东校区','site':rings(site),'walkSurface':rings(walk),'asphalt':rings(asphalt),'paving':rings(paving),'bounds':list(site.bounds),'spawn':spawn,'portal':portal,'roads':rr,'junctions':[[p.x,p.y] for p in junctions],'roadBuildingHits':road_hits,'grid':{'origin':[x0,y0],'step':step,'cols':cols,'rows':rows,'data':base64.b64encode(grid).decode()}}
 print(mid,'grid',cols,rows,'actual buildings/road overlap',road_hits,'junctions',len(junctions))
(out/'场景数据.json').write_text(json.dumps(D,ensure_ascii=False,separators=(',',':')))
