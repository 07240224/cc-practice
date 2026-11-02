from pathlib import Path
import sys,json,math
sys.path.insert(0,'/tmp/campus-vector-libs');sys.path.insert(0,'/tmp/campus-plan-libs')
import cv2,numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
out=Path('/workspace/cc-practice/占地复核图');im=cv2.imread('/workspace/scratch/map-review/sufe-official-map.jpg');im=cv2.resize(im,(4096,2286),interpolation=cv2.INTER_AREA);rgb=im[:,:,::-1].astype(np.int16);r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
mask=((r>180)&(g>164)&(b>135)&(r-g>5)&(r-g<38)&(g-b>12)&(g-b<48)).astype(np.uint8)*255
# Preserve real courtyards; remove small text holes and narrow ink gaps only.
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
cont,h=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
for i,c in enumerate(cont):
 if h[0][i][3]>=0:
  hole=np.zeros(mask.shape,np.uint8);cv2.drawContours(hole,[c],-1,255,-1)
  pix=rgb[hole>0];light=(pix.min(axis=1)>220).mean();green=((pix[:,1]>pix[:,0]+5)&(pix[:,1]>pix[:,2]+10)).mean()
  if cv2.contourArea(c)<24 or light+green<.3:cv2.drawContours(mask,[c],-1,255,-1)
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
# The central promenade is paving, not a building connection.
cv2.line(mask,(1220*2,488*2),(1517*2,488*2),0,12)
# Limit to the campus areas; no title/legend beige artifacts outside.
base=json.loads(Path('/workspace/cc-practice/地图规划/地面底图R3/地面底图数据.json').read_text());clip=np.zeros(mask.shape,np.uint8)
for c in base['campuses']:cv2.fillPoly(clip,[np.array(c['polygon'])*2 .__class__(1) if False else np.round(np.array(c['polygon'])*2).astype(np.int32)],255)
# Include full source outline in small boundary tolerance; precise perimeter checked separately.
clip=cv2.dilate(clip,np.ones((19,19),np.uint8));mask=cv2.bitwise_and(mask,clip)
cont,h=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE);shapes=[]
for i,c in enumerate(cont):
 if h[0][i][3]>=0 or cv2.contourArea(c)<20:continue
 p=cv2.approxPolyDP(c,3,True)[:,0,:]/2
 if len(p)<3:continue
 holes=[];j=h[0][i][2]
 while j>=0:
  if cv2.contourArea(cont[j])>120:
   hp=cv2.approxPolyDP(cont[j],3,True)[:,0,:]/2
   if len(hp)>=3:holes.append(hp.tolist())
  j=h[0][j][0]
 poly=Polygon(p,holes)
 if not poly.is_valid:
  p=c[:,0,:]/2;poly=Polygon(p,holes).buffer(0)
 if poly.geom_type!='Polygon':
  poly=max(poly.geoms,key=lambda z:z.area)
 poly=poly.simplify(.7,preserve_topology=True)
 shapes.append({'outer':list(map(list,list(poly.exterior.coords)[:-1])),'holes':[list(map(list,list(x.coords)[:-1])) for x in poly.interiors],'area':poly.area})
# Associate source components with old IDs only for names, never use old rectangles as new geometry.
old={b['id']:Polygon(b['polygon']) for b in base['buildings']};byid={b['id']:b for b in base['buildings']}
for n,s in enumerate(shapes):
 poly=Polygon(s['outer'],s['holes']);scores=sorted([(poly.intersection(p).area,id) for id,p in old.items()],reverse=True);score,id=scores[0]
 s['id']='C%03d'%n;s['oldIDs']=[i for a,i in scores if a>max(8,poly.area*.12)];s['name']=byid[id]['name'] if score>5 else '附属构件';s['zone']=byid[id]['zone'] if score>5 else ('W' if poly.centroid.x<900 else 'G' if poly.centroid.y<630 else 'D')
shapes=[s for s in shapes if s['oldIDs'] or (s['area']>25 and s['area']/max(Polygon(s['outer']).minimum_rotated_rectangle.area,1)>.16)]
# Non-beige buildings use explicit source outlines; retain actual geometry as separate semantic components.
def special(id,box,colorTest,oldIDs):
 x0,y0,x1,y1=box;sel=colorTest.astype(np.uint8)*255;roi=np.zeros_like(sel);cv2.rectangle(roi,(int(x0*2),int(y0*2)),(int(x1*2),int(y1*2)),255,-1);sel=cv2.bitwise_and(sel,roi);sel=cv2.morphologyEx(sel,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8));cs,_=cv2.findContours(sel,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 if not cs:return
 c=max(cs,key=cv2.contourArea);p=(cv2.approxPolyDP(c,2,True)[:,0,:]/2).tolist();shapes.append({'id':'SPECIAL-'+id,'outer':p,'holes':[],'oldIDs':oldIDs,'name':byid[oldIDs[0]]['name'],'zone':byid[oldIDs[0]]['zone'],'method':'非米色构件按参考图轮廓重描'})
special('G17',(1225,242,1355,330),(r>195)&(g>80)&(g<190)&(b<130),['G17'])
special('RESEARCH',(1190,575,1335,710),((r>130)&(r-g>22)&(g>b+12))|((r>45)&(r<120)&(abs(r-g)<20)&(abs(g-b)<20)),['G43','G44'])
special('W21',(487,740,559,796),(b>r+8)&(b>g-10)&(g>60),['W21'])
special('G37',(1573,483,1599,543),(r>120)&(r-g>6)&(g-b>3)&(r-g<35)&(g-b<40),['G37'])
# Ground roads come from the actual white surfaces, retaining widths, courtyards and intersections.
white=((rgb.min(axis=2)>235)&(rgb.max(axis=2)-rgb.min(axis=2)<15)).astype(np.uint8)*255
white=cv2.morphologyEx(white,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,9)));white=cv2.bitwise_and(white,clip)
num,lab,stats,cen=cv2.connectedComponentsWithStats(white);road=np.zeros_like(white)
for i in range(1,num):
 if stats[i,cv2.CC_STAT_AREA]>160:road[lab==i]=255
# Preserve named upper/lower layer connections as dashed pedestrian passage overrides.
passages=[{'name':'一教二教连廊下通路','points':[[1693,425],[1693,440]],'width':4},{'name':'学生中心北侧通道','points':[[1142,666],[1175,650]],'width':4}]
cv2.line(road,(1220*2,488*2),(1517*2,488*2),255,14)
# Apply the user's explicit red additions and blue deletions to this review plan.
red=[[[1030,611],[1034,598],[1061,583],[1067,583]],[[998,941],[1038,925],[1103,896],[1154,868],[1201,844]],[[1051,957],[1097,938],[1154,916],[1177,907],[1190,900.6],[1220,893]]]
blue=[[[1135,989],[1208,1012],[1228,968]]]
for pts in blue:cv2.polylines(road,[np.round(np.array(pts)*2).astype(np.int32)],False,0,18)
for pts in red:cv2.polylines(road,[np.round(np.array(pts)*2).astype(np.int32)],False,255,14)
# Vectorize the white road surfaces, keep holes for planted islands/structures.
cc,hh=cv2.findContours(road,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE);roads=[]
for i,c in enumerate(cc):
 if hh[0][i][3]>=0 or cv2.contourArea(c)<120:continue
 p=cv2.approxPolyDP(c,1,True)[:,0,:]/2
 if len(p)<3:continue
 holes=[];j=hh[0][i][2]
 while j>=0:
  if cv2.contourArea(cc[j])>30:
   hp=cv2.approxPolyDP(cc[j],1,True)[:,0,:]/2
   if len(hp)>=3:holes.append(hp.tolist())
  j=hh[0][j][0]
 roads.append({'outer':p.tolist(),'holes':holes})
# Stadium contour and its central field are traced from their own colours, not an old nine-point block.
track=((r>185)&(b>185)&(r-g>2)&(b-g>2)&(r-g<20)&(b-g<20)).astype(np.uint8)*255
roi=np.zeros_like(track);cv2.rectangle(roi,(945*2,640*2),(1120*2,875*2),255,-1);track=cv2.bitwise_and(track,roi);track=cv2.morphologyEx(track,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
tc,th=cv2.findContours(track,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE);sports=[]
for i,c in enumerate(tc):
 if th[0][i][3]>=0 or cv2.contourArea(c)<4000:continue
 p=cv2.approxPolyDP(c,2,True)[:,0,:]/2;holes=[];j=th[0][i][2]
 while j>=0:
  if cv2.contourArea(tc[j])>1000:holes.append((cv2.approxPolyDP(tc[j],2,True)[:,0,:]/2).tolist())
  j=th[0][j][0]
 sports.append({'name':'运动场跑道与内场','outer':p.tolist(),'holes':holes})
# Separate the track ring from the adjoining courts; its inner field supplies the true curved boundary.
if sports:
 holes=[h for t in sports for h in t['holes']]
 if holes:
  field=max((Polygon(h).buffer(0) for h in holes),key=lambda z:z.area).buffer(1).buffer(-1)
  stadium=field.buffer(7,quad_segs=12)
  sports=[{'name':'运动场跑道与内场','outer':list(map(list,list(stadium.exterior.coords)[:-1])),'holes':[list(map(list,list(field.exterior.coords)[:-1]))]}]
D={'revision':'F01','stage':'俯视占地复核，待用户确认','coordinateSystem':{'width':2048,'height':1143,'north':'up'},'basis':'用户初始校园图约束布局及构件；高分辨2023同版校园图仅辅助读取细边线，不沿用旧手绘矩形；红蓝修改单独记录','buildings':shapes,'roadSurfaces':roads,'campuses':base['campuses'],'spaces':base['spaces'],'sports':sports,'passages':passages,'redAdditions':red,'blueRemovals':blue}
(out/'轮廓与道路.json').write_text(json.dumps(D,ensure_ascii=False,separators=(',',':')))
print('source components',len(shapes),'road surfaces',len(roads),'identified',len(set(i for s in shapes for i in s['oldIDs'])))
