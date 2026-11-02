from pathlib import Path
import json,sys,math,hashlib
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString,Point
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/占地复核图/轮廓与道路.json');d=json.loads(p.read_text());oldroad=hashlib.sha256(json.dumps(d['roadSurfaces'],sort_keys=True).encode()).hexdigest()
kept=[];removed=[]
for b in d['buildings']:
 q=Polygon(b['outer'],b.get('holes',[]))
 if not b.get('oldIDs') and q.area<140 and not b.get('upperParts') and not b.get('groundParts'):removed.append(b)
 else:kept.append(b)
d['buildings']=kept;d['ignoredSmallStructures']=removed;d['revision']='F02';d['simplificationPolicy']='忽略独立无内容的小附属建筑；保留有名称的主体、翼部、内院边界与连接构件'
for s in d['spaces']:
 if s['id']=='D-COURTS':s['polygon']=[[1042,607],[1078,594],[1152,760],[1116,776]]
track=Polygon(d['sports'][0]['outer']);court=Polygon(next(s for s in d['spaces'] if s['id']=='D-COURTS')['polygon']);q=unary_union([track,court]).minimum_rotated_rectangle.buffer(2,join_style=2)
perimeter=LineString(q.exterior.coords);gates=[]
for name,xy,width in [('西侧原有接入口',(963,718),10),('北侧原有通道接入口',(1030,607),8)]:
 g=perimeter.interpolate(perimeter.project(Point(xy)));gates.append({'name':name,'point':[g.x,g.y],'width':width,'basis':'保留原图既有通道'})
wall=perimeter.difference(unary_union([Point(g['point']).buffer(g['width']/2) for g in gates]));segments=[wall] if wall.geom_type=='LineString' else list(wall.geoms)
d['sportsEnclosure']={'name':'体育场','contains':['运动场跑道及内场','D-COURTS'],'outer':[list(x) for x in list(q.exterior.coords)[:-1]],'wallSegments':[[list(x) for x in s.coords] for s in segments],'gates':gates,'note':'跑道与篮球场作为一个整体，长方形围墙包围；学生中心前纵路在墙外'}
assert track.difference(q).area<.001 and court.difference(q).area<.001
hits=[]
for b in kept:
 area=q.intersection(Polygon(b['outer'],b.get('holes',[]))).area
 if area>.01:hits.append((b['id'],area))
assert not hits,hits
assert oldroad==hashlib.sha256(json.dumps(d['roadSurfaces'],sort_keys=True).encode()).hexdigest()
p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
(p.parent/'F02修改核对.json').write_text(json.dumps({'ignoredCount':len(removed),'ignoredIDs':[b['id'] for b in removed],'namedAnchors':len(d['nameAnchors']),'wallContainsTrackAndCourts':True,'majorBuildingIntersections':hits,'roadLayerUnchanged':True,'gates':gates},ensure_ascii=False,indent=2)+'\n')
print('ignored',len(removed),'kept',len(kept),'rectangle',d['sportsEnclosure']['outer'])
