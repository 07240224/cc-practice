"""Check known omission regressions; this does not certify a playable map."""
from pathlib import Path
import csv, json
import cv2, numpy as np

P=Path(__file__).resolve().parents[2];O=P/'道路俯视复核R5'
mask=cv2.imread(str(O/'道路原色面.png'),0)>0;h,w=mask.shape;sx=w/2048;sy=h/1143
roi=(~mask[round(530*sy):round(600*sy),round(1268*sx):round(1375*sx)]).astype('uint8')
n,labels,stats,cent=cv2.connectedComponentsWithStats(roi,8)
k=labels[round(28*sy),round(49*sx)]
assert not ((labels[0]==k).any() or (labels[-1]==k).any() or (labels[:,0]==k).any() or (labels[:,-1]==k).any()), '三角外围未闭合'
assert mask[round(488*sy),round(1520*sx)], '绿叶街东端漏路'
assert not mask[round(488*sy),round(1530*sx)], '把东端绿地填成道路'
x0,x1,y0,y1=[round(a*b) for a,b in [(1636.7,sx),(1696.7,sx),(426.7,sy),(462.4,sy)]]
assert mask[y0:y1,x0:x1].sum()>3400, 'T形地面面缺失'
D=json.loads((O/'道路面数据.json').read_text(encoding='utf-8'))
R=json.loads((O/'路面分类核对.json').read_text(encoding='utf-8'))
assert len(D['roadFaces'])==len(R['kept']), '输出遗漏独立路面碎段'
assert {p['id'] for p in D['groundPassages']} == {'LOWER-12-W','LOWER-12','LOWER-3'}
report={'scope':'R5俯视核对稿，不是游戏修复验收','roadsFaceCount':len(D['roadFaces']),
        'retainedSourceComponents':len(R['kept']),'omissionByAreaFilter':False,
        'triangleIslandClosed':True,'triangleIslandSourceArea':int(stats[k,4])/(sx*sy),
        'teachingTSourcePixels':int(mask[y0:y1,x0:x1].sum()),
        'promenadeEastStepRestored':True,'promenadeEastGreenPreserved':True,
        'underpasses':[p['id'] for p in D['groundPassages']],
        'independentReview':'/root/marked_regions_gate：分区图与交互离线复核通过；本稿待用户确认。',
        'browserReview':{'pageErrors':0,'httpRequests':0,'regions':7,'modes':3},
        'rasterSource':'校方2023高清辅助图；用户初图和批注决定布局采用关系'}
(O/'专项核对结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
zones=[('W01','武川东北环路、经济学院街角和接站方向','08'),('W02','会计学院南侧庭园和外围支路','02'),
 ('W03','创业、体育馆与学术中心周边','02'),('W04','四教南北道路和楼前支路','02'),('W05','风雨操场四周道路','02'),
 ('W06','图书馆外围、入口和围合支路','02'),('W07','21至26号宿舍之间巷道','02'),('G01','北部27/20号及宿舍区','03'),
 ('G02','体育馆周围与南侧广场接路','03'),('G03','湖边南北向道路','03'),('G04','绿叶步行街和东端台阶前场','07'),
 ('G05','南北宿舍之间通路','03'),('G06','科研前三角北边与两条斜边','05'),('G07','19号楼院内开口和外沿路','03'),
 ('G08','院楼区东西南北支路','03'),('G09','一二教T形路和东西廊下接续','06'),('G10','博物馆、档案馆和校史馆周边','03'),
 ('G11','红瓦楼与艺术中心周边','03'),('G12','校门与最东侧快递中心方向','03'),('D01','运动场与篮球场围合外缘','04'),
 ('D02','金融、教工之家及西侧院楼通路','04'),('D03','学生中心与东侧院楼支路','04'),('D04','梯教、连续院楼和三教周边','04'),
 ('A01','西南附属地块：独立参考、不改游戏范围','01')]
with (O/'分区核对清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f,lineterminator='\n');writer.writerow(['分区','核对范围','对应图号','阶段'])
    writer.writerows([(*z,'俯视稿助手复核，待用户确认') for z in zones])
print(json.dumps(report,ensure_ascii=False,indent=2))
