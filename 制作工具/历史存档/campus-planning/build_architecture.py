from pathlib import Path
import json,sys,math,base64,copy
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union,nearest_points
from shapely.prepared import prep
O=Path('/workspace/cc-practice/校园建筑版');D=json.loads(Path('/workspace/cc-practice/正交可行走底图/场景数据.json').read_text());F=json.loads(Path('/workspace/cc-practice/占地复核图/轮廓与道路.json').read_text());anchors={a['id']:a for a in F['nameAnchors']}
models=[]
def body(x,z,w,d,f=3,style='cream',roof='flat',y=0,h=None):return dict(x=x,z=z,w=w,d=d,h=h or f*3.7,floors=f,style=style,roof=roof,y=y)
def add(id,lot,kind,w,d,f=3,rotation=0,parts=None,center=None,entry=None,detail='main',**kw):
 a=anchors[lot];m=dict(id=id,lot=lot,label=a['name'],map='wuchuan' if lot.startswith('W') else 'guoding',kind=kind,center=center or [round(a['x'],2),round(a['y'],2)],rotation=rotation,width=w,depth=d,height=f*3.7,parts=parts or [body(0,0,w,d,f,kw.get('style','cream'),kw.get('roof','flat'))],entryLocal=entry or [0,d/2+3.0],detail=detail,**kw);models.append(m);return m
# Three identities on one physically continuous building. No generated signs or physical name plates.
tri=add('academic_link','D09','academic_link',128,20,6,25,center=[1154,939],parts=[body(0,0,128,20,6,'academic')],entries=[dict(id='sime',x=-44,z=10,porch='single'),dict(id='scai',x=0,z=10,porch='single'),dict(id='teaching3',x=44,z=10,porch='wide')],entry=[44,14],fixed=True)
lec=add('wudonglecture','D08','academic',48,16,6,25,center=[1190,879],style='academic',porch='double',entry=[-6.5,11],fixed=True)
add('statistics','D07','statistics',58,24,3,25,parts=[body(-20.5,0,17,24,3,'statistics'),body(20.5,0,17,24,3,'statistics'),body(0,-2,24,20,2,'statistics'),body(0,0,24,24,1,'statistics','frontgable',y=7.4),body(-10.5,10,3,4,2,'statistics'),body(10.5,10,3,4,2,'statistics'),body(-3.8,10.7,.65,2.6,2,'statistics'),body(3.8,10.7,.65,2.6,2,'statistics')],entry=[0,11])
add('finance','D02','finance',54,26,4,-20,parts=[body(-18,0,18,24,3,'stone'),body(18,0,18,24,3,'stone'),body(0,0,18,26,4,'financecenter')],entry=[0,16],arcade=True)
add('activity','G48','activity',37,43,3,25,parts=[body(0,-16,37,11,3,'redwhite'),body(-13,0,11,22,3,'redwhite'),body(.5,-4,16,6,3,'redwhite'),body(13,-4,11,20,3,'redwhite'),body(0,16,37,11,3,'redwhite')],entry=[0,24],porch='double')
add('research','G43','research',86,58,14,0,parts=[body(0,0,37,24,14,'redtower'),body(-30,3,22,39,2,'redtower'),body(28,3,18,39,2,'redtower'),body(0,16,39,12,2,'redtower')],entry=[0,25],porch='glass')
# White arched bookstore is near Guoding-Wudong junction, not the old north-campus game coordinate.
add('bookstore','G46','bookstore',28,12,3,25,center=[1129,615],parts=[body(-3,0,22,12,3,'bookstore'),dict(body(8,0,12,12,3,'bookstore'),shape='round')],entry=[17,0],arcade=True)
add('guoding_gym','G17','gym',106,75,6,0,parts=[body(0,0,101,70,1,'gymbase',h=4.5),body(0,-1,100,66,1,'metal',y=4.5,h=17)],entry=[-25,40],fixed=False)
add('teaching1','G22','teaching',58,21,4,0,style='cream',roof='terrace',porch='redhip')
add('teaching2','G21','teaching',91,24,4,0,style='cream',roof='terrace',porch='redhip')
add('guodinglecture','G23','hall',35,25,2,0,style='ivory',roof='flat',porch='double')
add('greenleaf_canteen','G26','greenleaf',64,26,2,0,style='cream',roof='hip',porch='glass')
# The small cafe has a separate orange corrugated volume, beside the sixth-dorm living district.
add('sufe_cafe','G28','cafe',38,17,2,0,center=[1252,466],style='cafe',roof='gable',porch='glass')
add('halal_canteen','G41','halal',72,24,2,0,parts=[body(0,0,72,24,2,'brick','hip')],porch='double')
add('third_canteen','G10','newcanteen',57,35,3,-18,style='brick',roof='flat',porch='glass')
add('cainiao_station','G50','cainiao',18,12,1,25,center=[1839,623],style='ivory',roof='flat',porch='blue')
add('old_gate','D04','oldgate',18,4,2,-20,center=[840,842],parts=[body(-6.25,0,5.5,4,1,'stone',h=5.5),body(6.25,0,5.5,4,1,'stone',h=5.5),body(0,0,7,4,1,'stone',y=4.3,h=1.2)],entry=[0,6],detail='main')
add('water_tower','G28','watertower',15,15,7,0,center=[1252,440],parts=[dict(body(0,0,5,5,7,'stone',h=23),shape='round')],entry=[0,6],detail='main')
# Distinct west-campus landmarks.
add('library','W06','library',105,72,7,20,parts=[body(20,-9,62,24,7,'library'),body(-37,2,19,51,5,'library'),body(3,28,61,17,5,'library'),body(39,18,17,29,7,'libraryend')],entry=[39,35.5],porch='glass')
add('accounting','W01','accounting',82,43,4,0,parts=[body(0,-8,82,28,4,'pink'),body(0,12,70,15,2,'pink')],entry=[0,23],porch='glass')
add('teaching4','W08','teaching4',92,30,5,20,style='academic',porch='double')
add('economics','W10','economics',48,32,7,20,parts=[body(-16,0,16,32,7,'ivory'),body(8,2,32,27,6,'ivory')],entry=[0,19],porch='glass')
add('phoenix','W02','phoenix',72,30,5,20,style='cream',porch='glass')
add('enterprise','W03','enterprise',44,25,3,65,style='brick',porch='frame')
add('wuchuan_pool','W04','sporthall',46,32,2,65,style='cream',roof='gable')
add('exchange','W05','exchange',79,34,3,0,style='ivory',roof='hip')
add('wuchuan_hall','W07','sporthall',77,48,2,20,style='brick',roof='gable')
add('badminton','W09','sporthall',61,39,2,20,style='cream',roof='gable')
add('wuchuan_canteen','W12','canteen',49,28,3,20,style='cream',porch='glass')
add('advanced_research','W11','office',43,17,4,20,style='cream',detail='context')
# Residential and office context is grouped by original rows, with real floors/window rhythms and simpler detail.
for lot,w,d in [('W13',35,16),('W14',35,16),('W15',32,16),('W16',35,17),('W17',35,17),('W18',35,18)]:add(lot.lower(),lot,'dorm',w,d,6,20,style='dorm',roof='hip',detail='context')
for lot,w,d,r in [('G01',25,67,-8),('G02',76,23,0),('G03',73,20,0),('G04',19,61,0),('G05',45,17,0),('G06',40,19,0),('G07',49,22,0),('G08',45,23,0),('G11',29,16,25),('G12',32,17,25),('G13',31,17,25),('G14',31,24,25),('G15',29,23,25),('G16',31,18,25),('G29',40,19,0),('G34',47,20,0),('G35',47,20,0)]:add(lot.lower(),lot,'dorm',w,d,6,r,style='dorm',roof='hip',detail='context')
for lot in ['G30','G31','G32','G33']:
 add(lot.lower(),lot,'dormL',44,28,6,0,parts=[body(0,-8,44,12,6,'dorm','hip'),body(-16,6,12,16,6,'dorm','hip')],detail='context')
add('g09','G09','dormcourt',45,58,6,-18,parts=[body(0,-23,45,12,6,'dorm'),body(0,23,45,12,6,'dorm'),body(0,0,12,20,5,'cream'),body(17,0,11,34,6,'dorm')],entry=[-26,0],detail='context')
for id,lot,kind,w,d,f,r,style in [('admin','G18','office',63,36,5,0,'cream'),('tech_n','G19','office',68,23,5,0,'cream'),('tech_s','G20','office',68,23,5,0,'cream'),('law','G24','office',48,24,4,0,'cream'),('graduate','G27','office',46,30,4,0,'cream'),('bath','G25','service',48,17,2,0,'cream'),('medical','G42','medical',76,21,2,0,'redwhite'),('redtile','G39','redtile',69,32,7,0,'brick'),('art','G40','art',75,55,3,25,'brick'),('museum','G36','museum',41,47,3,0,'cream'),('archive','G38','office',38,20,3,0,'cream'),('ningyuanB','G45','office',39,33,3,25,'cream'),('ningyuanA','G47','office',42,31,3,25,'cream'),('teacher','D01','office',59,28,3,25,'cream'),('humanities','D04','humanities',55,33,3,25,'brick'),('business','D06','business',66,30,4,25,'ivory'),('westoffice','D03','office',35,57,4,25,'cream'),('affairs','D11','office',38,24,3,25,'cream'),('stats_e','D12','office',38,24,3,25,'gray')]:
 add(id,lot,kind,w,d,f,r,style=style,roof='hip' if kind in ['redtile','humanities'] else 'flat',detail='main' if kind in ['art','museum','medical','business','humanities'] else 'context',porch='double')
next(m for m in models if m['id']=='medical')['rotation']=180
na=next(m for m in models if m['id']=='ningyuanA');na['center']=[1153,650];na['layoutAdjustment']='向校内东南8个单位微移，释放匡时书店前场视线。'
art=next(m for m in models if m['id']=='art');art.update(rotation=0,width=66,depth=44,parts=[body(0,2,66,34,2,'brick','hip'),body(0,-8,26,22,4,'brick')],entryLocal=[0,22])
# Avoid guessing many tiny buildings. The user's simplification policy omits these altogether.
for model in models:
 if model['kind'] not in ['academic_link','bookstore','finance','dormcourt','gym','cainiao','watertower','oldgate']:
  x=model['entryLocal'][0];faces=[p['z']+p['d']/2 for p in model['parts'] if p['y']==0 and p['x']-p['w']/2<=x<=p['x']+p['w']/2]
  if faces:model['entryFace']=max(faces);model['entryLocal'][1]=model['entryFace']+3
D['models']=models;D['revision']='campus-architecture-v1';D['reservations']=[]
D['identities']=[{'id':m['id'],'model':m['id']} for m in models]+[{'id':x,'model':'academic_link'} for x in ['sime','scai','teaching3']]+[{'id':'student_dormitory','model':'g30'}]
D['models'][0]['label']='连体教学与院楼'
def world(m,x,z):
 t=math.radians(m['rotation']);return[m['center'][0]+math.cos(t)*x+math.sin(t)*z,m['center'][1]-math.sin(t)*x+math.cos(t)*z]
def localrect(m,x,z,w,d):return Polygon([world(m,x-w/2,z-d/2),world(m,x+w/2,z-d/2),world(m,x+w/2,z+d/2),world(m,x-w/2,z+d/2)])
def footprint(m):return unary_union([Point(world(m,p['x'],p['z'])).buffer(p['w']/2,quad_segs=16) if p.get('shape')=='round' else localrect(m,p['x'],p['z'],p['w'],p['d']) for p in m['parts'] if p['y']<.1])
def rings(q):
 if q.is_empty:return[]
 if q.geom_type=='Polygon':return[{'outer':list(q.exterior.coords)[:-1],'holes':[list(h.coords)[:-1] for h in q.interiors]}]
 return[p for g in q.geoms for p in rings(g)]
report={'placements':[],'roadBuildingOverlaps':[],'buildingOverlaps':[]}
# Keep all straight centerlines and both campus boundaries. Only the south-front walk is shifted to clear the corrected connected facade.
D['maps']['guoding']['roads'].append({'id':'TEACHING_LINK','width':3.4,'points':[[1603,431],[1740,431]],'map':'guoding','purpose':'一教二教间步道与上层连廊下通路'})
for mp in D['maps'].values():
 for r in mp['roads']:
  if r['id']=='D4':r['points']=[[959,909],[1009,949],[1030,950],[1080,984],[1125,989]]
  if r['id']=='D5':r['points']=[[1125,989],[1233,956]]
for mid,mp in D['maps'].items():
 site=unary_union([Polygon(r['outer'],r.get('holes',[])) for r in mp['site']]);rr=mp['roads'];lines=[LineString(r['points']) for r in rr];asphalt=unary_union([line.buffer(r['width']/2,cap_style=2,join_style=2) for line,r in zip(lines,rr)])
 junctions=[]
 for i,a in enumerate(lines):
  for b in lines[i+1:]:
   hit=a.intersection(b);pp=[hit] if hit.geom_type=='Point' else list(hit.geoms) if hit.geom_type=='MultiPoint' else []
   for pt in pp:
    if not any(pt.distance(p)<2 for p in junctions):junctions.append(pt)
 for pt in junctions:asphalt=asphalt.union(pt.buffer(4.4,quad_segs=10))
 water=unary_union([Polygon(s['polygon']) for s in D['spaces'] if s['kind']=='water' and Polygon(s['polygon']).intersects(site)])
 ex=unary_union([Polygon(s['polygon']) for s in F['exclusions']]);sports=Polygon(D['sportsEnclosure']['polygon']) if mid=='guoding' and 'polygon'in D['sportsEnclosure'] else unary_union([LineString(l).buffer(.3) for l in D['sportsEnclosure']['wallSegments']]).convex_hull if mid=='guoding' else Polygon()
 static=asphalt.buffer(2).union(water.buffer(1)).union(ex).union(sports)
 used=[]
 for m in [x for x in models if x['map']==mid]:
  origin=m['center'][:];sh=footprint(m)
  if not m.get('fixed'):
   candidates=[(0,0)]+[(dx,dz) for rad in range(2,57,2) for dx in range(-rad,rad+1,2) for dz in range(-rad,rad+1,2) if max(abs(dx),abs(dz))==rad]
   best=None
   for dx,dz in sorted(candidates,key=lambda q:q[0]**2+q[1]**2):
    from shapely.affinity import translate
    q=translate(sh,dx,dz)
    if not site.buffer(-1.3).covers(q):continue
    if q.intersection(static).area>.015:continue
    if any(q.distance(v)<2.2 for v in used):continue
    best=[origin[0]+dx,origin[1]+dz];break
   if best:m['center']=best;sh=footprint(m)
   else:print('NO FIT',m['id'],flush=True)
  used.append(sh)
  m['actualBuildingFootprint']=rings(sh);m['entry']=world(m,*m['entryLocal']);m['originalAnchor']=origin
  m['placementShift']=[round(m['center'][i]-origin[i],2) for i in range(2)]
  for e in m.get('entries',[]):e['world']=world(m,e['x'],e['z']+4)
  report['placements'].append({'id':m['id'],'lot':m['lot'],'shift':m['placementShift']})
  area=sh.intersection(asphalt).area
  if area>.015:report['roadBuildingOverlaps'].append([m['id'],round(area,3)])
 if mid=='guoding':
  D['bridge']['start']=world(lec,-17,8);D['bridge']['end']=world(tri,30,-10)
 solids=[footprint(m) for m in models if m['map']==mid]
 for i,m in enumerate([x for x in models if x['map']==mid]):
  for j in range(i):
   ar=solids[i].intersection(solids[j]).area
   if ar>.015:report['buildingOverlaps'].append([m['id'],[x for x in models if x['map']==mid][j]['id'],round(ar,3)])
 if mid=='guoding':
  t1=next(m for m in models if m['id']=='teaching1');t2=next(m for m in models if m['id']=='teaching2');xx=(max(t1['center'][0]-t1['width']/2,t2['center'][0]-t2['width']/2)+min(t1['center'][0]+t1['width']/2,t2['center'][0]+t2['width']/2))/2
  b2={'id':'north-teaching-link','start':[xx,t2['center'][1]+12],'end':[xx,t1['center'][1]-10.5],'width':3.4,'deckHeight':6.2,'clearance':5.85,'posts':[]};b2['posts']=[[xx+dx,pt[1]] for pt in [b2['start'],b2['end']] for dx in [-1.45,1.45]];D['bridges']=[dict(D['bridge'],id='wudong-link'),b2]
 wall=unary_union([LineString(l).buffer(.3) for l in D['sportsEnclosure']['wallSegments']]) if mid=='guoding' else Polygon()
 # Add realistic entrance canopies as separate collision posts; the canopy itself stays overhead.
 for m in [x for x in models if x['map']==mid]:
  m['posts']=[];m['groundFixtures']=[]
  if m['kind']=='cainiao':m['groundFixtures']=[rings(localrect(m,x,4.5,2.6,1.1))[0] for x in [-10.5,10.5]]
  if m['kind']=='halal':m['groundFixtures']=[rings(localrect(m,38,-4,3.0,13.4))[0]]
  for q in m['groundFixtures']:solids.append(Polygon(q['outer']))
  entries=m.get('entries') or [dict(x=m['entryLocal'][0],z=m.get('entryFace',m['depth']/2),porch=m.get('porch','double'))]
  if m['kind'] in ['finance','bookstore','dormcourt','gym','cainiao','oldgate','watertower','statistics']:entries=[]
  for e in entries:
   if e.get('porch') in ['single','double','wide','redhip','frame']:
    size=.5;px=[e['x']-3.5] if e['porch']=='single' else [e['x']-4,e['x']+4]
    for x in px:
     p=world(m,x,e['z']+2.1);post=Point(p).buffer(size/2);solids.append(post);m['posts'].append({'center':p,'size':size})
 solids.extend([Point(p).buffer(.3) for b in D.get('bridges',[D['bridge']]) for p in b['posts']] if mid=='guoding' else []);obstacles=unary_union(solids+[water,ex,wall]);walk=site.buffer(-.85).difference(obstacles.buffer(.65));paving=asphalt.buffer(1.4,join_style=2)
 for m in [x for x in models if x['map']==mid]:
  entries=[e['world'] for e in m.get('entries',[])] or [m['entry']]
  for e in entries:
   dest=nearest_points(asphalt,Point(e))[0];seg=LineString([e,[dest.x,dest.y]]);paving=paving.union(seg.buffer(2.4,cap_style=2,join_style=2)).union(Point(e).buffer(3,quad_segs=2))
  # Entrance approach selected on the same sidewalk system, exact valid point for route checks.
  e=Point(m['entry']);q=nearest_points(walk.buffer(-.12),e)[0];m['arrival']=[q.x,q.y]
 if mid=='guoding':
  for g in D['sportsEnclosure']['gates']:paving=paving.union(Point(g['point']).buffer(g['width']/2))
 pw=prep(walk);nav=prep(walk.buffer(-1.12));prs=prep(asphalt.buffer(.2));x0,y0,x1,y1=site.bounds;step=1.5;cols=math.ceil((x1-x0)/step)+1;rows=math.ceil((y1-y0)/step)+1;grid=bytearray(cols*rows)
 for y in range(rows):
  for x in range(cols):
   pt=Point(x0+x*step,y0+y*step)
   if nav.contains(pt):grid[y*cols+x]=1 if prs.contains(pt) else 2
 assert pw.contains(Point(mp['spawn'])),(mid,'bad spawn')
 assert pw.contains(Point(mp['portal'])),(mid,'bad portal')
 mp.update(walkSurface=rings(walk),asphalt=rings(asphalt.intersection(site)),paving=rings(paving.intersection(site)),roadBuildingHits=report['roadBuildingOverlaps'],grid={'origin':[x0,y0],'step':step,'cols':cols,'rows':rows,'data':base64.b64encode(grid).decode()})
 print(mid,len(solids),'buildings',flush=True)
(O/'场景数据.json').write_text(json.dumps(D,ensure_ascii=False,separators=(',',':')));(O/'落位检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('models',len(models),'road hits',report['roadBuildingOverlaps'],'building hits',report['buildingOverlaps'],flush=True)
