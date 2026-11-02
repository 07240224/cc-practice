import json
from pathlib import Path
p=Path('/workspace/cc-practice/地图规划/地面底图R3/地面底图数据.json');d=json.loads(p.read_text());B={b['id']:b for b in d['buildings']};R={r['id']:r for r in d['roads']}
R['R-GD']['points']=[[1673,208],[1798,455],[1890,646],[1958,773]];R['R-GD']['width']=26
B['G50']['polygon']=[[1828,611],[1841,605],[1856,635],[1847,640],[1844,635],[1835,640],[1825,620]]
R['W7']['width']=5
R['G1']['width']=7;R['G1']['points']=[[936,363],[1095,408],[1210,489],[1230,489],[1518,489]]
R['G4']['points']=[[1390,292],[1386,402],[1360,434],[1351,480],[1351,489]]
R['G9']['points']=[[1390,292],[1572,292],[1668,292]]
R['G10']['points']=[[1220,291],[1220,239],[1365,239],[1365,292],[1390,292]]
R['G11']['width']=6
B['G25']['polygon']=[[1383,411],[1443,411],[1443,437],[1383,437]]
for pt in B['G24']['polygon']:
 if pt[0]==1450:pt[0]=1451
R['G16']['points']=[[1233,535],[1272,562],[1430,562],[1440,562],[1520,562],[1600,562]];R['G16']['width']=6
for pt in B['G41']['polygon']:
 if pt[1]==562:pt[1]=567
R['G17R']['points']=[[1363,489],[1363,550],[1337,574],[1322,583],[1297,563],[1272,562]];R['G17R']['width']=6
R['G19R']['points']=[[1155,546],[1130,546],[1080,568],[1054,582]]
R['G22R']['points']=[[1822,626],[1819,620]];R['G22R']['name']='菜鸟前场连接';R['G22R']['width']=5
R['G23R']['points']=[[1520,562],[1520,532],[1518,489],[1520,434],[1447,434]];R['G23R']['width']=6
# The west and east halves of the southern precinct join south of the teaching block.
d['roads'].append({'id':'D7','name':'三教南侧道路接续','points':[[1202,1008],[1208,1015]],'width':7,'kind':'internal','status':'连接既有东西道路节点'})
d['forecourts'][0]['polygon']=[[1809,615],[1820,611],[1828,629],[1818,634]]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
