from pathlib import Path
import os
ROOT = Path(os.environ.get('CAMPUS_WORK_ROOT', str(Path(__file__).resolve().parents[2]))).resolve()
OUTPUT = Path(os.environ.get('CAMPUS_OUTPUT_DIR', str(ROOT / '工作输出' / '校园建筑修复版'))).resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)
from pathlib import Path
import json
O = OUTPUT
B = ROOT / '校园动作继承版'
R = Path(__file__).resolve().parent
old = (B / '运行脚本.js').read_text(encoding='utf-8')
a = old.index('// Architectural geometry.')
z = old.index('\nfunction wallLine', a)
base = (B / '建筑建模.js').read_text(encoding='utf-8').replace('function block(', 'function contextBlock(').replace('function entryCanopy(', 'function contextEntryCanopy(').replace('function architecturalBuilding(', 'function legacyArchitecturalBuilding(')
model = base + '\n' + (R / 'prototype_facades.js').read_text(encoding='utf-8')
model += '\n' + (R / 'site_features.js').read_text(encoding='utf-8')
model = model.replace('function prototypeBuilding(b){', "function prototypeBuilding(b){if(b.kind==='metro')return metroEntrance(b);")
runtime = old[:a] + model + old[z:]
runtime = runtime.replace("for(const p of m.site)wallLine([...p.outer,p.outer[0]],2.2,.35,'校区围墙');", 'mapBoundary();')
a = runtime.index('function updateCamera(')
z = runtime.index('\n', a)
runtime = runtime[:a] + (R / 'camera_view.js').read_text(encoding='utf-8') + runtime[z:]
runtime = runtime.replace('),az=T.MathUtils.degToRad(DATA.camera.azimuthFromSouth),cameraOffset=', ');let az=T.MathUtils.degToRad(DATA.camera.azimuthFromSouth);const cameraOffset=')
runtime = runtime.replace('a.bits=Uint8Array.from(atob(a.grid.data),c=>c.charCodeAt(0))', 'a.bits=Uint8Array.from(atob(a.grid.data),c=>c.charCodeAt(0));a.roadWalkPath=path2(a.roadWalkSurface);a.roadBits=Uint8Array.from(atob(a.roadGrid),c=>c.charCodeAt(0))')
runtime = runtime.replace('function findPath(start,end)', 'function findFreePath(start,end)')
a = runtime.index('function shape(')
runtime = runtime[:a] + "function validRoad(x,y){return collisionCtx.isPointInPath(m.roadWalkPath,x,y,'evenodd')}\nfunction findRoadPath(start,end){if(!validRoad(start.x,start.y)||!validRoad(end.x,end.y))return[];const bits=m.bits,walkPath=m.walkPath;try{m.bits=m.roadBits;m.walkPath=m.roadWalkPath;return findFreePath(start,end)}finally{m.bits=bits;m.walkPath=walkPath}}\nfunction findPath(start,end){const road=findRoadPath(start,end);return road.length?road:findFreePath(start,end)}\n" + runtime[a:]
runtime = runtime.replace('window.game={toggleBicycle,', 'window.game={validRoad,roadRoute:findRoadPath,walkRoadTo:(x,y)=>{path=findRoadPath({x:player.x,y:player.y},{x,y});return path.length},toggleBicycle,')
runtime = runtime.replace('camera:{type:camera.type,elevation:35,azimuth:12.5,zoom}', 'camera:{type:camera.type,elevation:35,azimuth:T.MathUtils.radToDeg(az),zoom}')
a = runtime.index('const SOURCE_MOTION=')
runtime = runtime[:a] + (R / 'camera_controls.js').read_text(encoding='utf-8') + '\n' + runtime[a:]
a = runtime.index('function stairHeight()')
z = runtime.index('\n', a)
runtime = runtime[:a] + "function stairHeight(){for(const b of DATA.models.filter(b=>b.map===mapId)){const a=T.MathUtils.degToRad(b.rotation),dx=player.x-b.center[0],dz=player.y-b.center[1],x=Math.cos(a)*dx-Math.sin(a)*dz,z=Math.sin(a)*dx+Math.cos(a)*dz;if(b.steps?.length){for(const s of b.steps){const e=s.entry,ddx=x-e.x,ddz=z-e.z,along=ddx*e.normal[0]+ddz*e.normal[1],across=ddx*e.normal[1]-ddz*e.normal[0];if(Math.abs(across)<=s.width/2&&along>=s.along0&&along<s.along1)return s.height}}else if(!['bookstore','finance','gym','cainiao','dormcourt','watertower','oldgate'].includes(b.kind)){const zz=z-(b.entryFace??b.depth/2);if(Math.abs(x-b.entryLocal[0])<3&&zz>=-.025&&zz<2.325)return zz<1.025?.36:zz<1.675?.24:.12}}return 0}" + runtime[z:]
(O / '建筑建模.js').write_text(model, encoding='utf-8', newline='\n')
(O / '运行脚本.js').write_text(runtime, encoding='utf-8', newline='\n')
html = (B / '打开校园.html').read_text(encoding='utf-8').replace('财大校园 · 原动作继承版', '财大校园 · 建筑修复版')
html = html.replace('<button id="reset">', '<button id="front-view">门前视角 V</button><button id="turn-view">转向 Q / R</button><button id="reset">').replace('遮挡时局部让出视野', 'Q / R 转向 · V 门前视角 · 遮挡时局部让出视野')
a = html.index('const DATA=') + len('const DATA=')
z = html.index(';const ASSETS=', a)
data = json.loads((O / '场景数据.json').read_text(encoding='utf-8'))
html = html[:a] + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + html[z:]
a = html.rindex('<script>') + len('<script>')
html = html[:a] + runtime + '</script></html>'
(O / '打开校园.html').write_text(html, encoding='utf-8', newline='\n')
print('runtime bytes', len(runtime.encode()), 'HTML bytes', len(html.encode()))
