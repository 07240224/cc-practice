"""Render an inspectable road-face plan. The playable V4 files are never edited."""
from pathlib import Path
import base64, csv, hashlib, io, json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

P=Path(__file__).resolve().parents[2]
O=P/'道路俯视复核R5'
F=json.loads((P/'占地复核图/轮廓与道路.json').read_text(encoding='utf-8'))
mask=cv2.imread(str(O/'道路原色面.png'),0)
H,W=mask.shape; sx=W/2048;sy=H/1143
fontfile=str(P/'制作工具/fonts/NotoSansCJK-Regular.ttc')
views=[
 ('01-全校道路俯视核对','全校道路俯视核对',[155,210,1905,1065]),
 ('02-武川全部道路','武川片区 · 主路、支路与楼前通路',[200,330,895,830]),
 ('03-国定全部道路','国定片区 · 北部、宿舍区与东侧',[890,215,1905,685]),
 ('04-武东全部道路','武东片区 · 场馆外缘与院楼通路',[740,565,1305,1060]),
 ('05-科研三角三边','科研楼前三角 · 三边完整保留',[1257,518,1395,607]),
 ('06-教学楼连廊下通路','第一、第二教学楼 · 地面T形路与连廊下通行',[1588,375,1769,482]),
 ('07-绿叶步行街','绿叶步行街 · 浅色铺装与南北接路',[1190,442,1550,563]),
 ('08-经济学院与接站方向','武川东北 · 经济学院转折与接站方向',[663,340,888,551]),
]

# Full-resolution contours: only exactly collinear pixel runs are compressed.
cc,hierarchy=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
faces=[]
for i,c in enumerate(cc):
    if hierarchy[0][i][3]>=0:continue
    if len(c)<3:continue
    outer=[[round(float(x)/sx,4),round(float(y)/sy,4)] for x,y in c[:,0,:]]
    holes=[];child=hierarchy[0][i][2]
    while child>=0:
        h=cc[child]
        if len(h)>=3:holes.append([[round(float(x)/sx,4),round(float(y)/sy,4)] for x,y in h[:,0,:]])
        child=hierarchy[0][child][0]
    faces.append(dict(id=f'FACE-{len(faces)+1:03}',outer=outer,holes=holes))
passages=[
 dict(id='LOWER-12-W',name='一二教西侧连廊下地面通行',points=[[1620,430],[1645,430]],width=4,layer='ground',meaning='西侧上层连廊下东西接续，两端连接原白路'),
 dict(id='LOWER-12',name='一二教连廊下地面通行',points=[[1682,430],[1720,430]],width=4,layer='ground',meaning='独立地面层，屋面不作道路'),
 dict(id='LOWER-3',name='梯教—三教连廊下地面通行',points=[[1177,907],[1190,900.6],[1220,893]],width=4,layer='ground',meaning='下层通行定位标记；不把上层连廊轮廓填成新街道'),
]
data={'revision':'ROAD-REVIEW-R5','stage':'俯视道路核对，待用户确认后再重建可玩底图',
      'coordinateSystem':dict(width=2048,height=1143,sourceWidth=W,sourceHeight=H,north='up'),
      'source':'校方2023高清图作描边辅助；对话初始图与用户批注决定采用关系；2020校方图作旧版交叉核对。',
      'roadFaces':faces,'groundPassages':passages,
      'priorAnnotations':dict(redAdditions=F['redAdditions'],blueRemovals=F['blueRemovals']),
      'rules':['不用V4中心线','不按连通块面积删路','不对道路整体作闭运算或平滑简化','浅色铺装单列','建筑内白块逐项排除，架空连廊不当楼体堵路']}
(O/'道路面数据.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')

base=Image.open(O/'核对图底层.png').convert('RGB')
anchors=[a for a in F['nameAnchors'] if a['id'] in ['W01','W06','W08','W10','W11','W12','W13','W14','G09','G17','G21','G22','G43','G44','D01','D03','D08','D09','G42']]
def dashed(draw,points,fill,width,dash=12):
    import math
    for a,b in zip(points,points[1:]):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        for k in np.arange(0,length,dash*1.7):
            v=min(k+dash,length)
            draw.line([(a[0]+dx*k/length,a[1]+dy*k/length),(a[0]+dx*v/length,a[1]+dy*v/length)],fill=fill,width=width)

for file,title,box in views:
    x0,y0,x1,y1=box
    width=3200 if file.startswith('01') else 2200
    scale=(width-100)/(x1-x0);maph=round((y1-y0)*scale)
    image=Image.new('RGB',(width,maph+238),'#f3f5ee');q=ImageDraw.Draw(image)
    q.text((50,29),'上海财经大学  /  道路逐面核对 R5',font=ImageFont.truetype(fontfile,22),fill='#6b7a68')
    q.text((50,69),title,font=ImageFont.truetype(fontfile,40),fill='#29463b')
    crop=base.crop((round(x0*sx),round(y0*sy),round(x1*sx),round(y1*sy)))
    crop=crop.resize((width-100,maph),Image.Resampling.LANCZOS);image.paste(crop,(50,143))
    q=ImageDraw.Draw(image);pt=lambda p:(50+(p[0]-x0)*scale,143+(p[1]-y0)*scale)
    labelsize=max(15,min(28,round(scale*7.5)))
    label=ImageFont.truetype(fontfile,labelsize)
    if not file.startswith('05'):
        for a in anchors:
            if x0<a['x']<x1 and y0<a['y']<y1:
                name='21/22连体楼' if a['id']=='W13' else a['name'][:11]
                if a['id']=='W14':continue
                q.text(pt([a['x'],a['y']]),name,font=label,fill='#3b4a40',anchor='mm')
    for passage in passages:
        if all(x0<p[0]<x1 and y0<p[1]<y1 for p in passage['points']):
            dashed(q,[pt(p) for p in passage['points']],'#288b91',max(2,round(scale*.65)),max(8,round(scale*2)))
    if file.startswith('05'):
        note=ImageFont.truetype(fontfile,27)
        for text,at in [('北边：宿舍南侧道路',[1317,536]),('西斜边',[1279,566]),('东斜边',[1352,568])]:
            q.text(pt(at),text,font=note,fill='#31534b',anchor='mm',stroke_width=3,stroke_fill='#f3f5ee')
        q.text(pt([1319,558]),'三角绿岛',font=note,fill='#31534b',anchor='mm')
    footer=143+maph+26
    q.rectangle([50,footer+2,76,footer+20],fill='#fffffa',outline='#85917f')
    q.text((88,footer-1),'道路及明确步行铺装',font=ImageFont.truetype(fontfile,20),fill='#445641')
    q.rectangle([370,footer+2,396,footer+20],fill='#b2ab98')
    q.text((408,footer-1),'建筑定位轮廓',font=ImageFont.truetype(fontfile,20),fill='#445641')
    q.text((650,footer-1),'青虚线：连廊下地面通行',font=ImageFont.truetype(fontfile,20),fill='#288b91')
    q.text((50,footer+33),'描边辅助：校方2023高清图；布局以对话初始参考图及批注为准。本轮只出俯视核对图。',font=ImageFont.truetype(fontfile,18),fill='#7d8775')
    image.save(O/(file+'.png'),optimize=True)

def uri(path):
    suffix='jpeg' if path.suffix.lower() in ['.jpg','.jpeg'] else 'png'
    return 'data:image/'+suffix+';base64,'+base64.b64encode(path.read_bytes()).decode()
labels=''.join(f'<text x="{a["x"]}" y="{a["y"]}" text-anchor="middle" font-size="8" fill="#344c3e">{a["name"][:11]}</text>' for a in anchors if a['id']!='W14')
pass_svg=''.join('<polyline points="'+' '.join(f'{x},{y}' for x,y in a['points'])+'" fill="none" stroke="#288b91" stroke-width="1.3" stroke-dasharray="3 2"/>' for a in passages)
annot_svg=''.join('<polyline points="'+' '.join(f'{x},{y}' for x,y in line)+'" fill="none" stroke="'+color+'" stroke-width="3"/>' for color,lines in [('#bf644d',F['redAdditions']),('#439bb5',F['blueRemovals'])] for line in lines)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>财大 · 道路俯视核对 R5</title><style>
*{box-sizing:border-box}body{margin:0;background:#e2e8e1;color:#29463b;font:15px/1.5 system-ui}header{background:#f8faf5;padding:18px 24px;border-bottom:1px solid #cbd5c6;display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap}h1{font-size:23px;margin:0}header p{margin:4px 0 0;font-size:13px;color:#73816c}nav{display:flex;gap:6px;flex-wrap:wrap}button{background:#f9fbf6;color:#3b614e;border:1px solid #b9c9b3;border-radius:5px;padding:8px 12px;cursor:pointer}button.active{color:white;background:#426b54;border-color:#426b54}main{height:calc(100vh - 155px);position:relative}svg{display:block;width:100%;height:100%;touch-action:none;cursor:grab}svg:active{cursor:grabbing}.tools{position:absolute;right:22px;top:18px;background:#f9fbf4ee;padding:12px;border:1px solid #c3cfbb;border-radius:7px;max-width:315px;box-shadow:0 8px 24px #3f5b3e10}.tools button{margin:3px;padding:6px 9px}.tools p{font-size:12px;color:#73816c;margin:5px}.foot{height:55px;background:#f8faf5;border-top:1px solid #cbd5c6;padding:14px 24px;font-size:12px;color:#73816c}.legend{background:#fffffa;border:1px solid #a4b19c;display:inline-block;width:18px;height:10px;margin-right:6px}@media(max-width:700px){.tools{top:8px;right:8px;max-width:250px}main{height:calc(100vh - 220px)}.foot{height:auto}h1{font-size:20px}}
</style><header><div><h1>上海财经大学 · 道路俯视核对 R5</h1><p>完整路面与支路逐面整理 · 三角三边保留 · 不沿用V4中心线</p></div><nav>
<button data-view="all" class="active">全校</button><button data-view="west">武川</button><button data-view="east">国定</button><button data-view="south">武东</button><button data-view="triangle">科研前三角</button><button data-view="teaching">一二教</button><button data-view="greenleaf">绿叶步行街</button></nav></header><main>
<svg id="map" xmlns="http://www.w3.org/2000/svg" viewBox="155 210 1750 855"><defs><filter id="highlight"><feFlood flood-color="#dd7448"/><feComposite in2="SourceAlpha" operator="in"/></filter></defs>
<image href="__BASE__" width="2048" height="1143"/><image id="ref" href="__SOURCE__" width="2048" height="1143" opacity="0"/><image id="road" href="__ROADS__" width="2048" height="1143" opacity="0"/>
<g id="names">__LABELS__</g><g id="passages">__PASSAGES__</g><g id="annotations" display="none">__ANNOT__</g></svg>
<div class="tools"><div><button id="clean" class="active">道路图</button><button id="reference">高清底稿</button><button id="overlay">叠图核对</button></div><div><button id="names-button">名称开／关</button><button id="annotation-button">前次红补蓝删</button></div><p><span class="legend"></span>白色：道路与明确步行铺装</p><p>青虚线：上层连廊下的地面通行</p><p>滚轮缩放 · 拖动平移 · 分区按钮定位</p><p>来源：校方2023高清辅助图，旧版用2020校方图交叉核对；采用关系以对话初图和批注为准。</p></div></main><div class="foot">本轮只核对俯视路网。科研前三角的北边与两条斜边均保留，内部不加穿行路。PNG分区图、道路面数据与核对清单随包提供。</div>
<script>const map=document.querySelector('#map'),views={all:[155,210,1750,855],west:[200,330,695,500],east:[890,215,1015,470],south:[740,565,565,495],triangle:[1257,518,138,89],teaching:[1588,375,181,107],greenleaf:[1190,442,360,121]};let box=views.all.slice(),drag=null;
function draw(){map.setAttribute('viewBox',box.join(' '))}for(const el of document.querySelectorAll('[data-view]'))el.onclick=()=>{box=views[el.dataset.view].slice();draw();document.querySelectorAll('[data-view]').forEach(x=>x.classList.toggle('active',x===el))};
function mode(id){document.querySelector('#ref').setAttribute('opacity',id==='clean'?0:1);document.querySelector('#road').setAttribute('opacity',id==='overlay'?.7:0);document.querySelector('#road').setAttribute('filter','url(#highlight)');for(const name of['clean','reference','overlay'])document.querySelector('#'+name).classList.toggle('active',name===id)}for(const id of['clean','reference','overlay'])document.querySelector('#'+id).onclick=()=>mode(id);
document.querySelector('#names-button').onclick=()=>{let el=document.querySelector('#names');el.style.display=el.style.display==='none'?'':'none'};document.querySelector('#annotation-button').onclick=()=>{let el=document.querySelector('#annotations');el.setAttribute('display',el.getAttribute('display')==='none'?'inline':'none')};
function world(e){let p=map.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(map.getScreenCTM().inverse())}map.onwheel=e=>{e.preventDefault();let p=world(e),factor=Math.exp(e.deltaY*.001);if(box[2]*factor<35||box[2]*factor>3000)return;box=[p.x+(box[0]-p.x)*factor,p.y+(box[1]-p.y)*factor,box[2]*factor,box[3]*factor];draw()};map.onpointerdown=e=>{drag={point:world(e),box:box.slice()};map.setPointerCapture(e.pointerId)};map.onpointermove=e=>{if(!drag)return;let p=world(e);box[0]+=drag.point.x-p.x;box[1]+=drag.point.y-p.y;draw()};map.onpointerup=()=>drag=null;map.onpointercancel=()=>drag=null;window.review={views,setView:key=>{box=views[key].slice();draw()},mode};</script></html>'''
for a,b in {'__BASE__':uri(O/'核对图底层.png'),'__SOURCE__':uri(O/'校方高清辅助参考.jpg'),'__ROADS__':uri(O/'道路面透明层.png'),'__LABELS__':labels,'__PASSAGES__':pass_svg,'__ANNOT__':annot_svg}.items():page=page.replace(a,b)
(O/'打开道路核对图.html').write_text(page,encoding='utf-8')
report=json.loads((O/'路面分类核对.json').read_text(encoding='utf-8'))
with (O/'排除对象清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f,lineterminator='\n');writer.writerow(['审查ID','参考图范围','源像素数','最大宽度(参考单位)','排除依据'])
    for row in report['excluded']:writer.writerow([row['id'],row['bbox'],row['sourcePixels'],round(row['maxWidth'],3),row['reason']])
manifest={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in O.iterdir() if p.is_file() and p.name!='文件校验.json'}
(O/'文件校验.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Rendered',len(views),'views;',len(faces),'full-resolution faces;',len(report['kept']),'retained source components')
