import json,sys,math
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
P=Path('/workspace/cc-practice/地图规划/全校布局规划.json');d=json.loads(P.read_text())
def rect(id,x,y,w,h,a=0):
 b=next(b for b in d['buildings'] if b['id']==id);r=math.radians(a);b['polygon']=[[round(x+u*math.cos(r)-v*math.sin(r),1),round(y+u*math.sin(r)+v*math.cos(r),1)] for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
for row in [('D01',860,730,75,51,-25),('D02',858,778,69,26,-25),('D03',935,801,31,80,-25),('D04',910,881,68,40,-25),('D05',1016,882,34,32,-25),('D06',1068,887,84,32,-25),('D07',1147,848,88,27,-25),('D08',1188,878,40,35,-25),('D09',1156,940,92,34,-25),('D10',1104,961,47,31,-25),('D11',1209,770,53,28,-25),('D12',1228,803,53,28,-25),('D13',1253,849,55,25,-25),('D14',1197,739,53,25,-25),('D15',1127,1005,174,18,21),('D16',865,652,62,25,-25),('W12',783,478,68,43,-21),('W18',784,628,45,48,-21),('W21',537,769,50,25,-21)]:rect(*row)
# Continuous east site is split into two production zones, without inventing a wall.
d['campuses'][1]['polygon']=[[902,241],[919,226],[1631,224],[1654,244],[1863,650],[1511,598],[1501,580],[1450,580],[1440,642],[1364,643],[1362,680],[1339,672],[1328,642],[1236,700],[1225,715],[1155,735],[1110,655],[1092,579],[1040,596],[1024,587],[1008,560],[1023,548],[996,481],[936,489],[902,462],[925,365]]
d['campuses'][2]['polygon']=[[848,646],[1024,587],[1040,596],[1092,579],[1110,655],[1155,735],[1225,715],[1285,856],[1234,878],[1243,960],[1210,1053],[752,888],[793,785]]
d['campuses'].append({'id':'A','name':'西南附属地块','subtitle':'与主片区隔路，保留独立边界','color':'#a28780','polygon':[[177,711],[210,709],[237,727],[178,858],[170,784]],'view':[145,680,135,205]})
d['buildings'].append({'id':'A01','name':'国际文化交流学院','zone':'A','polygon':[[188,736],[220,747],[191,815],[178,808]],'source':'archive2023','stage':'平面占地','entranceStage':'实景门位核对阶段','note':'位于武东路288号入口西南侧的独立附属地块'})
next(s for s in d['spaces'] if s['id']=='D-COURTS')['polygon']=[[1041,605],[1066,594],[1150,762],[1129,771]]
r=d['roads'][1];r['points']=r['points'][1:];d['roads'].append({'id':'R-GQ','name':'国权北路','points':[[855,52],[863,201]],'width':24,'kind':'external'})
# Internal paths are individually retraced below. They are not carried across blocks.
d['roads']=[r for r in d['roads'] if r['kind']=='external']
# Field widths here represent planning corridors, with no invented building doors.
new=[
 ('W1',[[224,676],[361,620],[541,551],[686,495],[795,447]],8),
 ('W2',[[376,422],[374,513],[421,613]],8),
 ('W3',[[518,420],[541,481],[579,568],[617,665]],8),
 ('W4',[[690,397],[719,475],[749,551],[777,624],[788,680],[771,701]],8),
 ('W5',[[244,693],[357,737],[472,780],[598,811],[772,729]],8),
 ('W6',[[576,687],[642,663],[721,634]],8),
 ('W7',[[570,603],[682,560],[724,547]],8),
 ('G1',[[936,363],[1012,385],[1125,445],[1212,487],[1431,487],[1726,487]],8),
 ('G2',[[969,281],[1220,281],[1220,301]],8),
 ('G3',[[1219,302],[1219,439],[1212,487],[1247,552],[1300,608]],8),
 ('G4',[[1390,286],[1390,404],[1381,436],[1351,480]],8),
 ('G5',[[1572,285],[1572,396],[1598,477],[1596,541],[1600,608],[1767,616]],8),
 ('G6',[[1670,294],[1726,387],[1751,479],[1800,590]],8),
 ('G7',[[1059,443],[1092,477],[1110,521],[1136,565],[1176,647],[1203,711]],8),
 ('G8',[[1203,711],[1222,707]],6),
 ('D1',[[811,711],[913,675],[981,629],[1030,611]],8),
 ('D2',[[811,711],[836,761],[874,837],[959,918],[1038,967]],8),
 ('D3',[[776,878],[917,914],[959,918],[1005,904],[1189,824]],8),
 ('D4',[[1081,611],[1112,687],[1158,779],[1190,832],[1212,882],[1228,961],[1208,1015]],8),
 ('D5',[[1038,967],[1084,949],[1218,896]],8),
 ('D6',[[1046,985],[1142,1021],[1208,1034]],8),
 ('D7',[[1212,882],[1178,904],[1099,938],[1038,967]],8)
]
for id,pts,w in new:d['roads'].append({'id':id,'name':('武川' if id[0]=='W' else '国定' if id[0]=='G' else '武东')+'片区内部通路','points':pts,'width':w,'kind':'internal'})
d['connections'][1]['points']=[[1136,565],[1176,647],[1203,711],[1222,707],[1203,741],[1190,786],[1190,832]]
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);ex=unary_union([Polygon(c['polygon']) for c in d['exclusions']])
print('BOUNDARY / EXCLUSION')
for b in d['buildings']:
 p=Polygon(b['polygon']);out=p.difference(site).area/p.area;inter=p.intersection(ex).area/p.area
 if out>.05 or inter>.01:print(b['id'],b['name'],round(out,2),round(inter,2))
print('ROAD / BUILDING')
for r in d['roads']:
 p=LineString(r['points']).buffer(r['width']/2)
 for b in d['buildings']:
  a=p.intersection(Polygon(b['polygon'])).area
  if a>1:print(r['id'],b['id'],round(a))
