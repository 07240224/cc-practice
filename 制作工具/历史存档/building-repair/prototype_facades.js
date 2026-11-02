// Measured local-coordinate facade rules. Each principal building has its own profile.
// Text is intentionally absent from the model. This file does not use whole-building photo planes.
function prototypeFacade(b,p,side=false){
 const id=b.facadeProfile,role=p.role||'',w=side?p.d:p.w,h=p.h;
 const key=['prototype-v3',id,role,w,h,p.floors,p.y,side].join(':');if(architectureCache.has(key))return architectureCache.get(key);
 const c=document.createElement('canvas');c.width=Math.min(3072,Math.ceil(w*40));c.height=Math.min(3072,Math.ceil(h*48));const q=c.getContext('2d'),frames=[];q.scale(c.width/w,c.height/h);
 const colors={research:'#a06350',academic_link:'#b9b09b',wudonglecture:'#b9ae98',finance:'#c7c7bd',statistics:'#aaa99b',activity:'#dddcd2',library:'#dedfd6',accounting:'#cfbfb0',phoenix:'#c9c3ac',economics:'#d8dcd5',teaching4:'#ded7c5',teaching1:'#e0dbca',teaching2:'#ddd6bf',guodinglecture:'#dcddd1',greenleaf_canteen:'#cbc8b5',halal_canteen:'#b49a73',third_canteen:'#a56953',sufe_cafe:'#a95e42',cainiao_station:'#d6d8ce',enterprise:'#a16d54',wuchuan_hall:'#a27b66',badminton:'#cecab8',wuchuan_pool:'#c9c3b2',exchange:'#d9d6ca',wuchuan_canteen:'#c6bba1'};
 q.fillStyle=colors[id]||'#cac8b8';q.fillRect(0,0,w,h);
 const brick=['research','academic_link','wudonglecture','statistics','activity','third_canteen','enterprise','wuchuan_hall'].includes(id),stone=id==='finance';
 if(brick||stone){const bh=stone?.8:.28,bw=stone?2.2:.7;q.strokeStyle=stone?'#72786827':'#4a342718';q.lineWidth=stone?.025:.016;for(let y=0,r=0;y<h;y+=bh,r++){q.beginPath();q.moveTo(0,y);q.lineTo(w,y);q.stroke();for(let x=-(r%2)*bw/2;x<w;x+=bw){q.beginPath();q.moveTo(x,y);q.lineTo(x,y+bh);q.stroke()}}}
 function window(x,y,ww,hh,cols=2,rows=2,frame='#b3b6aa',sill=true){
  const xx=x+ww/2-w/2,yy=p.y+h-y-hh/2;
  if(id==='library'&&!side&&p.x===-37&&Math.abs(xx)<6+ww/2&&yy-hh/2<15)return;
  for(const e of b.entrances||[]){const onFace=!side&&Math.abs(e.angle%360)<.1&&Math.abs(p.z+p.d/2-e.z)<.3;const half=e.canopy==='accounting'?9:e.canopy==='library'?4:e.canopy==='blue'?8:Math.min(3.5,e.width*.425),doorHeight=e.canopy==='accounting'?7.1:3.25;if(onFace&&Math.abs(p.x+xx-e.x)<half+ww/2&&yy-hh/2<doorHeight)return}
  frames.push({x,y,w:ww,h:hh,color:frame});
  q.fillStyle='#333e3b';q.fillRect(x-.075,y-.075,ww+.15,hh+.15);
  const g=q.createLinearGradient(x,y,x+ww*.15,y+hh);g.addColorStop(0,'#6e8586');g.addColorStop(.46,'#5e7476');g.addColorStop(1,'#354b4d');q.fillStyle=g;q.fillRect(x,y,ww,hh);
  q.fillStyle='#d9e4d417';q.fillRect(x+.07,y+.05,Math.max(.03,ww-.14),hh*.22);
  q.strokeStyle=frame;q.lineWidth=.055;q.strokeRect(x+.035,y+.035,ww-.07,hh-.07);
  for(let k=1;k<cols;k++){q.beginPath();q.moveTo(x+ww*k/cols,y);q.lineTo(x+ww*k/cols,y+hh);q.stroke()}
  for(let k=1;k<rows;k++){q.beginPath();q.moveTo(x,y+hh*k/rows);q.lineTo(x+ww,y+hh*k/rows);q.stroke()}
  if(sill){q.fillStyle='#e5e1ce';q.fillRect(x-.10,y+hh,ww+.20,.085);q.fillStyle='#303c3025';q.fillRect(x-.07,y+hh+.085,ww+.14,.12)}
 }
 function grid(bay,ratio,hratio,cols=2,offset=.18,frame){const count=Math.max(1,Math.round(w/bay)),bw=w/count,fh=h/p.floors;for(let r=0;r<p.floors;r++)for(let k=0;k<count;k++){const ww=bw*ratio,hh=fh*hratio;window((k+.5)*bw-ww/2,r*fh+fh*offset,ww,hh,cols,2,frame)}}
 function slots(count,margin=1.5){const bw=(w-margin*2)/count,top=1.2,bottom=.8;for(let k=0;k<count;k++){const ww=bw*.55,x=margin+k*bw+(bw-ww)/2;q.fillStyle='#593f36';q.fillRect(x-.08,top,ww+.16,h-top-bottom);for(let r=0;r<p.floors;r++){const fh=(h-top-bottom)/p.floors;window(x,top+r*fh+.09,ww,fh-.22,2,3,'#8f9d97',false)}}}
 if(id==='research'){
  if(role==='research-tower')slots(side?7:12,1.6);
  else {const count=Math.max(1,Math.round(w/4.8)),gap=(w-1.5)/count;for(let i=0;i<count;i++)window(.75+(i+.5)*gap-.70,.65,1.4,h-1.7,2,4,'#5b655e',false)}
 }else if(id==='academic_link'||id==='wudonglecture'){
  const n=Math.max(1,Math.round(w/(side?4.2:6.3))),bw=w/n,fh=h/p.floors;
  for(let r=0;r<p.floors;r++){for(let i=0;i<n;i++){window(i*bw+.28,r*fh+.75,bw-.56,fh*.53,4,2,'#b9bbaa');q.fillStyle='#405455';q.fillRect(i*bw+.32,r*fh+.28,bw-.64,.34)}q.fillStyle='#d1cbb8';q.fillRect(0,(r+1)*fh-.17,w,.14)}q.fillStyle='#8e5d49';q.fillRect(0,h-.9,w,.9);
 }else if(id==='statistics'){
  if(p.y===0&&p.z>0){/* Structural columns have no fake window rectangles. */}
  else {const n=Math.max(1,Math.round(w/5.0)),bw=w/n,fh=h/p.floors;for(let r=0;r<p.floors;r++)for(let i=0;i<n;i++)for(let j=0;j<2;j++)window((i+.5)*bw-1.2+j*1.35,r*fh+.55,.82,fh*.73,1,2,'#9b9f91')}
 }else if(id==='finance'){
  if(p.style!=='financecenter')grid(5.0,.50,.69,2,.17,'#adb3a4');
 }else if(id==='activity'){
  const n=Math.max(1,Math.round(w/4.2)),bw=w/n,fh=h/p.floors;for(let r=0;r<p.floors;r++)for(let i=0;i<n;i++){q.fillStyle='#a36a53';q.fillRect(i*bw+.03,r*fh,.35,fh);q.fillStyle='#b4b6a9';q.fillRect(i*bw+.39,r*fh+fh-.65,bw-.42,.42);window(i*bw+.75,r*fh+.40,bw-1.12,fh*.64,2,2,'#b5bcb1')}q.fillStyle='#a06d54';q.fillRect(0,h-.28,w,.28);
 }else if(id==='library'){
  if(p.style!=='libraryend'){const n=Math.max(1,Math.round(w/6.4)),bw=w/n,fh=h/p.floors;for(let r=0;r<p.floors;r++)for(let i=0;i<n;i++)for(let j=0;j<2;j++)window((i+.5)*bw-1.65+j*1.72,r*fh+.7,1.3,fh*.62,2,2,'#9fada5')}
 }else if(id==='accounting'){
  if(role==='accounting-upper'){const n=Math.max(1,Math.round(w/6.0)),bw=w/n,fh=h/p.floors;for(let r=0;r<p.floors;r++)for(let i=0;i<n;i++){window(i*bw+.6,r*fh+.45,bw*.54,fh*.64,2,2,'#8a9186');window(i*bw+bw*.78,r*fh+.5,.42,fh*.71,1,1,'#a0a69a')}}
  else {grid(3.8,.23,.72,1,.16,'#a7a99a');q.fillStyle='#394943';q.fillRect(0,.3,w,.65)}
 }else if(id==='phoenix'){
  grid(role==='phoenix-upper'?3.1:4.3,role==='phoenix-upper'?.46:.58,.68,2,.16,'#a7ad9e');
 }else if(id==='economics'){
  const fh=h/p.floors;if(p.w<20||side){for(let r=0;r<p.floors;r++)window(.7,r*fh+.55,w-1.4,fh*.30,Math.max(2,Math.round(w/1.5)),1,'#afb8b0',false)}else grid(5.8,.64,.52,3,.18,'#a6b0a8');
 }else if(['teaching1','teaching2','teaching4','guodinglecture'].includes(id)){
  grid(id==='teaching2'?5.4:id==='teaching4'?4.8:4.4,id==='guodinglecture'?.65:.71,.70,id==='teaching2'?4:3,.14,'#b3b8a9');
 }else if(id==='greenleaf_canteen'){
  const n=Math.max(1,Math.round(w/7.6)),bw=w/n;for(let i=0;i<n;i++){window(i*bw+.55,h/2+.5,bw-1.1,2.8,3,2,'#d0d2c4');window(i*bw+.55,.55,bw-1.1,2.9,3,1,'#d0d2c4');const xx=(i+.5)*bw,yy=1.9;q.strokeStyle='#e1dfcf';q.lineWidth=.08;q.beginPath();q.moveTo(xx,yy-1.3);q.lineTo(xx,yy+1.3);q.stroke();for(let k=0;k<3;k++){q.beginPath();q.ellipse(xx,yy-.85+k*.8,.38,.48,k%2?.65:-.65,0,Math.PI*2);q.stroke()}}
 }else if(id==='halal_canteen'){
  const n=Math.max(1,Math.round(w/8)),bw=w/n;for(let i=0;i<n;i++)window(i*bw+.6,.55,bw-1.2,2.6,4,2,'#aeb3a2');
 }else if(id==='third_canteen'){
  if(role==='canteen-solid-front'&&!side){for(let r=0;r<3;r++)window(w-2.7,r*h/3+.4,1.65,h/3-.8,2,2,'#b5b5a3')}
  else if(role!=='canteen-pier')grid(6.0,.72,.73,3,.13,'#aea893');q.fillStyle='#8f5d49';q.fillRect(0,0,w,.55);
 }else if(id==='sufe_cafe'){
  if(role==='cafe-glass')window(.08,.15,w-.16,h-.3,3,3,'#6f6660',false);
  else {q.strokeStyle='#d48c6740';q.lineWidth=.035;for(let x=.2;x<w;x+=.28){q.beginPath();q.moveTo(x,0);q.lineTo(x,h*.48);q.stroke()}window(.35,h*.50,w-.7,h*.45,Math.max(3,Math.round(w/2.6)),2,'#726b60',false)}
 }else if(id==='cainiao_station'){
  if(side)window(.8,.6,w-1.6,h-1.3,4,1,'#b6beb3');
 }else if(id==='enterprise'){
  const fh=h/p.floors,n=Math.max(1,Math.round(w/9)),bw=w/n;for(let r=0;r<p.floors;r++){for(let i=0;i<n;i++)window(i*bw+.7,r*fh+.7,bw-1.4,fh*.38,4,1,'#b0ae9e');q.fillStyle='#b9b6a5';q.fillRect(0,(r+1)*fh-.18,w,.12)}
 }else if(['badminton','wuchuan_pool','wuchuan_hall'].includes(id)){
  window(.8,1.0,w-1.6,1.7,Math.max(3,Math.round(w/2.3)),2,'#a3aaa0');
 }else grid(5.5,.60,.61,3,.20,'#abb0a0');
 const tex=new T.CanvasTexture(c);tex.userData.frames=frames;tex.colorSpace=T.SRGBColorSpace;tex.anisotropy=renderer.capabilities.getMaxAnisotropy();architectureCache.set(key,tex);return tex;
}

// Merge actual projecting jambs/sills into a few meshes rather than adding a draw call for every window.
const frameUnitGeometry=new T.BoxGeometry(1,1,1).toNonIndexed();
function recessedWindowFrames(g,p,b,front,side){
 if(b.id==='research')return;
 const groups=new Map(),add=(color,x,y,z,w,h,d)=>{if(!groups.has(color))groups.set(color,[]);groups.get(color).push({x,y,z,w,h,d})};
 for(const [face,tex]of [['front',front],['side',side]])for(const r of tex.userData.frames||[]){
  const cy=p.y+p.h-r.y-r.h/2;
  const frame=(cx,yy,ww,hh)=>{if(face==='front')add(r.color,p.x-p.w/2+cx,yy,p.z+p.d/2+.075,ww,hh,.25);else add(r.color,p.x+p.w/2+.075,yy,p.z+p.d/2-cx,.25,hh,ww)};
  frame(r.x-.045,cy,.09,r.h+.16);frame(r.x+r.w+.045,cy,.09,r.h+.16);frame(r.x+r.w/2,cy+r.h/2+.035,r.w+.18,.07);frame(r.x+r.w/2,cy-r.h/2-.05,r.w+.22,.10);
 }
 const unitP=frameUnitGeometry.attributes.position,unitN=frameUnitGeometry.attributes.normal;
 for(const [color,boxes]of groups){const positions=new Float32Array(boxes.length*unitP.count*3),normals=new Float32Array(positions.length);let cursor=0;for(const q of boxes)for(let i=0;i<unitP.count;i++){positions[cursor]=unitP.getX(i)*q.w+q.x;normals[cursor++]=unitN.getX(i);positions[cursor]=unitP.getY(i)*q.h+q.y;normals[cursor++]=unitN.getY(i);positions[cursor]=unitP.getZ(i)*q.d+q.z;normals[cursor++]=unitN.getZ(i)}const geo=new T.BufferGeometry();geo.setAttribute('position',new T.BufferAttribute(positions,3));geo.setAttribute('normal',new T.BufferAttribute(normals,3));geo.computeBoundingSphere();const mesh=new T.Mesh(geo,reveal(mat(color),b.id+'-recessed-window-frames'));mesh.name=b.id+'-recessed-window-frames';mesh.castShadow=mesh.receiveShadow=true;g.add(mesh);occluderMeshes.push(mesh)}
}

function block(g,p,b){
 if(!b.facadeProfile)return contextBlock(g,p,b);
 if(p.shape==='round')return contextBlock(g,p,b);
 const frontTexture=prototypeFacade(b,p),sideTexture=prototypeFacade(b,p,true),wall=mat('#ffffff',frontTexture),side=mat('#ffffff',sideTexture),top=mat('#ffffff',textures.buildingroof);
 box(p.w,p.h,p.d,p.x,p.y,p.z,[side,side,top,top,wall,wall],g,b.id+'-body');
 box(p.w+.08,.20,p.d+.08,p.x,p.y,p.z,mat(b.id==='research'?'#86634e':'#a59e8d'),g,b.id+'-foundation');
 if(b.id==='research'){const red=mat('#a16c55'),y=p.y+p.h-.15;for(let z of [-1,1])box(p.w+.3,.45,.35,p.x,y,p.z+z*p.d/2,red,g,b.id+'-brick-parapet');for(let x of [-1,1])box(.35,.45,p.d,p.x+x*p.w/2,y,p.z,red,g,b.id+'-brick-parapet')}
 else roof(g,p,b);
 recessedWindowFrames(g,p,b,frontTexture,sideTexture);
}

function registeredEntrance(g,e,b){
 const eg=new T.Group();eg.position.set(e.x,0,e.z);eg.rotation.y=T.MathUtils.degToRad(e.angle);g.add(eg);
 const w=e.width,h=e.canopyHeight,d=e.canopyDepth,type=e.canopy,stone=mat('#c5c5b5'),warm=mat('#dad5c4'),red=mat('#9d624b');
 const doorW=Math.min(type==='research-portico'?14:type==='accounting'?15:type==='library'?7:type==='blue'?16:7,w*.85);
 if(type!=='none')opening(eg,0,.06,doorW,type==='research-portico'?6.1:type==='accounting'?6.8:3.05,b);
 if(type==='research-portico'){
  box(w,1.25,d,0,h-1.25,d/2-1.0,red,eg,b.id+'-recess-portico-header');
  for(let x of e.columns)box(.55,h-1.25,.55,x,0,d*.65,red,eg,b.id+'-recess-portico-post');
  glazing(eg,0,.35,-.2,18,6.15,b,8,2);
 }else if(type==='activity'){
  box(w,.55,d,0,h-.55,d/2,warm,eg,b.id+'-white-portico');box(w,.24,.35,0,h,d-.1,red,eg,b.id+'-brick-lintel');
 }else if(type==='red-tile'){
  box(w,.35,d,0,h-.35,d/2,warm,eg,b.id+'-portico-soffit');roof(eg,{x:0,z:d/2,w:w+.2,d:d+.2,h,y:0,style:'brick',roof:'hip'},b);
 }else if(type==='blue'){
  box(w+2,1.05,d,0,3.1,d/2,mat('#356086'),eg,b.id+'-blue-fascia');glazing(eg,0,.15,.08,w-2,2.8,b,7,1);
 }else if(type==='single'||type==='academic-wide'||type==='lecture'){
  box(w,.28,d,0,h-.28,d/2,mat(type==='academic-wide'?'#ae6c4b':'#d2c8af'),eg,b.id+'-entrance-slab');
  if(type==='academic-wide')box(w,.42,.25,0,h,d-.04,red,eg,b.id+'-red-edge');
 }else if(type==='steel-frame'){
  for(let x of [-w/2,w/2])box(.18,7.6,.18,x,0,d*.6,mat('#adb9b5'),eg,b.id+'-steel-entry-upright');
  box(w+.2,.20,.25,0,7.5,d*.6,mat('#b9c3bc'),eg,b.id+'-steel-entry-head');for(let y of [3.7,5.6])box(w,.12,d,0,y,d/2,mat('#b6beb3'),eg,b.id+'-entry-frame-tie');
 }else if(['phoenix','library','accounting','economics','cafe','hall','canteen','sports','newcanteen','greenleaf'].includes(type)){
  if(!['accounting','library','cafe','newcanteen'].includes(type))box(w,.20,2.3,0,3.45,1.1,mat(type==='phoenix'?'#889c97':'#c6c6b5'),eg,b.id+'-'+type+'-door-cap');
 }
 if(type!=='research-portico')for(let x of e.columns)box(.55,h,.55,x,0,d*.65,type==='activity'?stone:type==='red-tile'?warm:mat('#a18d71'),eg,b.id+'-registered-column');
 for(let i=0;i<e.steps;i++){const begin=i*e.run+(i?e.landing:0),end=(i+1)*e.run+e.landing;box(Math.min(w,12),(e.steps-i)*e.rise,end-begin,0,0,(begin+end)/2,stone,eg,b.id+'-registered-step')}
 return eg;
}

function prototypeBuilding(b){
 if(!b.facadeProfile)return legacyArchitecturalBuilding(b);
 // Most landmarks retain their individually modelled roofs/arcades; their walls and entrances use prototype rules.
 if(!['research','activity','accounting','phoenix','sufe_cafe','greenleaf_canteen','cainiao_station','wudonglecture','academic_link','teaching1','teaching2','teaching4','economics','enterprise','exchange','wuchuan_pool','wuchuan_hall','badminton','wuchuan_canteen','library','third_canteen'].includes(b.id)){const g=legacyArchitecturalBuilding(b);if(['finance','bookstore','statistics','guoding_gym'].includes(b.id))for(const e of b.entrances||[])registeredEntrance(g,e,b);return g}
 const g=new T.Group();g.name=b.id;g.position.set(b.center[0],0,b.center[1]);g.rotation.y=T.MathUtils.degToRad(b.rotation);root.add(g);
 for(const p of b.parts)block(g,p,b);
 if(b.id==='research'){
  // Continuous red piers replace the former stack of white ledges and independent blue window boxes.
  const p=b.parts[0],brick=mat('#a46b55');for(let face of [-1,1]){const bw=(p.w-3.2)/12;for(let i=1;i<12;i++)box(bw*.45,p.h-1.3,.70,p.x-p.w/2+1.6+i*bw,.65,p.z+face*(p.d/2+.14),brick,g,b.id+'-continuous-pier');for(let x of [-1,1])box(1.6,p.h,.7,p.x+x*(p.w/2-.8),0,p.z+face*(p.d/2+.14),brick,g,b.id+'-outer-brick-frame');const sd=(p.d-3.2)/7;for(let i=1;i<7;i++)box(.7,p.h-1.3,sd*.45,p.x+face*(p.w/2+.14),.65,p.z-p.d/2+1.6+i*sd,brick,g,b.id+'-side-window-slot')}
 }else if(b.id==='activity'){
  for(const p of b.parts)for(let x=-p.w/2+.3;x<p.w/2;x+=4.2)box(.33,p.h,.16,p.x+x,0,p.z+p.d/2+.04,mat('#a96851'),g,b.id+'-brick-pilaster');
 }else if(b.id==='accounting'){
  glazing(g,16,.4,6.10,18,6.7,b,7,3);box(82,.24,1,0,7.3,18.35,mat('#cbbdab'),g,b.id+'-upper-cantilever');
  for(let x of [-34,-24,-14,-4,6,26,36])box(.40,7.3,.5,x,0,18,mat('#c8baa7'),g,b.id+'-gallery-column');
 }else if(b.id==='phoenix'){
  glazing(g,0,.25,15.08,23,10.6,b,8,4);
  for(let x of [-11.8,11.8])box(.30,11.1,.45,x,0,15.12,mat('#d3cebd'),g,b.id+'-atrium-edge');
 }else if(b.id==='sufe_cafe'){
  glazing(g,15.3,.12,8.58,5.1,8.0,b,3,3);box(5.7,.24,17.4,15.3,8.5,0,mat('#a7684f'),g,b.id+'-glass-end-frame');
 }else if(b.id==='third_canteen'){
  glazing(g,-8.5,.25,17.58,6,10.3,b,3,3);
  for(let y of [3.7,7.4]){box(16,.24,10,-20,y,12.5,mat('#a3765e'),g,b.id+'-recessed-gallery-floor');box(16,.78,.36,-20,y+.24,17.35,mat('#a56f57'),g,b.id+'-recessed-gallery-front')}
  const edge=mat('#a86f57'),roofMat=mat('#8e8e82');box(58,.8,36,0,10.7,0,[edge,edge,roofMat,edge,edge,edge],g,b.id+'-unified-canteen-eave');
 }else if(b.id==='greenleaf_canteen'){
  box(3.7,.18,1.4,0,4.05,13.65,mat('#aaa99a'),g,b.id+'-balcony');for(let x=-1.7;x<=1.7;x+=.23)box(.035,.75,.04,x,4.23,14.32,mat('#5c665a'),g,b.id+'-balcony-rail');box(3.7,.06,.07,0,4.98,14.32,mat('#5c665a'),g,b.id+'-balcony-top');
 }else if(b.id==='cainiao_station'){
  for(let x of [-10.5,10.5]){box(2.6,2.15,1.1,x,.1,4.5,mat('#607e89'),g,b.id+'-lockers');for(let y=.4;y<2;y+=.45)box(2.45,.025,.03,x,y,5.07,mat('#c9d1c4'),g,b.id+'-locker-dividers')}
 }else if(b.id==='library'){
  glazing(g,39,0,32.6,7.5,25.5,b,3,7);glazing(g,-37,0,27.6,12,15,b,3,5);
 }else if(b.id==='economics'){
  for(const p of b.parts)for(let y=3.7;y<p.h;y+=3.7)box(p.w+.09,.12,.16,p.x,y,p.z+p.d/2+.05,mat('#d0d7cf'),g,b.id+'-white-ribbon-sill');
 }
 for(const e of b.entrances||[])registeredEntrance(g,e,b);
 return g;
}

function entryCanopy(g,e,b){if(b.entrances){for(const q of b.entrances)registeredEntrance(g,q,b);return}return contextEntryCanopy(g,e,b)}
function architecturalBuilding(b){return prototypeBuilding(b)}
