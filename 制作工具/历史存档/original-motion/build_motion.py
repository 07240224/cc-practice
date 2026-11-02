from pathlib import Path
import json,base64,shutil,hashlib,re
O=Path('/workspace/cc-practice/校园动作继承版');B=Path('/workspace/cc-practice/校园建筑版');R=Path('/workspace/scratch/original-motion')
# This delivery contains the runnable game and this round's movement evidence, not old architectural approval sheets.
keep={'打开校园.html','运行脚本.js','场景数据.json','vendor','建筑建模.js','动作继承基线.json','原动作来源','更新内嵌版本.py'}
for p in O.iterdir():
 if p.name not in keep and p.name not in ['原动作图集.png','原动作帧表.json','动作继承说明.txt','动作继承记录.json','建筑修复方案.txt','动作验证.json','本轮独立复核.txt'] and not p.name.startswith('动作-'):
  if p.is_dir():shutil.rmtree(p)
  else:p.unlink()
meta=json.loads((R/'atlas.json').read_text());runtime=(B/'运行脚本.js').read_text();adapter=(R/'motion_adapter.js').read_text()
a=runtime.index('function reveal(');b=runtime.index('\nfunction box(',a);runtime=runtime[:a]+(R/'motion_reveal.js').read_text()+runtime[b:]
runtime=runtime.replace('else follow.lerp(target,.12)', 'else follow.lerp(target,1-Math.exp(-12*lastFrameDt))')
runtime=runtime.replace('function setMap(id,spawn){', 'function setMap(id,spawn){clearActorRevealOverlays();')
a=runtime.index('function frame(now)');b=runtime.index('\n',a)
runtime=runtime[:a]+'''let physicsAccumulator=0,lastFrameDt=1/60;
function frame(now){const elapsed=Math.min(.25,Math.max(0,(now-last)/1000||1/60));last=now;lastFrameDt=elapsed;physicsAccumulator+=elapsed;while(physicsAccumulator+1e-9>=1/60){t+=1/60;update(1/60);physicsAccumulator=Math.max(0,physicsAccumulator-1/60)}render();requestAnimationFrame(frame)}'''+runtime[b:]
a=runtime.index('function createActor()');b=runtime.index('\nfunction setMap',a);runtime=runtime[:a]+runtime[b:]
a=runtime.index('function occlusion()');b=runtime.index('\nfunction move(',a);runtime=runtime[:a]+(R/'motion_occlusion.js').read_text()+runtime[b:]
a=runtime.index('function update(dt)');b=runtime.index('\nfunction stairHeight',a);runtime=runtime[:a]+runtime[b:]
a=runtime.index('function render()');b=runtime.index('\nfunction nearby',a);runtime=runtime[:a]+runtime[b:]
a=runtime.index("addEventListener('resize'");b=runtime.index('\ncanvas.onpointerdown',a)
runtime=runtime[:a]+'''addEventListener('resize',resize);addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();keys.add(inputKey(e));if((e.code==='KeyF'||e.key.toLowerCase()==='f')&&!e.repeat)toggleBicycle();if((e.code==='KeyE'||e.key.toLowerCase()==='e')&&!e.repeat&&portalArmed&&Math.hypot(player.x-m.portal[0],player.y-m.portal[1])<4)transfer()});addEventListener('keyup',e=>keys.delete(inputKey(e)));addEventListener('blur',()=>{keys.clear();motionState.gaitStep=0;motionState.speed=0;player.frame=1});\n'''+runtime[b:]
runtime=runtime.replace("document.querySelector('#map-w').onclick", "document.querySelector('#bike').onclick=toggleBicycle;document.querySelector('#map-w').onclick")
runtime=runtime.replace("occluders:[...occlusionHits],camera:","occluders:[...occlusionHits],motion:{...motionState},speeds:MOVEMENT_SPEEDS,camera:")
runtime=runtime.replace("window.game={state:","window.game={toggleBicycle,sourceMotion:SOURCE_MOTION,state:")
# The original source constants are attached to the adapter; models/roads remain byte-identical.
runtime=runtime.replace("function createActor", "function createActor")
a=runtime.index('window.game=');runtime=runtime[:a]+'const SOURCE_MOTION='+json.dumps(meta,ensure_ascii=False,separators=(',',':'))+';\n'+adapter+'\n'+runtime[a:]
(O/'运行脚本.js').write_text(runtime)
html=(B/'打开校园.html').read_text();a=html.index('const ASSETS=')+len('const ASSETS=');b=html.index(';const FRAMES=',a);assets=json.loads(html[a:b]);assets.pop('student',None);assets['originalMotion']='data:image/png;base64,'+base64.b64encode((R/'original-motion-atlas.png').read_bytes()).decode();html=html[:a]+json.dumps(assets,separators=(',',':'))+html[b:]
a=html.rindex('<script>')+len('<script>');html=html[:a]+runtime+'</script></html>'
html=html.replace('财大校园 · 校园建筑版','财大校园 · 原动作继承版').replace('<button id="map-w">','<button id="bike">骑上自行车  F</button><button id="map-w">').replace('点击地面自动前往</span>','点击地面自动前往 · <kbd>F</kbd> 骑车 / 下车</span>')
(O/'打开校园.html').write_text(html)
shutil.copy2(R/'original-motion-atlas.png',O/'原动作图集.png');shutil.copy2(R/'atlas.json',O/'原动作帧表.json');shutil.copy2(R/'export-project/export_motion.gd',O/'原动作来源/导出工具.gd');shutil.copy2(R/'export-project/base_character.gd',O/'原动作来源/导出宿主.gd')
base=json.loads((O/'动作继承基线.json').read_text());assert hashlib.sha256((O/'场景数据.json').read_bytes()).hexdigest()==base['geometrySHA256'];assert (O/'建筑建模.js').read_bytes()==(B/'建筑建模.js').read_bytes()
record={'sourceRepo':'https://github.com/i-m-not-sufer/sufe-campus-adventure','sourceFiles':base['sourceFiles'],'atlasSHA256':hashlib.sha256((O/'原动作图集.png').read_bytes()).hexdigest(),'geometrySHA256':base['geometrySHA256'],'displacement':{'previousWalk':4.4,'walkMultiplier':3,'walk':13.2,'previousRun':8,'runMultiplier':10,'run':80,'bikeOriginalToWalk':300/112,'bike':4.4*(300/112)*3},'gait':{'order':[0,1,2,1],'stepsPerSecond':7,'idleColumn':1,'rows':['down','up','left','right']},'bicycle':{'key':'F','sourceRenderedPhases':128,'originalBodyCrop':.68,'originalCadenceRadiansPerSecond':20,'cadenceMultiplier':1,'poseEdits':False},'scope':'本轮只替换主角绘制和动作播放、继承F骑车及原体力逻辑，并调整位移速度；不修改建筑模型、地图数据、道路或建筑材质。'}
record['runtimeIntegration']={'physicsStep':1/60,'frameAccumulator':True,'maximumCatchupSeconds':.25,'cameraFollowPerSecond':12,'occlusion':'圆外保留原不透明深度；圆内单独绘制局部透明层；切图回收局部层材质。'}
(O/'动作继承记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print('motion HTML',len(html.encode()),'atlas',len((O/'原动作图集.png').read_bytes()),'geometry unchanged',base['geometrySHA256'])
