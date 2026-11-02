import json,math,sys
from pathlib import Path
sys.path.insert(0,'/tmp/campus-plan-libs')
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
p=Path('/workspace/cc-practice/地图规划/全校布局规划.json');d=json.loads(p.read_text())
def rect(id,x,y,w,h,a=0):
 b=next(b for b in d['buildings'] if b['id']==id);r=math.radians(a);b['polygon']=[[round(x+u*math.cos(r)-v*math.sin(r),1),round(y+u*math.sin(r)+v*math.cos(r),1)] for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
for row in [('W03',347,589,61,77,-23),('W13',826,503,38,25,-21),('W15',740,544,40,31,-21),('W16',805,567,42,42,-21),('W17',760,589,41,31,-21),('W18',784,628,43,45,-21),('W20',604,622,18,29,-21),('D16',866,656,56,21,-25),('G41',1480,577,70,31,0),('G42',1393,631,100,18,0)]:rect(*row)
next(b for b in d['buildings'] if b['id']=='G44')['polygon']=[[1200,633],[1266,602],[1298,663],[1228,699]]
next(b for b in d['buildings'] if b['id']=='G43')['polygon']=[[1265,603],[1295,585],[1328,648],[1298,663]]
next(b for b in d['buildings'] if b['id']=='G48')['polygon']=[[1143,670],[1182,655],[1206,706],[1196,720],[1172,732]]
# Remove a duplicated end of the southern facade block, retain a single continuous footprint.
# The west facade remains a separately identified use within the same connected building.
d['campuses'][1]['polygon']=[[902,241],[919,226],[1631,224],[1654,244],[1863,650],[1511,598],[1501,580],[1450,580],[1440,644],[1364,644],[1362,680],[1339,672],[1328,642],[1236,700],[1225,715],[1155,735],[1110,655],[1092,579],[1040,596],[1024,587],[1008,560],[1023,548],[996,481],[936,489],[902,462],[925,365]]
# The second dining hall projects south of the main boundary step.
pp=d['campuses'][1]['polygon'];i=pp.index([1501,580]);pp[i:i+2]=[[1501,580],[1501,602],[1440,602]]
# Top-down road alignment; keep the external road outside the west blocks.
next(r for r in d['roads'] if r['id']=='R-WC')['points']=[[863,201],[898,358],[900,422],[870,520],[840,605],[805,710],[780,780],[737,899],[693,1019]]
# Internal trunks are chosen from the broad white corridors on the supplied map.
paths=[
 ('W1',[[230,687],[390,625],[540,565],[700,500],[752,478]],6),
 ('W2',[[361,528],[388,616],[424,662],[460,751]],6),
 ('W3',[[503,435],[515,494],[547,560],[575,615],[598,678],[612,699]],6),
 ('W4',[[670,428],[685,458],[693,489],[710,543],[736,619],[770,696],[791,716]],6),
 ('W5',[[612,699],[562,725],[593,791],[741,750],[790,725]],6),
 ('W6',[[612,699],[728,650],[747,650]],6),
 ('W7',[[575,615],[700,563],[716,564]],6),
 ('G1',[[936,363],[1099,400],[1209,487],[1518,487]],6),
 ('G2',[[969,281],[1220,281],[1220,301]],6),
 ('G3',[[1219,302],[1219,439],[1212,487],[1233,535]],6),
 ('G4',[[1390,286],[1390,404],[1373,425],[1351,480]],6),
 ('G5',[[1572,285],[1572,396],[1605,477],[1605,541],[1600,608],[1767,616]],6),
 ('G6',[[1670,294],[1726,387],[1756,477],[1779,510]],6),
 ('G7',[[1779,510],[1730,524],[1724,603],[1767,616]],6),
 ('G8',[[1155,546],[1187,625],[1218,708]],6),
 ('D1',[[811,711],[913,675],[981,629],[1030,611]],6),
 ('D2',[[1081,611],[1112,687],[1158,779],[1189,819],[1218,880],[1228,961],[1208,1015]],6),
 ('D3',[[780,890],[864,920],[959,905],[984,892],[986,861],[1025,850],[1131,820],[1177,800]],6),
 ('D4',[[959,905],[1009,949],[1042,974],[1140,1008],[1208,1030]],6),
 ('D5',[[1042,974],[1119,1000],[1213,956]],6),
 ('D6',[[1025,850],[975,728],[913,675]],6)
]
d['roads']=[r for r in d['roads'] if r['kind']=='external']+[{'id':id,'name':('武川' if id[0]=='W' else '国定' if id[0]=='G' else '武东')+'片区主通路规划','points':pts,'width':w,'kind':'internal','status':'依图示白色通道布置的主通路；细支路进入P02逐段校核'} for id,pts,w in paths]
d['connections']=[{'id':'C01','name':'西片—南片跨路衔接规划','points':[[771,724],[794,716],[818,724]],'status':'按校门位置预留；过街点与通行方式进入通路白模核对'},{'id':'C02','name':'国定—武东内部连续步行轴','points':[[1187,625],[1218,708],[1218,739],[1189,819]],'status':'内部连续步行轴；白模阶段核对路面净宽'}]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ROAD INTERSECTIONS')
for r in d['roads']:
 line=LineString(r['points']).buffer(r['width']/2)
 hits=[(b['id'],round(line.intersection(Polygon(b['polygon'])).area)) for b in d['buildings'] if line.intersection(Polygon(b['polygon'])).area>1]
 if hits:print(r['id'],hits)
site=unary_union([Polygon(c['polygon']) for c in d['campuses']]);print('OUTSIDE')
for b in d['buildings']:
 q=Polygon(b['polygon']);ratio=q.difference(site).area/q.area
 if ratio>.03:print(b['id'],round(ratio,2))
