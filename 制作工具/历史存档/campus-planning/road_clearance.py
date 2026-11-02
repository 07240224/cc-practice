import json,sys,math
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/地图规划/全校布局规划.json');d=json.loads(p.read_text());B={b['id']:b for b in d['buildings']};R={r['id']:r for r in d['roads']}
def rect(id,x,y,w,h,a=0):
 r=math.radians(a);B[id]['polygon']=[[round(x+u*math.cos(r)-v*math.sin(r),1),round(y+u*math.sin(r)+v*math.cos(r),1)] for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
rect('W09',628,449,79,55,-21);rect('W10',714,449,50,37,-21);rect('D16',870,656,52,20,-25)
B['W06']['polygon']=[[589,722],[706,678],[721,754],[614,788]]
R['R-WC']['width']=24;R['R-GD']['points']=[[1658,208],[1781,455],[1873,646],[1941,773]]
R['W1']['points']=[[230,687],[390,625],[540,565],[700,500],[737,485]]
R['W2']['points']=[[390,625],[424,662],[460,751]]
R['W3']['points']=[[503,435],[515,494],[542,560],[570,615],[598,678],[609,699]]
R['W4']['points']=[[660,423],[677,469],[693,489],[710,543],[736,619],[770,696],[791,716]]
R['W5']['points']=[[609,699],[562,725],[593,791],[620,799],[741,748],[790,725]]
R['W6']['points']=[[609,699],[728,650],[747,650]]
R['G1']['points']=[[936,363],[1095,408],[1210,491],[1518,491]]
R['G4']['points']=[[1390,286],[1390,404],[1367,425],[1351,480]]
R['G5']['points']=[[1572,285],[1572,396],[1605,477],[1605,541],[1598,550],[1597,608],[1767,616]]
R['D4']['points']=[[959,905],[1009,949],[1038,962],[1126,992],[1202,1020]]
R['D5']['points']=[[1038,962],[1119,980],[1213,956]]
q=d['campuses'][1]['polygon'];q[q.index([1328,642])]=[1332,649]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ROAD INTERSECTIONS')
for r in d['roads']+[{**c,'width':6} for c in d['connections']]:
 line=LineString(r['points']).buffer(r['width']/2)
 hits=[(b['id'],round(line.intersection(Polygon(b['polygon'])).area,1)) for b in d['buildings'] if line.intersection(Polygon(b['polygon'])).area>.1]
 if hits:print(r['id'],hits)
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);print('OUTSIDE')
for b in d['buildings']:
 q=Polygon(b['polygon']);ratio=q.difference(site).area/q.area
 if ratio>.01:print(b['id'],round(ratio,3))
