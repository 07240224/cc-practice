
// This isolated c1 review scene keeps geographical ground coordinates separate
// from the common oblique projection. It never changes the production campus.
const canvas = document.getElementById('scene');
const ctx = canvas.getContext('2d', {alpha:false});
const WORLD = {w:1440,h:1120};
const R = 11, CELL = 16;
const buildings = [
 {id:'lecture',name:'武东路梯教',x:235,y:70,w:610,d:210,h:264,floors:6,entry:{x:450,y:324}},
 {id:'teaching3',name:'第三教学楼',x:430,y:650,w:690,d:215,h:272,floors:6,entry:{x:535,y:915}}
];
const bridge = {id:'bridge',x:690,y:280,w:90,d:370,z:86};
const trees = [
 {id:'tree1',x:150,y:255,type:0,scale:.34},
 {id:'tree2',x:230,y:835,type:1,scale:.36},
 {id:'tree3',x:1375,y:810,type:3,scale:.32},
 {id:'tree4',x:990,y:225,type:2,scale:.30},
 {id:'tree5',x:125,y:635,type:3,scale:.28}
];
const treeRegions = ASSETS.regions.trees_painted;
const treeHeights=[172,176,153,162,148];
const LIGHT={x:.36,y:.22};
const CACHE_RATIO=2;
let groundMaterials=null;
const pillars = [];
for (const y of [325,590]) for(const x of [690,768]) pillars.push({id:`pillar-${x}-${y}`,x,y,w:12,d:12});
// Entrances and stairs are outside solid footprints, never inside a building box.
const porchPosts=[{id:'lecture-porch-left',x:394,y:298,w:5,d:5},{id:'lecture-porch-right',x:508,y:298,w:5,d:5},{id:'third-porch',x:476,y:884,w:13,d:13}];
const treeWells=trees.map(t=>({id:t.id+'-well',x:t.x-23,y:t.y-23,w:46,d:46}));
// Deliberately placed planting and furniture; all raised bases share navigation.
const plantingBeds=[
 {id:'lecture-west-bed',x:250,y:309,w:104,d:32,h:4},
 {id:'lecture-east-bed',x:561,y:302,w:100,d:34,h:4},
 {id:'lecture-corner-bed',x:820,y:306,w:90,d:35,h:4},
 {id:'third-entry-bed',x:620,y:873,w:125,d:27,h:4},
 {id:'third-east-bed',x:961,y:872,w:131,d:29,h:4},
 {id:'court-north-bed',x:464,y:585,w:160,d:42,h:3},
 {id:'court-east-bed',x:856,y:586,w:196,d:35,h:3},
 {id:'west-pocket-bed',x:161,y:782,w:138,d:24,h:3,natural:true},
 {id:'east-garden-bed',x:1362,y:871,w:46,d:125,h:3,natural:true},
 {id:'south-garden-bed',x:660,y:1044,w:240,d:54,h:3,natural:true}
];
const furnishings=[
 {id:'west-bench',kind:'bench',x:196,y:723,w:80,d:24,h:34},
 {id:'third-bench',kind:'bench',x:800,y:874,w:80,d:24,h:34},
 {id:'north-lamp',kind:'lamp',x:1077,y:343,w:8,d:8,h:92},
 {id:'south-lamp',kind:'lamp',x:1118,y:884,w:8,d:8,h:92}
];
const decorSolids=[...plantingBeds,...furnishings];
const solids = buildings.map(b=>({id:b.id,x:b.x,y:b.y,w:b.w,d:b.d})).concat(pillars,porchPosts,treeWells,decorSolids);
const roads=[{x:105,y:395,w:1235,d:135},{x:1195,y:395,w:100,d:575},{x:370,y:935,w:925,d:66}];
const pavements=[{x:105,y:292,w:1235,d:270},{x:1145,y:380,w:200,d:650},{x:325,y:885,w:1020,d:145},{x:315,y:520,w:110,d:470},{x:380,y:280,w:170,d:120},{x:160,y:710,w:155,d:70}];
const onPaving=(x,y)=>pavements.some(r=>inRect(x,y,r));
function pavedSegment(a,b){const n=Math.max(1,Math.ceil(Math.hypot(a.x-b.x,a.y-b.y)/8));for(let i=0;i<=n;i++)if(!onPaving(a.x+(b.x-a.x)*i/n,a.y+(b.y-a.y)*i/n))return false;return true}

const player={x:450,y:324,dir:0,frame:1,moving:false};
const keys=new Set(); let path=[],visited=[true,false,false],showRoute=false,plan=false,overview=false;
let W=1600,H=1000,DPR=1,scale=1,ox=0,oy=0,clock=0,last=0,raf=0;
let hidden=[],clickMarker=null,images={},entities=[],ground=null,groundRect=null;
const alphaState=new Map(); let focused=true,noticeUntil=0;
const routePoints=[{x:450,y:324},{x:450,y:460},{x:735,y:460},{x:1200,y:460},{x:1200,y:955},{x:535,y:955},{x:535,y:915}];
let viewMode='raised';
const views={original:{a:.9,b:1.15,c:-.12,d:.4,z:1},raised:{a:.9,b:1.15,c:-.12,d:.65,z:.92}};
const P=(x,y,z=0)=>{const v=views[viewMode];return{x:v.a*x+v.b*y,y:v.c*x+v.d*y-v.z*z}};
const unproject=(x,y)=>{const v=views[viewMode],det=v.a*v.d-v.b*v.c;return{x:(v.d*x-v.b*y)/det,y:(-v.c*x+v.a*y)/det}};
const screen=p=>({x:ox+scale*p.x,y:oy+scale*p.y});
const worldFromScreen=(x,y)=>unproject((x-ox)/scale,(y-oy)/scale);
function polygon(c,pts,fill,stroke=null,width=1){c.beginPath();pts.forEach((p,i)=>i?c.lineTo(p.x,p.y):c.moveTo(p.x,p.y));c.closePath();if(fill){c.fillStyle=fill;c.fill()}if(stroke){c.strokeStyle=stroke;c.lineWidth=width;c.stroke()}}
function line(c,a,b,color,width=1){c.beginPath();c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);c.strokeStyle=color;c.lineWidth=width;c.stroke()}
function rectPoints(x,y,w,d,z=0){return[P(x,y,z),P(x+w,y,z),P(x+w,y+d,z),P(x,y+d,z)]}
function floorRect(c,x,y,w,d,fill,stroke=null,z=0){polygon(c,rectPoints(x,y,w,d,z),fill,stroke)}
function noise(seed){let v=seed|0;return()=>{v=(Math.imul(v,1664525)+1013904223)|0;return(v>>>0)/4294967296}}
function tone(hex,f){const n=parseInt(hex.slice(1),16);return '#'+[n>>16,(n>>8)&255,n&255].map(v=>Math.min(255,Math.round(v*f)).toString(16).padStart(2,'0')).join('')}
function inRect(x,y,o,pad=0){return x>o.x-pad&&x<o.x+o.w+pad&&y>o.y-pad&&y<o.y+o.d+pad}
function collides(x,y){
 if(x<R+18||y<R+18||x>WORLD.w-R-18||y>WORLD.h-R-18)return true;
 for(const b of solids){const dx=x-Math.max(b.x,Math.min(x,b.x+b.w));const dy=y-Math.max(b.y,Math.min(y,b.y+b.d));if(dx*dx+dy*dy<R*R)return true}
 for(const t of trees)if(Math.hypot(x-t.x,y-t.y)<R+12)return true;
 return false;
}
function safeSegment(a,b){let n=Math.ceil(Math.hypot(a.x-b.x,a.y-b.y)/5);for(let i=1;i<=n;i++)if(collides(a.x+(b.x-a.x)*i/n,a.y+(b.y-a.y)*i/n))return false;return true}
function findPath(start,end){
 if(collides(end.x,end.y))return [];
 if(safeSegment(start,end)&&pavedSegment(start,end))return [{...end}];
 const nx=Math.ceil(WORLD.w/CELL),ny=Math.ceil(WORLD.h/CELL);
 const pos=i=>({x:(i%nx)*CELL+CELL/2,y:Math.floor(i/nx)*CELL+CELL/2});
 const idx=p=>Math.floor(p.y/CELL)*nx+Math.floor(p.x/CELL);
 let s=idx(start),goal=idx(end);if(collides(pos(s).x,pos(s).y)){
   let options=[];for(let yy=-2;yy<=2;yy++)for(let xx=-2;xx<=2;xx++){let i=s+yy*nx+xx,p=pos(i);if(i>=0&&i<nx*ny&&!collides(p.x,p.y)&&safeSegment(start,p))options.push(i)}
   if(!options.length)return [];s=options.sort((a,b)=>Math.hypot(pos(a).x-start.x,pos(a).y-start.y)-Math.hypot(pos(b).x-start.x,pos(b).y-start.y))[0];
 }
 if(collides(pos(goal).x,pos(goal).y))return [];
 let open=[s],came=new Map(),g=new Map([[s,0]]),closed=new Set();
 const heuristic=i=>Math.hypot(pos(i).x-end.x,pos(i).y-end.y);
 while(open.length){open.sort((a,b)=>(g.get(a)+heuristic(a))-(g.get(b)+heuristic(b)));const cur=open.shift();
   if(cur===goal){let result=[end],i=cur;while(i!==s){result.push(pos(i));i=came.get(i)}result.push(pos(s));result.reverse();
     let smooth=[],from=start,k=0;while(k<result.length){let j=result.length-1;while(j>k&&(!safeSegment(from,result[j])||!pavedSegment(from,result[j])))j--;if(!safeSegment(from,result[j]))return [];smooth.push(result[j]);from=result[j];k=j+1}return smooth}
   closed.add(cur);const p=pos(cur);
   for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]){
     const q={x:p.x+dx*CELL,y:p.y+dy*CELL};if(q.x<0||q.y<0||q.x>WORLD.w||q.y>WORLD.h)continue;
     const ni=idx(q);if(closed.has(ni)||collides(q.x,q.y)||!safeSegment(p,q))continue;
     const ng=g.get(cur)+Math.hypot(dx,dy)*CELL*(onPaving(q.x,q.y)?1:3.5);if(ng<(g.get(ni)??Infinity)){came.set(ni,cur);g.set(ni,ng);if(!open.includes(ni))open.push(ni)}
   }
 }return [];
}
function message(text){document.getElementById('message').textContent=text;noticeUntil=clock+4}
function goTo(dest){if(collides(dest.x,dest.y)){message('这里是楼体或实体设施，请点击旁边的道路');return false}path=findPath(player,dest);if(!path.length){message('请点击地图内可达的道路');return false}clickMarker={...dest,t:clock};message('正在前往 · 按方向键可接管行走');return true}
function move(dx,dy){const count=Math.max(1,Math.ceil(Math.hypot(dx,dy)/4));for(let i=0;i<count;i++){let x=player.x+dx/count,y=player.y+dy/count;if(!collides(x,y)){player.x=x;player.y=y}else{if(!collides(x,player.y))player.x=x;if(!collides(player.x,y))player.y=y}}}
function steps(c,x,y,w,d,h=10){for(let i=0;i<4;i++)floorRect(c,x,y+i*d/4,w,d/4,'#d2ccbd','#b0ab9f',h*(1-i/4));}
// Painted sprites are kept at 2x in tight caches; geometry remains in world units.
function pixelEntity(id,draw,bounds,depth,extra={}){
 const origin={x:Math.floor(bounds.x),y:Math.floor(bounds.y)},ratio=CACHE_RATIO;
 const logicalW=Math.ceil(bounds.w)+2,logicalH=Math.ceil(bounds.h)+2;
 const buffer=document.createElement('canvas');buffer.width=logicalW*ratio;buffer.height=logicalH*ratio;
 const g=buffer.getContext('2d',{willReadFrequently:true});g.setTransform(ratio,0,0,ratio,-origin.x*ratio,-origin.y*ratio);g.imageSmoothingQuality='high';draw(g);
 const rgba=g.getImageData(0,0,buffer.width,buffer.height).data,alpha=new Uint8Array(buffer.width*buffer.height);
 for(let i=0;i<alpha.length;i++)alpha[i]=rgba[i*4+3];
 return{id,buffer,origin,logicalW,logicalH,ratio,alpha,depth,...extra};
}
function projectedBounds(x,y,w,d,h,pad=12){
 const pts=[...rectPoints(x,y,w,d),...rectPoints(x,y,w,d,h)];
 const minX=Math.min(...pts.map(p=>p.x))-pad,minY=Math.min(...pts.map(p=>p.y))-pad;
 return{x:minX,y:minY,w:Math.max(...pts.map(p=>p.x))-minX+pad,h:Math.max(...pts.map(p=>p.y))-minY+pad};
}
function compactEntity(o,draw){return pixelEntity(o.id,draw,projectedBounds(o.x-20,o.y-15,o.w+40,o.d+30,o.h+22,10),P(o.x,o.y+o.d).y,{kind:'decor',footprint:o})}
// Each mound remains upright and uniformly scaled. Only root positions are projected.
function shrubGroups(b,index=plantingBeds.indexOf(b)){
 const along=b.w>=b.d,length=along?b.w:b.d;
 const count=Math.max(2,Math.round(length/(b.natural?46:38)));
 return Array.from({length:count},(_,i)=>{
  const u=(i+.5)/count,jitter=[-.10,.09,-.04,.12,-.07][i%5];
  return{x:b.x+b.w*(along?u:.5+jitter),y:b.y+b.d*(along?.5+jitter:u),
   width:(b.natural?78:58)*[1,.88,1.07,.94,1.02][i%5],type:(index+i)%4};
 }).sort((a,b)=>P(a.x,a.y).y-P(b.x,b.y).y);
}
function plantSprite(c,b,index){
 for(const g of shrubGroups(b,index)){
  const r=ASSETS.regions.shrubs[g.type].rect,p=P(g.x,g.y,b.h);
  const h=g.width*r[3]/r[2];
  c.save();c.filter='saturate(0.86) brightness(0.96)';
  c.drawImage(images.shrubs,...r,p.x-g.width/2,p.y-h,g.width,h);c.restore();
 }
}
// A single projected corner cannot order a wide facade against all its front beds.
// Build constraints from ground footprints, then use projected depth only to break ties.
function orderEntities(items){
 const footprint=e=>e.building||e.footprint||(e.kind==='bridge'?bridge:
  e.tree?{x:e.tree.x-23,y:e.tree.y-23,w:46,d:46}:null);
 const edges=items.map(()=>new Set()),indegree=items.map(()=>0);
 const add=(a,b)=>{if(!edges[a].has(b)){edges[a].add(b);indegree[b]++}};
 for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++){
  const a=footprint(items[i]),b=footprint(items[j]);if(!a||!b)continue;
  if(a.x<b.x+b.w&&b.x<a.x+a.w){
   if(a.y+a.d<=b.y)add(i,j);else if(b.y+b.d<=a.y)add(j,i);
  }
  if(a.y<b.y+b.d&&b.y<a.y+a.d){
   if(a.x>=b.x+b.w)add(i,j);else if(b.x>=a.x+a.w)add(j,i);
  }
 }
 const result=[],ready=items.map((_,i)=>i).filter(i=>!indegree[i]);
 while(ready.length){ready.sort((a,b)=>items[a].depth-items[b].depth);const i=ready.shift();result.push(items[i]);for(const j of edges[i])if(--indegree[j]===0)ready.push(j)}
 if(result.length!==items.length)throw new Error('Static drawing-order cycle: '+items.filter((_,i)=>indegree[i]).map(e=>e.id).join(','));
 return result;
}
function makeLandscape(){return [
 ...plantingBeds.map((b,i)=>compactEntity({...b,h:85},c=>{
  if(b.natural){
   // Natural soil/turf edges belong to the ground; only plants are on this layer.
  }else{
   box(c,b.x,b.y,b.w,b.d,b.h,0,'#b2a78e','#939b83','#d4c5a5');
   floorRect(c,b.x+3,b.y+3,b.w-6,b.d-6,'#736d50',null,b.h+.1);
   for(let x=b.x+18;x<b.x+b.w;x+=25)line(c,P(x,b.y+b.d,0),P(x,b.y+b.d,b.h),'#8b887077',.6);
  }
  plantSprite(c,b,i);
 })),
 ...furnishings.map(o=>compactEntity(o,c=>{
  const x=o.x,y=o.y;
  if(o.kind==='bench'){
   for(const xx of [x+8,x+o.w-8]){box(c,xx,y+2,3,19,16,0,'#4c584e','#37483f','#78806b');line(c,P(xx,y+21,0),P(xx,y+21,34),'#485446',2.5)}
   for(let i=0;i<4;i++){
    floorRect(c,x,y+i*5,o.w,4,i%2?'#b18b58':'#a78050','#735b3d',16);
    line(c,P(x+3,y+i*5+1,16),P(x+o.w-3,y+i*5+1,16),'#d9b87888',.6);
   }
   for(let i=0;i<3;i++){
    line(c,P(x,y+22,23+i*5),P(x+o.w,y+22,23+i*5),'#987346',3.5);
    line(c,P(x,y+22,24+i*5),P(x+o.w,y+22,24+i*5),'#cfaa6b',.7);
   }
   for(const xx of [x+8,x+o.w-8])line(c,P(xx,y+1,22),P(xx,y+22,22),'#455446',2);
  }else{
   box(c,x,y,8,8,4,0,'#8d9384','#777e72','#bbc0ab');
   line(c,P(x+4,y+4,3),P(x+4,y+4,o.h),'#59675c',3);
   line(c,P(x+3,y+4,3),P(x+3,y+4,o.h),'#c9ccb6',.8);
   box(c,x-5,y-3,18,14,3,o.h,'#566358','#485b50','#8b947e');
   box(c,x-2,y,12,8,7,o.h-7,'#e0dfc5','#c6cfb9','#d9ddc9');
  }
 }))
]}
function treeShape(t,i=trees.indexOf(t)){
 const r=treeRegions[t.type],height=treeHeights[i],width=height*r.rect[2]/r.rect[3];
 return{r:r.rect,height,width,anchor:r.anchor[0]};
}
function treeSpriteCanvas(t){
 const a=treeShape(t),buff=document.createElement('canvas');buff.width=a.width*2;buff.height=a.height*2;
 const g=buff.getContext('2d');g.drawImage(images.trees_painted,...a.r,0,0,buff.width,buff.height);
 g.globalCompositeOperation='source-in';g.fillStyle='#3b4b37';g.fillRect(0,0,buff.width,buff.height);
 return{...a,buff};
}
function castGeometry(c,points,z,opacity){
 const base=points.map(([x,y])=>P(x,y)),top=points.map(([x,y])=>P(x+LIGHT.x*z,y+LIGHT.y*z));
 const all=[...base,...top].sort((a,b)=>a.x-b.x||a.y-b.y),cross=(o,a,b)=>(a.x-o.x)*(b.y-o.y)-(a.y-o.y)*(b.x-o.x);
 const lower=[],upper=[];for(const p of all){while(lower.length>1&&cross(lower.at(-2),lower.at(-1),p)<=0)lower.pop();lower.push(p)}
 for(const p of [...all].reverse()){while(upper.length>1&&cross(upper.at(-2),upper.at(-1),p)<=0)upper.pop();upper.push(p)}
 c.save();c.globalAlpha=opacity;c.filter='blur(2px)';polygon(c,[...lower.slice(0,-1),...upper.slice(0,-1)],'#334539');c.restore();
}
function groundShadows(c){
 for(const b of buildings)castGeometry(c,[[b.x,b.y],[b.x+b.w,b.y],[b.x+b.w,b.y+b.d],[b.x,b.y+b.d]],b.h,.17);
 // Elevated deck and its supports have separate shadows, leaving readable pavement.
 const deck=[[bridge.x,bridge.y],[bridge.x+bridge.w,bridge.y],[bridge.x+bridge.w,bridge.y+bridge.d],[bridge.x,bridge.y+bridge.d]];
 c.save();c.globalAlpha=.16;c.filter='blur(1.5px)';polygon(c,deck.map(([x,y])=>P(x+LIGHT.x*(bridge.z+45),y+LIGHT.y*(bridge.z+45))),'#334539');c.restore();
 for(const o of [...pillars,...furnishings])castGeometry(c,[[o.x,o.y],[o.x+o.w,o.y],[o.x+o.w,o.y+o.d],[o.x,o.y+o.d]],o.h||bridge.z,.14);
 const v=views[viewMode],light=P(LIGHT.x,LIGHT.y);
 for(const t of trees){
  const s=treeSpriteCanvas(t),p=P(t.x,t.y);
  c.save();c.globalAlpha=.22;c.filter='blur(1.7px)';c.translate(p.x,p.y);
  // Reproject the alpha silhouette onto the ground, anchored at the same trunk.
  c.transform(v.a,v.c,-light.x,-light.y,0,0);
  c.drawImage(s.buff,-s.width*s.anchor,-s.height,s.width,s.height);c.restore();
  c.save();c.fillStyle='#34482f22';const q=P(t.x,t.y);c.beginPath();c.ellipse(q.x,q.y,15,5,-.1,0,7);c.fill();c.restore();
 }
 for(const b of plantingBeds)for(const g of shrubGroups(b)){
  const q=P(g.x,g.y);c.save();c.translate(q.x,q.y);
  c.scale(1,.32);const r=g.width*.47,fade=c.createRadialGradient(0,0,r*.15,0,0,r);
  fade.addColorStop(0,'#33452b66');fade.addColorStop(.65,'#43563430');fade.addColorStop(1,'#43563400');
  c.fillStyle=fade;c.beginPath();c.arc(0,0,r,0,Math.PI*2);c.fill();c.restore();
 }
}
function prepareMaterials(){
 const asphalt=document.createElement('canvas');asphalt.width=256;asphalt.height=256;
 const g=asphalt.getContext('2d'),data=g.createImageData(256,256),rnd=noise(7021);
 for(let i=0;i<data.data.length;i+=4){const n=(rnd()-.5)*17;data.data[i]=153+n;data.data[i+1]=155+n;data.data[i+2]=146+n;data.data[i+3]=255}g.putImageData(data,0,0);
 return{asphalt};
}
function fillGroundTexture(c,rect,image,period,alpha=1){
 const v=views[viewMode];c.save();c.transform(v.a,v.c,v.b,v.d,0,0);
 const pattern=c.createPattern(image,'repeat');pattern.setTransform(new DOMMatrix().scale(period/image.width));
 c.globalAlpha=alpha;c.fillStyle=pattern;c.fillRect(rect.x,rect.y,rect.w,rect.d);c.restore();
}
function buildGround(){
 const v=views[viewMode];const bounds={x:-80,y:-260,w:WORLD.w*v.a+WORLD.h*v.b+160,h:WORLD.h*v.d+500};
 groundRect=bounds;ground=document.createElement('canvas');ground.width=Math.ceil(bounds.w);ground.height=Math.ceil(bounds.h);const c=ground.getContext('2d');c.translate(-bounds.x,-bounds.y);
 floorRect(c,0,0,WORLD.w,WORLD.h,'#a5b17f','#95a273');
 fillGroundTexture(c,{x:0,y:0,w:WORLD.w,d:WORLD.h},images.grass,440,.58);
 const rnd=noise(204);
 const paved=pavements;
 for(const r of paved){floorRect(c,r.x-5,r.y-5,r.w+10,r.d+10,'#a3aa91');floorRect(c,r.x,r.y,r.w,r.d,'#d8d3c3','#c4c3b4');
 c.save();polygon(c,rectPoints(r.x,r.y,r.w,r.d));c.clip();
 for(let x=Math.floor(r.x/35)*35;x<r.x+r.w;x+=35)for(let y=Math.floor(r.y/32)*32;y<r.y+r.d;y+=32){
  const pick=noise(x*101+y*307)(),tint=['#d5cebb','#ddd5c3','#d9d0be','#cec8b6'][Math.floor(pick*4)];
  floorRect(c,x,y,35,32,tint,'#b9b4a27a');
  line(c,P(x+1,y+1),P(x+34,y+1),'#f5ecd466',.65);
  for(let k=0;k<6;k++){const q=P(x+3+rnd()*29,y+3+rnd()*26);c.fillStyle=k%2?'#fff8df12':'#686c5710';c.fillRect(q.x,q.y,1.5,1)}
 }
 c.restore();}
 for(const r of roads){floorRect(c,r.x-5,r.y-5,r.w+10,r.d+10,'#c5b6a3');floorRect(c,r.x,r.y,r.w,r.d,'#a2a49b','#8d978a');fillGroundTexture(c,r,groundMaterials.asphalt,128,.80);}
 for(let i=0;i<6500;i++){const x=rnd()*WORLD.w,y=rnd()*WORLD.h;if(roads.some(r=>inRect(x,y,r))){const p=P(x,y);c.fillStyle=i%2?'#ffffff10':'#384e4510';c.fillRect(p.x,p.y,1,1)}}
 // Perimeter brick strips and simple draining grates, never props filling space.
 for(const y of [382,541])for(let x=110;x<1330;x+=20){if(roads.some(r=>inRect(x+10,y+4,r)))continue;floorRect(c,x,y,20,8,'#b58e77');line(c,P(x,y),P(x,y+8),'#d6b89b',.8)}
 for(const x of [530,1115]){floorRect(c,x,387,34,7,'#68706a');for(let i=2;i<34;i+=4)line(c,P(x+i,387),P(x+i,394),'#a8b0a3',.8)}
 // Ground detail follows usage: entrance courts, quiet lanes and edge drainage.
 for(const court of [{x:367,y:308,w:188,d:74},{x:471,y:901,w:176,d:29}]){
  floorRect(c,court.x,court.y,court.w,court.d,'#b79b82','#987f69');
  for(let yy=court.y+3;yy<court.y+court.d;yy+=12)for(let xx=court.x+3;xx<court.x+court.w-8;xx+=26)
   floorRect(c,xx,yy,23,9,((xx+yy)%3)?'#c4b09a':'#bfa48c','#ab927b');
 }
 // Subtle aggregate and maintenance patches rather than decorative road clutter.
 for(const patch of [{x:865,y:421,w:105,d:63},{x:1212,y:728,w:61,d:85}])floorRect(c,patch.x,patch.y,patch.w,patch.d,'#7e898612','#8c958d35');
 for(const r of roads){
  const along=r.w>r.d;
  for(let k=0;k<(along?r.w:r.d);k+=28){
   const x=along?r.x+k:r.x-5,y=along?r.y-5:r.y+k;
   if(roads.some(other=>other!==r&&inRect(x+(along?13:2),y+(along?2:13),other)))continue;
   floorRect(c,x,y,along?26:5,along?5:26,'#ddd8c7','#aeb2a3');
  }
 }
 for(const q of [{x:1138,y:543,w:34,d:10},{x:1297,y:735,w:10,d:34},{x:920,y:1004,w:34,d:9}]){
  floorRect(c,q.x,q.y,q.w,q.d,'#737e76','#c8c7b6');
  for(let k=3;k<q.w;k+=5)line(c,P(q.x+k,q.y+1),P(q.x+k,q.y+q.d-1),'#aeb6a8',1);
 }
 // Two flush inspection covers in the lane are surface detail, not obstacles.
 for(const [x,y] of [[1070,478],[1240,875]]){
  floorRect(c,x-14,y-14,28,28,'#959f95','#7c897f');
  for(let k=-9;k<11;k+=5)line(c,P(x+k,y-9),P(x+k,y+9),'#aeb5a8',.7);
 }
 for(const b of buildings){
  floorRect(c,b.x-12,b.y-10,b.w+24,b.d+25,'#c2c0b0');
  for(let k=0;k<5;k++)floorRect(c,b.x,b.y+b.d+k*5,b.w,5,`rgba(50,66,47,${.12-k*.022})`);
 }
 // Paved pauses beside the two entrances and the existing west bench.
 for(const r of [{x:770,y:880,w:132,d:45},{x:160,y:710,w:140,d:70}]){
  floorRect(c,r.x,r.y,r.w,r.d,'#c5bca7','#b4ab97');
  for(let xx=r.x+6;xx<r.x+r.w;xx+=18)line(c,P(xx,r.y),P(xx,r.y+r.d),'#b1a79380',.7);
 }

 // Bridge contact shadows stop at the pier bases; no false obstacle across the lane.

 for(const y of [570,1038])for(let x=y===570?440:385;x<(y===570?1090:1125);x+=33){
  const q=P(x,y);line(c,q,P(x+22,y+2),'#7d8b5b65',.7);
 }

 steps(c,398,282,106,38);steps(c,487,867,99,40);
 for(const t of trees){floorRect(c,t.x-23,t.y-23,46,46,'#b5a98b','#8a9275');floorRect(c,t.x-19,t.y-19,38,38,'#8b8765');}
 groundShadows(c);
 // Small leaf fall remains beside planting, never a noisy all-over ground texture.
 for(const bed of plantingBeds){for(let i=0;i<14;i++){const x=bed.x+rnd()*bed.w,y=bed.y+bed.d+3+rnd()*8;const q=P(x,y);c.fillStyle=i%3?'#9d8f5d55':'#a2976d66';c.beginPath();c.ellipse(q.x,q.y,1.5+rnd(),.7,-.4,0,7);c.fill()}}

}
function wall(c,x1,y1,x2,y2,z,h,fill,seed=0){
 const a=P(x1,y1,z),b=P(x2,y2,z),d=P(x1,y1,z+h),e=P(x2,y2,z+h);const grad=c.createLinearGradient(d.x,d.y,a.x,a.y);grad.addColorStop(0,tone(fill,1.035));grad.addColorStop(.5,fill);grad.addColorStop(1,tone(fill,seed?.85:.9));polygon(c,[a,b,e,d],grad,'#776f5d',.7);
 // Quiet fine tile texture, aligned to each facade plane.
 const len=Math.hypot(x2-x1,y2-y1),dx=(x2-x1)/len,dy=(y2-y1)/len;
 c.save();polygon(c,[a,b,e,d]);c.clip();
 for(let zz=z+5;zz<z+h;zz+=5){line(c,P(x1,y1,zz),P(x2,y2,zz),'#f8ecd938',.55);for(let s=(Math.round(zz/5)%2)*4;s<len;s+=9)line(c,P(x1+dx*s,y1+dy*s,zz),P(x1+dx*s,y1+dy*s,zz+5),'#5b574027',.5)}
 const rnd=noise(Math.round(x1*17+y1*13+h));for(let i=0;i<len*h/65;i++){const t=rnd(),zz=z+rnd()*h,pt=P(x1+(x2-x1)*t,y1+(y2-y1)*t,zz);c.fillStyle=i%2?'#fff5cf10':'#4b483c09';c.fillRect(pt.x,pt.y,1.4,1.4)}
 c.restore();
}
function box(c,x,y,w,d,h,base=0,front='#c4b597',side='#aeaa95',roof='#c5c6bc'){
 wall(c,x,y,x,y+d,base,h,side,1);wall(c,x,y+d,x+w,y+d,base,h,front,0);
 floorRect(c,x,y,w,d,roof,'#7e8173',base+h);
}
function windowOn(c,x1,y1,x2,y2,z,h){
 const a=P(x1,y1,z),b=P(x2,y2,z),d=P(x1,y1,z+h),e=P(x2,y2,z+h);
 const glass=c.createLinearGradient(d.x,d.y,a.x,a.y);glass.addColorStop(0,'#3e5860');glass.addColorStop(.55,'#738f92');glass.addColorStop(1,'#4f7079');polygon(c,[a,b,e,d],glass,'#35494e',1.7);
 const mx=(x1+x2)/2,my=(y1+y2)/2;
 polygon(c,[P(x1,y1,z+2),P(mx,my,z+2),P(mx,my,z+h-2),P(x1,y1,z+h-2)],'#c6d3be22');
 const tx=x1+(x2-x1)*.27,ty=y1+(y2-y1)*.27;line(c,P(tx,ty,z+4),P(tx,ty,z+h-4),'#dfd4b25c',2);
 line(c,P(mx,my,z),P(mx,my,z+h),'#d1d2bd',1.2);line(c,P(x1,y1,z+h*.28),P(x2,y2,z+h*.28),'#b4bcae',.8);
 line(c,P(x1,y1,z+h-2),P(x2,y2,z+h-2),'#263a465a',4);line(c,P(x1,y1,z+1),P(x2,y2,z+1),'#ded1ad',1);
}
function facadeWindows(c,b,x,width,floors=b.floors){
 const cols=Math.floor(width/66),gap=12,bay=width/cols;
 for(let f=0;f<floors;f++)for(let i=0;i<cols;i++){
   const xx=x+i*bay+gap/2,zz=15+f*41;windowOn(c,xx,b.y+b.d+.7,xx+bay-gap,b.y+b.d+.7,zz,25);
   box(c,xx-3,b.y+b.d-1,bay-gap+6,9,3,zz+27,'#d7cdb6','#b7b29f','#e0d7c2');
 }
}
function makeEntity(id,draw,depth,extra={}){
 const o=extra.building||bridge;
 const bounds=extra.kind==='building'?projectedBounds(o.x-20,o.y-15,o.w+45,o.d+90,o.h+45,12):projectedBounds(o.x-20,o.y-10,o.w+40,o.d+30,o.z+65,10);
 return pixelEntity(id,draw,bounds,depth,extra);
}
// Treat painted facades as UV surfaces on the verified geometric model. The
// image's backdrop is never drawn; its perspective never changes collision.
function texturedQuad(c,img,src,dst){
 for(const ids of [[0,1,2],[0,2,3]]){
  const s=ids.map(i=>({x:src[i][0],y:src[i][1]})),t=ids.map(i=>dst[i]);
  const ax=s[1].x-s[0].x,ay=s[1].y-s[0].y,bx=s[2].x-s[0].x,by=s[2].y-s[0].y,det=ax*by-ay*bx;
  const ux=t[1].x-t[0].x,uy=t[1].y-t[0].y,vx=t[2].x-t[0].x,vy=t[2].y-t[0].y;
  const a=(ux*by-vx*ay)/det,b=(uy*by-vy*ay)/det,cc=(vx*ax-ux*bx)/det,d=(vy*ax-uy*bx)/det;
  c.save();polygon(c,t);c.clip();c.transform(a,b,cc,d,t[0].x-a*s[0].x-cc*s[0].y,t[0].y-b*s[0].x-d*s[0].y);c.drawImage(img,0,0);c.restore();
 }
}
function paintedSurfaces(c,b){
 const im=images[b.id],x=b.x,y=b.y,w=b.w,d=b.d,h=b.h;
 c.save();c.filter='saturate(0.82) contrast(0.94) brightness(1.01)';
 if(b.id==='lecture'){
  texturedQuad(c,im,[[59,228],[488,389],[488,922],[59,735]],[P(x,y,h),P(x,y+d,h),P(x,y+d),P(x,y)]);
  texturedQuad(c,im,[[488,389],[1478,245],[1478,762],[488,922]],[P(x,y+d,h),P(x+w,y+d,h),P(x+w,y+d),P(x,y+d)]);
  texturedQuad(c,im,[[59,228],[1045,90],[1478,245],[488,389]],[P(x,y,h),P(x+w,y,h),P(x+w,y+d,h),P(x,y+d,h)]);
 }else{
  texturedQuad(c,im,[[659,368],[1479,278],[1479,762],[659,851]],[P(x+129,y+d,h),P(x+w,y+d,h),P(x+w,y+d),P(x+129,y+d)]);
  texturedQuad(c,im,[[269,241],[1062,134],[1479,278],[659,368]],[P(x+129,y,h),P(x+w,y,h),P(x+w,y+d,h),P(x+129,y+d,h)]);
  texturedQuad(c,im,[[76,246],[478,392],[478,881],[56,727]],[P(x+4,y+5,295),P(x+4,y+d+5,295),P(x+4,y+d+5),P(x+4,y+5)]);
  texturedQuad(c,im,[[478,392],[659,368],[659,851],[478,881]],[P(x+4,y+d+5,295),P(x+129,y+d+5,295),P(x+129,y+d+5),P(x+4,y+d+5)]);
  texturedQuad(c,im,[[76,246],[261,222],[659,368],[478,392]],[P(x+4,y+5,295),P(x+129,y+5,295),P(x+129,y+d+5,295),P(x+4,y+d+5,295)]);
 }
 c.restore();
}
function buildingArt(b){return makeEntity(b.id,c=>{
 box(c,b.x,b.y,b.w,b.d,b.h);
 // Red-brown brick plinth and flat parapet, not decorative European architecture.
 wall(c,b.x,b.y,b.x,b.y+b.d,0,19,'#98745a',1);wall(c,b.x,b.y+b.d,b.x+b.w,b.y+b.d,0,19,'#a47c5f');
 for(const z of [6,12])line(c,P(b.x,b.y+b.d+.8,z),P(b.x+b.w,b.y+b.d+.8,z),'#d7a88b55',.6);
 floorRect(c,b.x+10,b.y+10,b.w-20,b.d-20,'#b9bcb5','#8e978e',b.h+.3);
 for(let x=b.x+65;x<b.x+b.w;x+=75)line(c,P(x,b.y+12,b.h+1),P(x,b.y+b.d-12,b.h+1),'#9ca398',.8);
 box(c,b.x,b.y,b.w,6,7,b.h,'#d5cbb4','#b5b29f','#e0d8c3');box(c,b.x,b.y,6,b.d,7,b.h,'#d5cbb4','#b5b29f','#e0d8c3');box(c,b.x,b.y+b.d-6,b.w,6,7,b.h,'#d5cbb4','#b5b29f','#e0d8c3');
 if(b.id==='lecture'){
   facadeWindows(c,b,b.x+15,b.w-30);
   // Recessed center bay preserves the lecture building's characteristic setback.
   wall(c,390,b.y+b.d+2,510,b.y+b.d+2,20,b.h-30,'#9e9787',1);
   for(let f=0;f<6;f++)windowOn(c,399,b.y+b.d+3,500,b.y+b.d+3,16+f*41,27);
   for(const yy of [b.y+30,b.y+100,b.y+165])for(let f=0;f<6;f++)windowOn(c,b.x-.8,yy,b.x-.8,yy+36,15+f*41,25);
   box(c,385,260,133,49,7,56,'#d6ccba','#c0bcac','#e4ddcd');
   for(const xx of [394,508])box(c,xx,298,5,5,54,0,'#dad7c8','#bcbfb1','#e5e3d3');
   windowOn(c,404,281,495,281,1,48);
 }else{
   facadeWindows(c,b,b.x+158,b.w-170);
   box(c,b.x+4,b.y+5,125,b.d,295,0,'#bfb095','#aaa38e','#d2cbb7');
   for(let f=0;f<6;f++)windowOn(c,b.x+132,b.y+b.d+.9,b.x+155,b.y+b.d+.9,18+f*43,32);
   box(c,468,843,145,55,8,58,'#dbd2be','#bdb8a9','#e3ddcf');
   box(c,476,884,13,13,56,0,'#ac765c','#885f4d','#b98566');
   windowOn(c,500,867,576,867,2,49);
 }
 paintedSurfaces(c,b);
 // The canopy is a separate raised structure; its feet stay on the ground plane.
 if(b.id==='lecture'){
  box(c,385,260,133,49,7,56,'#d8cdb6','#b4ac98','#e8dcc4');
  windowOn(c,404,281,495,281,1,48);
  for(const xx of [394,508])box(c,xx,298,5,5,54,0,'#d9d4c3','#adae9e','#e5e0ce');
 }else{
  box(c,468,843,145,55,8,58,'#ddceb4','#b4a58d','#e8dcc4');
  windowOn(c,500,867,576,867,2,49);
  box(c,476,884,13,13,56,0,'#af7459','#885e4b','#b98566');
 }
 // Architectural signs follow the facade's own projection, rather than screen labels.
 const sign=b.id==='lecture'?{x:401,y:309,z:58,text:b.name}:{x:493,y:898,z:60,text:b.name};
 const sp=P(sign.x,sign.y,sign.z);c.save();c.translate(sp.x,sp.y);c.transform(views[viewMode].a,views[viewMode].c,0,1,0,0);c.font='600 11px "Microsoft YaHei",sans-serif';c.fillStyle='#43524a';c.fillText(sign.text,0,0);c.restore();
 // Slim downpipe with highlights ties material scale to the doors.
 const pipe=P(b.x+10,b.y+b.d+2),pipeTop=P(b.x+10,b.y+b.d+2,b.h-5);line(c,pipe,pipeTop,'#8b9288',2.5);line(c,{x:pipe.x-1,y:pipe.y},{x:pipeTop.x-1,y:pipeTop.y},'#e0ddca',.8);
},P(b.x,b.y+b.d).y,{kind:'building',building:b})}
function makeBridge(){return makeEntity('bridge',c=>{
 for(const p of pillars)box(c,p.x,p.y,p.w,p.d,bridge.z,0,'#a98064','#8d745d','#c2b294');
 box(c,bridge.x,bridge.y,bridge.w,bridge.d,9,bridge.z,'#bbb7a7','#a09f91','#d4d0bd');
 wall(c,bridge.x,bridge.y,bridge.x,bridge.y+bridge.d,bridge.z+9,29,'#bdbba9',1);
 for(let y=bridge.y+15;y<bridge.y+bridge.d-10;y+=42)windowOn(c,bridge.x-.5,y,bridge.x-.5,y+31,bridge.z+13,23);
 texturedQuad(c,images.lecture,[[1000,540],[1454,476],[1454,532],[1000,604]],[P(bridge.x,bridge.y,bridge.z+38),P(bridge.x,bridge.y+bridge.d,bridge.z+38),P(bridge.x,bridge.y+bridge.d,bridge.z+9),P(bridge.x,bridge.y,bridge.z+9)]);
 box(c,bridge.x-5,bridge.y,bridge.w+10,bridge.d,7,bridge.z+42,'#c8c2ae','#a9aa9c','#dcd6c2');
},P(bridge.x,bridge.y+bridge.d).y,{kind:'bridge'})}
function makeTrees(){return trees.map((t,i)=>{
 const s=treeShape(t,i),p=P(t.x,t.y),height=s.height;
 return pixelEntity(t.id,c=>{
  c.save();c.filter='saturate(0.80) brightness(0.97)';
  const r=ASSETS.regions.understory[(i+1)%4].rect,w=43,h=w*r[3]/r[2];
  c.drawImage(images.understory,...r,p.x-32,p.y-h,w,h);
  c.drawImage(images.trees_painted,...s.r,p.x-s.width*s.anchor,p.y-height,s.width,height);c.restore();
 },{x:p.x-s.width*s.anchor-5,y:p.y-height-5,w:s.width+10,h:height+12},P(t.x,t.y+23).y,{kind:'tree',tree:t});
})}
function inFrontOfPlayer(e){
 if(e.kind==='building'){const b=e.building;return player.y<b.y+b.d+R&&player.x>b.x-R}
 if(e.kind==='bridge')return true;
 return e.depth>P(player.x,player.y).y-3;
}
function isOccluding(e){
 if(!inFrontOfPlayer(e))return false;const p=actorPoint();
 for(const z of [8,22,36]){const x=Math.round((p.x-e.origin.x)*e.ratio),y=Math.round((p.y-z-e.origin.y)*e.ratio);if(x>=0&&y>=0&&x<e.buffer.width&&y<e.buffer.height&&e.alpha[y*e.buffer.width+x]>100)return true}
 return false;
}
const reveal=document.createElement('canvas');const rc=reveal.getContext('2d');
function drawEntity(e,dt){
 const hit=isOccluding(e),target=hit?1:0,a=(alphaState.get(e.id)||0),v=a+(target-a)*Math.min(1,dt*13);alphaState.set(e.id,v);if(hit)hidden.push(e.id);
 if(v<.01){ctx.drawImage(e.buffer,e.origin.x,e.origin.y,e.logicalW,e.logicalH);return}
 if(reveal.width<e.buffer.width)reveal.width=e.buffer.width;if(reveal.height<e.buffer.height)reveal.height=e.buffer.height;
 rc.setTransform(1,0,0,1,0,0);rc.clearRect(0,0,reveal.width,reveal.height);rc.globalCompositeOperation='source-over';rc.drawImage(e.buffer,0,0);
 const p=actorPoint(),r=e.ratio,x=(p.x-e.origin.x)*r,y=(p.y-e.origin.y-15)*r;
 const grad=rc.createRadialGradient(x,y,28*r,x,y,105*r);grad.addColorStop(0,`rgba(0,0,0,${.93*v})`);grad.addColorStop(.55,`rgba(0,0,0,${.82*v})`);grad.addColorStop(1,'rgba(0,0,0,0)');
 rc.globalCompositeOperation='destination-out';rc.fillStyle=grad;rc.fillRect(x-106*r,y-106*r,212*r,212*r);rc.globalCompositeOperation='source-over';
 ctx.drawImage(reveal,0,0,e.buffer.width,e.buffer.height,e.origin.x,e.origin.y,e.logicalW,e.logicalH);
}
function elevation(x,y){for(const r of [{x:398,y:282,w:106,d:38},{x:487,y:867,w:99,d:40}])if(inRect(x,y,r))return 10*(1-(y-r.y)/r.d);return 0}
function actorPoint(){return P(player.x,player.y,elevation(player.x,player.y))}
function drawPlayer(){const p=actorPoint();ctx.fillStyle='#283e3d35';ctx.beginPath();ctx.ellipse(p.x,p.y,10,4,0,0,7);ctx.fill();const row=player.dir,f=ASSETS.frames[row][player.frame],s=.156;ctx.drawImage(images.student,f.x,f.y,f.w,f.h,p.x-f.w*s/2,p.y-f.h*s,f.w*s,f.h*s);}
function ring(p,color,r=13){const a=P(p.x,p.y);ctx.save();ctx.translate(a.x,a.y);ctx.scale(1,.45);ctx.beginPath();ctx.arc(0,0,r,0,7);ctx.strokeStyle=color;ctx.lineWidth=2;ctx.stroke();ctx.restore()}
function drawRoute(){ctx.save();ctx.beginPath();routePoints.forEach((p,i)=>{const q=P(p.x,p.y);i?ctx.lineTo(q.x,q.y):ctx.moveTo(q.x,q.y)});ctx.strokeStyle='#527e7280';ctx.lineWidth=3;ctx.setLineDash([9,8]);ctx.stroke();ctx.restore();for(const b of buildings)ring(b.entry,'#4d7f70',16)}
function drawPlan(){
 ctx.save();ctx.setTransform(DPR,0,0,DPR,0,0);ctx.fillStyle='#f5f4e9f5';ctx.fillRect(0,0,W,H);const s=Math.min((W-380)/WORLD.w,(H-210)/WORLD.h),x=(W-WORLD.w*s)/2,y=120;ctx.translate(x,y);ctx.scale(s,s);
 ctx.fillStyle='#b4bf9a';ctx.fillRect(0,0,WORLD.w,WORLD.h);
 ctx.fillStyle='#e0dac8';for(const r of pavements)ctx.fillRect(r.x,r.y,r.w,r.d);
 ctx.strokeStyle='#718b74';ctx.setLineDash([12,12]);ctx.lineWidth=5;ctx.strokeRect(bridge.x,bridge.y,bridge.w,bridge.d);ctx.setLineDash([]);
 for(const b of buildings){ctx.fillStyle='#a69b85';ctx.fillRect(b.x,b.y,b.w,b.d);ctx.fillStyle='#faf7eb';ctx.font='24px sans-serif';ctx.fillText(b.name,b.x+25,b.y+80)}
 ctx.fillStyle='#655e4e';for(const p of [...pillars,...porchPosts])ctx.fillRect(p.x,p.y,p.w,p.d);
 for(const d of decorSolids){ctx.fillStyle=d.kind?'#81765d':'#6d8057';ctx.fillRect(d.x,d.y,d.w,d.d)}
 for(const t of treeWells)ctx.fillRect(t.x,t.y,t.w,t.d);
 ctx.beginPath();routePoints.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle='#588576';ctx.lineWidth=4;ctx.setLineDash([10,8]);ctx.stroke();ctx.setLineDash([]);
 ctx.fillStyle='#d99957';ctx.beginPath();ctx.arc(player.x,player.y,13,0,7);ctx.fill();ctx.strokeStyle='#fffdf2';ctx.lineWidth=3;ctx.stroke();
 ctx.fillStyle='#4e6652';ctx.font='22px sans-serif';ctx.fillText('北 ↑',20,45);ctx.font='18px sans-serif';ctx.fillText('虚线为二层连廊 · 地面从柱脚之间通行',355,575);ctx.restore();
}
function camera(snap=false,dt=.016){const foot=P(player.x,player.y),v=views[viewMode],width=WORLD.w*v.a+WORLD.h*v.b,low=-365,high=WORLD.h*v.d;const targetScale=overview?Math.min((W-90)/(width+40),(H-230)/(high-low)):Math.max(.7,Math.min(W/1400,H/820));const tx=overview?(W-width*targetScale)/2:W*.46-foot.x*targetScale;const ty=overview?140-low*targetScale:H*.66-foot.y*targetScale;const k=snap?1:Math.min(1,dt*5);scale+=(targetScale-scale)*k;ox+=(tx-ox)*k;oy+=(ty-oy)*k;}
function resize(){W=innerWidth;H=innerHeight;DPR=Math.min(devicePixelRatio||1,2);canvas.width=W*DPR;canvas.height=H*DPR;camera(true);}
function update(dt){clock+=dt;let sx=0,sy=0;if(focused&&!plan){sx=Number(keys.has('KeyD')||keys.has('ArrowRight'))-Number(keys.has('KeyA')||keys.has('ArrowLeft'));sy=Number(keys.has('KeyS')||keys.has('ArrowDown'))-Number(keys.has('KeyW')||keys.has('ArrowUp'))}
 let dx=0,dy=0;const speed=keys.has('ShiftLeft')||keys.has('ShiftRight')?240:150;
 if(sx||sy){path=[];const v=unproject(sx,sy),l=Math.hypot(v.x,v.y);dx=v.x/l*speed*dt;dy=v.y/l*speed*dt}
 else if(path.length&&!plan&&focused){const q=path[0],vx=q.x-player.x,vy=q.y-player.y,len=Math.hypot(vx,vy);if(len<3)path.shift();else{const step=Math.min(speed*dt,len);dx=vx/len*step;dy=vy/len*step}}
 const before={x:player.x,y:player.y};if(dx||dy)move(dx,dy);const actual=P(player.x-before.x,player.y-before.y);player.moving=Math.hypot(actual.x,actual.y)>.01;
 if(player.moving){player.dir=Math.abs(actual.x)>Math.abs(actual.y)?(actual.x>0?3:2):(actual.y>0?0:1);player.frame=[0,1,2,1][Math.floor(clock*8)%4]}else player.frame=1;
 if(Math.abs(player.x-735)<50&&player.y>395&&player.y<530)visited[1]=true;
 if(visited[1]&&Math.hypot(player.x-535,player.y-915)<45)visited[2]=true;
 document.querySelectorAll('#stops li').forEach((li,i)=>li.classList.toggle('done',visited[i]));
 let place='武东路校区 · 院楼道路';if(Math.hypot(player.x-450,player.y-324)<90)place='武东路梯教门前';else if(inRect(player.x,player.y,bridge,10))place='二层连廊下方';else if(Math.hypot(player.x-535,player.y-915)<90)place='第三教学楼门前';else if(player.x>1150)place='院楼东侧路口';
 document.getElementById('place').textContent=place;
 if(clock>noticeUntil)document.getElementById('message').textContent=visited[2]?'已走通两栋楼之间的路线，可自由探索':hidden.length?'遮挡已淡出，脚下道路保持可见':'WASD 移动，或点击道路前往';
}
function render(dt){camera(false,dt);ctx.setTransform(DPR,0,0,DPR,0,0);ctx.fillStyle='#e8e8dc';ctx.fillRect(0,0,W,H);ctx.translate(ox,oy);ctx.scale(scale,scale);ctx.drawImage(ground,groundRect.x,groundRect.y);
 if(showRoute)drawRoute();if(clickMarker&&clock-clickMarker.t<4)ring(clickMarker,'#61887c',11+Math.sin(clock*5)*2);
 // Static surfaces keep the same painter order regardless of the actor's side.
 // Occluding layers reveal a local patch, then the actor is composited in it.
 // Re-grouping static objects around the actor would draw the bridge over walls.
 hidden=[];for(const e of entities)drawEntity(e,dt);drawPlayer();
 // A small foot locator remains visible through foliage; not a replacement for fading.
 if(hidden.length){const p=P(player.x,player.y);ctx.strokeStyle='#f9f6df';ctx.lineWidth=1.1;ctx.beginPath();ctx.ellipse(p.x,p.y+1,12,5,0,0,7);ctx.stroke()}
 if(plan)drawPlan();
}
function frame(t){const dt=Math.min(.035,(t-last)/1000||.016);last=t;update(dt);render(dt);raf=requestAnimationFrame(frame)}
addEventListener('keydown',e=>{if(['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();keys.add(e.code);if(e.code==='Escape'){plan=false;path=[];document.getElementById('plan').setAttribute('aria-pressed','false')}});
addEventListener('keyup',e=>keys.delete(e.code));
function stop(){keys.clear();path=[];player.moving=false;focused=false}
addEventListener('blur',stop);document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();else focused=true});addEventListener('focus',()=>focused=true);addEventListener('resize',resize);
canvas.addEventListener('pointerdown',e=>{focused=true;canvas.focus();if(!plan){const r=canvas.getBoundingClientRect();goTo(worldFromScreen(e.clientX-r.left,e.clientY-r.top))}});
document.getElementById('reset').onclick=()=>{player.x=450;player.y=324;path=[];visited=[true,false,false];keys.clear();message('已回到梯教入口');canvas.focus()};
document.getElementById('route').onclick=e=>{showRoute=!showRoute;e.currentTarget.setAttribute('aria-pressed',showRoute);canvas.focus()};
document.getElementById('overview').onclick=e=>{overview=!overview;e.currentTarget.setAttribute('aria-pressed',overview);e.currentTarget.textContent=overview?'跟随角色':'全景';canvas.focus()};
document.getElementById('plan').onclick=e=>{plan=!plan;path=[];keys.clear();e.currentTarget.setAttribute('aria-pressed',plan);canvas.focus()};
document.getElementById('angle').onclick=()=>{
 viewMode=viewMode==='raised'?'original':'raised';keys.clear();path=[];alphaState.clear();
 groundMaterials=groundMaterials||prepareMaterials();buildGround();entities=orderEntities([...buildings.map(buildingArt),makeBridge(),...makeTrees(),...makeLandscape()]);camera(true);
 document.getElementById('angle').textContent=viewMode==='raised'?'对比：切回原视角':'对比：略高俯视';
 document.getElementById('angle-label').textContent=viewMode==='raised'?'略高俯视 · 新版':'低角度侧视 · 原版';
 message('视角已切换，建筑位置和角色位置保持不变');canvas.focus();
};
for(const b of document.querySelectorAll('[data-key]')){b.addEventListener('pointerdown',e=>{e.preventDefault();b.setPointerCapture(e.pointerId);focused=true;keys.add(b.dataset.key)});for(const ev of ['pointerup','pointercancel','lostpointercapture'])b.addEventListener(ev,()=>keys.delete(b.dataset.key))}
// Read-only inspection surface used by the independent route/collision acceptance.
Object.defineProperty(window,'campusSample',{value:Object.freeze({
 rendering:()=>({drawOrder:entities.map(e=>e.id),orderingCycles:[],cacheRatio:CACHE_RATIO,cacheBytes:entities.reduce((n,e)=>n+e.buffer.width*e.buffer.height*4+e.alpha.byteLength,0),entities:entities.map(e=>({id:e.id,width:e.buffer.width,height:e.buffer.height,ratio:e.ratio})),paintedPlants:true}),
 state:()=>({player:{...player},path:path.map(p=>({...p})),visited:[...visited],occluders:[...hidden],plan,viewMode,ready:!!ground}),
 project:(x,y)=>screen(P(x,y)),unproject:(x,y)=>worldFromScreen(x,y),
 geometry:()=>JSON.parse(JSON.stringify({buildings,pillars,porchPosts,trees,treeWells,roads,pavements,plantingBeds,furnishings,decorSolids,bridge,world:WORLD,radius:R,route:routePoints})),
 blocked:(x,y)=>collides(x,y),pathTo:(x,y)=>findPath(player,{x,y}).map(p=>({...p}))
})});
Promise.all(['student','trees_painted','understory','shrubs','grass','lecture','teaching3'].map(name=>new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{images[name]=i;resolve()};i.onerror=reject;i.src=ASSETS[name]}))).then(()=>{
 groundMaterials=groundMaterials||prepareMaterials();buildGround();entities=orderEntities([...buildings.map(buildingArt),makeBridge(),...makeTrees(),...makeLandscape()]);resize();canvas.focus();document.documentElement.dataset.ready='true';requestAnimationFrame(frame)
}).catch(()=>message('素材加载失败，请重新打开完整样板文件'));
