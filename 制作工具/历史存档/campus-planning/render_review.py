from pathlib import Path
import json,base64,html
out=Path('/workspace/cc-practice/占地复核图');d=json.loads((out/'轮廓与道路.json').read_text())
def path(p):return 'M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in p)+'Z'
def rings(s):return path(s['outer'])+''.join(path(h) for h in s.get('holes',[]))
parts=['<svg xmlns="http://www.w3.org/2000/svg" id="map" viewBox="155 210 1770 865"><rect width="2100" height="1200" fill="#e6ebe7"/><defs><pattern id="excluded" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="6" height="6" fill="#dce0da"/><path d="M0 0V6" stroke="#aab7aa" stroke-width="1"/></pattern></defs>']
# Boundary/green fill only; no geometric reuse for buildings.
for c in d['campuses']:parts.append(f'<path d="{path(c["polygon"])}" fill="#c8d8ba" stroke="#8eaa8b" stroke-width=".7"/>')
for e in d.get('exclusions',[]):parts.append(f'<path d="{path(e["polygon"])}" fill="url(#excluded)" stroke="#9ba99a" stroke-width=".7"/>')
for s in d['spaces']:
 if s['kind'] in ['water','green','sport']:parts.append(f'<path d="{path(s["polygon"])}" fill="{"#a8ccd0" if s["kind"]=="water" else "#d8d0d3" if s["kind"]=="sport" else "#b6cca2"}" stroke="none"/>')

for t in d.get('sports',[]):parts.append(f'<path d="{rings(t)}" fill="#d6c4cd" stroke="#b5a0b0" stroke-width=".6" fill-rule="evenodd"/>')
parts.append('<g id="road-layer" fill="#fff" fill-rule="evenodd">')
for r in d['roadSurfaces']:parts.append(f'<path d="{rings(r)}"/>')
parts.append('</g><g id="building-layer" fill="#b0aaa0" stroke="#675f53" stroke-width=".55" fill-rule="evenodd">')
for s in d['buildings']:parts.append(f'<path data-id="{s["id"]}" d="{''.join(rings(g) for g in s['groundParts']) if s.get('groundParts') else rings(s)}"><title>{html.escape(s["name"])} · {",".join(s["oldIDs"])}</title></path>')

for b in d['buildings']:
 for u in b.get('upperParts',[]):parts.append(f'<path d="{rings(u)}" fill="none" stroke="#675f53" stroke-width=".8" stroke-dasharray="2 2"/>')
# The whole athletics facility has one rectangular wall; preserve its original access gaps.
if d.get('sportsEnclosure'):
 e=d['sportsEnclosure'];parts.append('<g id="sports-wall" fill="none" stroke-linecap="butt" stroke-linejoin="miter">')
 for line in e['wallSegments']:
  linepath='M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in line)
  parts.append(f'<path d="{linepath}" stroke="#536d54" stroke-width="2.5"/><path d="{linepath}" stroke="#c9d2b5" stroke-width=".8"/>')
 for g in e['gates']:
  x,y=g['point'];parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="1.8" fill="#fffdf1" stroke="#536d54" stroke-width=".7"><title>{g["name"]}</title></circle>')
 parts.append('</g>')
parts.append('</g><g id="edits" fill="none" stroke-linejoin="round" stroke-linecap="round" style="display:none">')
for pts in d['redAdditions']:parts.append(f'<path d="M'+ 'L'.join(f'{x},{y}' for x,y in pts)+'" stroke="#d65b49" stroke-width="3"/>')
for pts in d['blueRemovals']:parts.append(f'<path d="M'+ 'L'.join(f'{x},{y}' for x,y in pts)+'" stroke="#2f9fc4" stroke-width="3" stroke-dasharray="4 3"/>')
parts.append('</g><g id="passages" fill="none" stroke="#4f827c" stroke-width="1" stroke-dasharray="2 2">')
for p in d['passages']:parts.append('<path d="M'+'L'.join(f'{x},{y}' for x,y in p['points'])+'"/>')
parts.append('</g><g id="labels" fill="#384537" stroke="#f9faf0" stroke-width="2" paint-order="stroke" font-size="10" text-anchor="middle">')
parts.append('<text x="1038" y="750" font-size="13" font-weight="600">体育场</text><text x="1038" y="765" font-size="9">跑道＋篮球场统一围墙</text>')
seen=set()
for a in d['nameAnchors']:
 name=a['name'].replace(' / ','／');seen.add(a['id']);parts.append(f'<text x="{a["x"]:.2f}" y="{a["y"]:.2f}">{html.escape(name)}</text>')
parts.append('</g></svg>');svg=''.join(parts);(out/'俯视占地图.svg').write_text(svg)
ref='data:image/jpeg;base64,'+base64.b64encode(Path('/workspace/scratch/map-review/sufe-official-map.jpg').read_bytes()).decode()
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>校园占地与道路 · 待确认稿</title><style>*{box-sizing:border-box}body{margin:0;background:#e6ebe7;color:#354a3b;font:14px 'Microsoft YaHei','Noto Sans CJK SC',sans-serif}header{height:90px;padding:18px 25px;background:#f9fbf5;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #c4d1bf}h1{font-size:24px;margin:0}header p{font-size:12px;margin:5px 0;color:#75856d}nav{display:flex;gap:6px;flex-wrap:wrap}button{padding:9px 12px;background:#f8faf5;border:1px solid #acbfa5;border-radius:4px;color:#476344;cursor:pointer}button.on{background:#557953;color:white}main{height:calc(100vh - 144px);position:relative;overflow:hidden}svg{width:100%;height:100%;display:block;touch-action:none;cursor:grab}footer{height:54px;padding:16px 25px;background:#f9fbf5;display:flex;justify-content:space-between;font-size:12px;color:#72826a}#source{opacity:0;pointer-events:none}body.compare #source{opacity:.6}body.compare #building-layer{fill:none;stroke:#e35c43;stroke-width:.9}body.compare #road-layer{fill:#ffffff20;stroke:#3e91b8;stroke-width:.4}body.compare #labels{display:none}body.nonames #labels{display:none}#status{position:absolute;bottom:20px;left:20px;background:#fffff2ee;padding:10px 15px;border:1px solid #c3cfba;font-size:12px}</style><header><div><h1>校园建筑占地与道路 · F02 待确认稿</h1><p>北向朝上 · 楼体轮廓 / 内院 / 连接件 / 连续道路</p></div><nav><button data-view="all">全校</button><button data-view="west">武川</button><button data-view="north">国定北部</button><button data-view="east">国定东部</button><button data-view="south">武东</button><button id="compare">参考叠合</button><button id="names">名称开关</button><button id="changes">红蓝修订</button></nav></header><main>'''+svg.replace('<g id="road-layer"',f'<image id="source" x="0" y="0" width="2048" height="1143" href="{ref}"/><g id="road-layer"')+'''<div id="status">白色：道路与前场　灰褐：主体建筑　深绿线：体育场围墙</div></main><footer><span>本轮只核对俯视占地；确认后再制作游戏地面与建筑。</span><span>拖动平移 · 滚轮缩放 · 点击构件查看名称</span></footer><script>
const views={all:[155,210,1770,865],west:[200,330,700,510],north:[900,220,830,340],east:[1200,290,720,400],south:[750,575,550,490]},map=document.querySelector('svg');let box=views.all.slice(),drag=null;function draw(){map.setAttribute('viewBox',box.join(' '))}document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{box=views[b.dataset.view].slice();draw()});document.querySelector('#compare').onclick=()=>{document.body.classList.toggle('compare');document.querySelector('#status').textContent=document.body.classList.contains('compare')?'叠合参照：工作区2023高清同版图辅助辨读；布局与构件以你上传的初始图为准':'白色：道路与前场　灰褐：主体建筑　深绿线：体育场围墙'};document.querySelector('#names').onclick=()=>document.body.classList.toggle('nonames');document.querySelector('#changes').onclick=()=>{let g=document.querySelector('#edits');g.style.display=g.style.display==='none'?'':'none'};function point(e){let p=map.createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform(map.getScreenCTM().inverse())}map.onwheel=e=>{e.preventDefault();let p=point(e),k=e.deltaY>0?1.12:1/1.12;if(box[2]*k<90||box[2]*k>2300)return;box=[p.x-(p.x-box[0])*k,p.y-(p.y-box[1])*k,box[2]*k,box[3]*k];draw()};map.onpointerdown=e=>{drag={p:point(e),x:e.clientX,y:e.clientY};map.setPointerCapture(e.pointerId)};map.onpointermove=e=>{if(!drag)return;let p=point(e);box[0]+=drag.p.x-p.x;box[1]+=drag.p.y-p.y;draw()};map.onpointerup=e=>{if(drag&&Math.hypot(e.clientX-drag.x,e.clientY-drag.y)<4){let t=document.elementFromPoint(e.clientX,e.clientY)?.closest('[data-id]');if(t)document.querySelector('#status').textContent=t.querySelector('title').textContent}drag=null};
</script></html>'''
(out/'打开占地复核图.html').write_text(page)
print('rendered',len(seen),'named groups')
