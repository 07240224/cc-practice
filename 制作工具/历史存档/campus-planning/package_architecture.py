from pathlib import Path
import json,re
O=Path('/workspace/cc-practice/校园建筑版');r=Path('/workspace/scratch/campus-planning/runtime_ortho.js').read_text()
start=r.index('textures.lectureFront=');end=r.index('\nfunction schoolBuilding',start)
r=r[:start]+ 'textures.buildingroof=textures.roof.clone();textures.buildingroof.repeat.set(6,6);textures.buildingroof.needsUpdate=true;}\n'+r[end:]
start=r.index('function schoolBuilding');end=r.index('function wallLine',start);r=r[:start]+Path('/workspace/scratch/campus-planning/architecture_models.js').read_text()+'\n'+r[end:]
r=r.replace('Math.hypot(b.x-a.x,b.y-a.y)/.5','Math.hypot(b.x-a.x,b.y-a.y)/.15')
r=r.replace('0xfffae7,0x85946c,1.4','0xfffbf1,0x9ba7a4,1.8').replace('0xfff1ce,2.0','0xfff4e4,2.0')
r=r.replace('const shared=new Set(Object.values(textures))','const shared=new Set([...Object.values(textures),...architectureCache.values()])')
r=r.replace('function corridor(){const b=DATA.bridge,','function corridor(b=DATA.bridge){const ' ).replace('for(const p of m.site)wallLine','for(const p of m.site)wallLine')
r=r.replace("for(const b of DATA.models){if(b.kind==='painted')schoolBuilding(b);else calibrationStudent(b)}corridor()",'for(const bridge of DATA.bridges)corridor(bridge)')
r=r.replace("for(const p of m.site)wallLine", "for(const b of DATA.models.filter(b=>b.map===id))architecturalBuilding(b); for(const p of m.site)wallLine")
start=r.index('function stairHeight()');end=r.index('\nfunction render()',start)
r=r[:start]+'''function stairHeight(){for(const b of DATA.models.filter(b=>b.map===mapId&&!['bookstore','finance','gym','cainiao','dormcourt','watertower','oldgate'].includes(b.kind))){const a=T.MathUtils.degToRad(b.rotation),dx=player.x-b.center[0],dz=player.y-b.center[1],x=Math.cos(a)*dx-Math.sin(a)*dz,z=Math.sin(a)*dx+Math.cos(a)*dz;const entries=b.entries||[{x:b.entryLocal[0],z:b.entryFace??b.depth/2,porch:b.porch}];for(const e of entries){const zz=z-e.z;if(Math.abs(x-e.x)<3&&zz>=-.025&&zz<2.325)return zz<1.025?.36:zz<1.675?.24:.12}}return 0}'''+r[end:]
start=r.index('function nearby()');end=r.index('\nfunction frame',start);r=r[:start]+"function nearby(){return '校园步道'}"+r[end:]
r=r.replace("let s=label(r.name,10);s.position.set(r.center[0],.2,r.center[1]);g.add(s)","")
r=r.replace("building:id=>DATA.models.find(s=>s.id===id)","building:id=>DATA.models.find(s=>s.id===id)||DATA.models.find(s=>s.id===DATA.identities.find(a=>a.id===id)?.model),buildings:()=>DATA.models,inspect:(id,view=90)=>{let b=DATA.models.find(s=>s.id===id)||DATA.models.find(s=>s.id===DATA.identities.find(a=>a.id===id)?.model);if(b.map!==mapId)setMap(b.map);player.x=b.arrival[0];player.y=b.arrival[1];path=[];overview=false;zoom=80/view;follow.set(player.x,.5,player.y);updateCamera(true);render()},stats:()=>({meshes:occluderMeshes.length,materials:revealMaterials.length,textures:renderer.info.memory.textures,geometries:renderer.info.memory.geometries,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles})")
r=r.replace("document.querySelector('#reset').onclick", "document.querySelector('#map-w').onclick=()=>setMap('wuchuan');document.querySelector('#map-g').onclick=()=>setMap('guoding');document.querySelector('#reset').onclick")
(O/'运行脚本.js').write_text(r)
a=json.loads(Path('/workspace/scratch/campus-planning/sample-assets.json').read_text());assets={k:a[k] for k in ['grass','student']};frames=json.dumps(a['frames']);data=(O/'场景数据.json').read_text();three=(O/'vendor/three.min.js').read_text()
old=Path('/workspace/cc-practice/正交可行走底图/打开校园底图.html').read_text();html=old[:old.index('<script>')];html=html.replace('财大校园 · 正交可行走底图','财大校园 · 校园建筑版').replace('三教 · 梯教 · 连廊下通路','两座独立校区 · 沿道路自由行走').replace('第三教学楼门前','校园步道').replace('建筑预留区','落位辅助线').replace('<button id="reset">','<button id="map-w">武川</button><button id="map-g">国定 · 武东</button><button id="reset">')
html=html.replace('<button id="slots">落位辅助线</button>','<button id="slots" hidden>落位辅助线</button>')
html+='<script>'+three+'</script><script>const DATA='+data+';const ASSETS='+json.dumps(assets)+';const FRAMES='+frames+';</script><script>'+r+'</script></html>'
(O/'打开校园.html').write_text(html);print('html',len(html.encode()),'models',len(json.loads(data)['models']))
