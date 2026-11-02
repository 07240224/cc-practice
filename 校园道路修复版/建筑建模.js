// Architectural geometry. Every façade texture is drawn without text, in orthographic local coordinates.
const architectureCache=new Map();
const palette={financecenter:['#cfcec3','#a2a49a'],libraryend:['#dedfd6','#bfc4b9'],bookstore:['#e7e6db','#bdbeb4'],cream:['#d7cbb1','#bdb8a6'],academic:['#c5b49a','#a38e70'],ivory:['#dedbd0','#b5b8ac'],stone:['#ccc8bc','#98998c'],statscol:['#b6b8aa','#8c9489'],statistics:['#b0b0a3','#8c9489'],gray:['#b6b5a8','#8b9186'],pink:['#c6b3a8','#aa9b91'],brick:['#a16650','#8e5745'],redwhite:['#dfdfd3','#a36852'],redtower:['#9e5e4e','#774b42'],dorm:['#c2c0b2','#9c9e93'],library:['#d2d5ca','#a4b0a8'],cafe:['#b9633d','#814b35'],gymbase:['#a6aaa0','#808b84'],metal:['#ab614b','#7e5146']};
function architectureTexture(w,h,floors,style='cream',isSide=false){const key=[w,h,floors,style,isSide].join(':');if(architectureCache.has(key))return architectureCache.get(key);const pal=palette[style]||palette.cream,c=document.createElement('canvas');c.width=Math.min(2048,Math.ceil(w*32));c.height=Math.min(2048,Math.ceil(h*40));const q=c.getContext('2d'),sx=c.width/w,sy=c.height/h;q.scale(sx,sy);q.fillStyle=pal[0];q.fillRect(0,0,w,h);let seed=1317;function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}if(['brick','redwhite','redtower','gray','stone','academic'].includes(style)){const bh=style==='stone'?.65:.28,bw=style==='stone'?1.6:.66;for(let y=0,j=0;y<h;y+=bh,j++)for(let x=-(j%2)*bw/2;x<w;x+=bw){q.fillStyle=rng()>.5?'#ffffff0a':'#261d1408';q.fillRect(x+.02,y+.02,bw-.04,bh-.04)}q.strokeStyle='#433e2c11';q.lineWidth=.025;for(let y=0;y<h;y+=bh){q.beginPath();q.moveTo(0,y);q.lineTo(w,y);q.stroke()}}for(let i=0;i<Math.min(13000,w*h*12);i++){q.fillStyle=i%2?'#fffee50a':'#3d483809';q.fillRect(rng()*w,rng()*h,.03+rng()*.04,.03)}if(['bookstore','financecenter','libraryend','statscol'].includes(style)){const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;architectureCache.set(key,t);return t}const fh=h/floors,bay=style==='statistics'?2.1:style==='redtower'?2.8:style==='dorm'?3.7:style==='library'?4.0:style==='academic'?6.2:style==='redwhite'?3.6:4.4,cols=Math.max(1,Math.round(w/bay)),bw=w/cols;for(let r=0;r<floors;r++){const yy=h-(r+1)*fh;for(let j=0;j<cols;j++){let ww=bw*(style==='statistics'?.43:style==='academic'?.89:style==='redtower'?.43:style==='dorm'?.64:.62),wh=fh*(style==='statistics'?.74:style==='redtower'?.80:style==='academic'?.58:.62),x=(j+.5)*bw-ww/2,y=yy+fh*.22;if(style==='statistics')x+=(j%2?-.4:.4);if(style==='academic'){q.fillStyle='#536b75';q.fillRect(j*bw+bw*.06,yy+.15,bw*.88,.40);q.fillStyle='#dfd6bf';q.fillRect(j*bw,yy+.65,bw,.11)}if(style==='redwhite'){q.fillStyle='#a16a53';q.fillRect(j*bw+.05,yy,.42,fh);q.fillRect(j*bw,yy+fh-.25,bw,.25)}q.fillStyle='#746f5f';q.fillRect(x-.14,y-.13,ww+.28,wh+.27);q.fillStyle='#e0d6bc';q.fillRect(x-.08,y-.07,ww+.16,wh+.1);q.fillStyle='#3c5869';q.fillRect(x,y,ww,wh);let g=q.createLinearGradient(x,y,x+ww,y+wh);g.addColorStop(0,'#a4b6bd');g.addColorStop(.35,'#6e8796');g.addColorStop(1,'#354f60');q.fillStyle=g;q.fillRect(x+.07,y+.07,ww-.14,wh-.14);q.fillStyle='#d6dbc24d';q.beginPath();q.moveTo(x+.1,y+.1);q.lineTo(x+ww*.65,y+.1);q.lineTo(x+.1,y+wh*.65);q.fill();q.strokeStyle='#b6b9a8';q.lineWidth=.055;q.strokeRect(x+.06,y+.06,ww-.12,wh-.12);const panels=style==='academic'?4:ww>2?3:2;for(let k=1;k<panels;k++){q.beginPath();q.moveTo(x+ww*k/panels,y);q.lineTo(x+ww*k/panels,y+wh);q.stroke()}q.beginPath();q.moveTo(x,y+wh*.67);q.lineTo(x+ww,y+wh*.67);q.stroke();q.fillStyle='#efe4c8';q.fillRect(x-.18,y+wh+.05,ww+.36,.10);q.fillStyle='#3a372e23';q.fillRect(x-.09,y+wh+.15,ww+.18,.16);if(style==='dorm'&&r>0){q.fillStyle='#9c9d8d';q.fillRect(x-.3,y+wh-.3,ww+.6,.7);q.fillStyle='#d4d2c3';q.fillRect(x-.35,y+wh-.33,ww+.7,.13);q.strokeStyle='#737d73';q.lineWidth=.035;for(let k=0;k<8;k++)q.strokeRect(x-.28+k*(ww+.56)/8,y+wh-.2,.02,.5);q.fillStyle='#8b9389';q.fillRect(j*bw+.17,yy+fh*.61,.64,.48);q.fillStyle='#d7d7cb';q.fillRect(j*bw+.2,yy+fh*.61,.58,.36)}}q.fillStyle=style==='academic'?'#e0d4bc':style==='redtower'?'#835247':'#d8d3c1';q.fillRect(0,yy+fh-.13,w,.13);q.fillStyle='#292b2420';q.fillRect(0,yy+fh-.3,w,.13)}q.fillStyle='#85715b';q.fillRect(0,h-.38,w,.38);const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;t.anisotropy=4;architectureCache.set(key,t);return t}
function archMesh(shape,depth,material,g,name){const geo=new T.ExtrudeGeometry(shape,{depth,bevelEnabled:false,curveSegments:18});const obj=new T.Mesh(geo,reveal(material,name));obj.castShadow=true;obj.receiveShadow=true;obj.name=name;g.add(obj);occluderMeshes.push(obj);return obj}
function roofGeometry(w,d,h,rise,hip){const x=w/2+.45,z=d/2+.45,r=hip?Math.min(d*.25,w*.2):0,ps=[[-x,h,-z],[x,h,-z],[x,h,z],[-x,h,z],[-x+r,h+rise,0],[x-r,h+rise,0]],faces=hip?[[0,5,1],[0,4,5],[1,5,2],[2,4,3],[2,5,4],[3,4,0]]:[[0,1,5],[0,5,4],[2,3,4],[2,4,5],[3,0,4],[1,2,5]],v=[];for(const f of faces)for(const i of f)v.push(...ps[i]);const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(v,3));geo.computeVertexNormals();return geo}
function roof(g,p,b){const height=p.y+p.h,trim=mat('#d7c9b0'),dark=mat('#ffffff',textures.buildingroof);if(p.roof==='frontgable'){frontGableRoof(g,p,b);return}if(p.roof==='terrace'){terraceRoof(g,p,b);return}if(p.roof==='flat'){box(p.w+.35,.32,.32,p.x,height,p.z-p.d/2,trim,g,b.id+'-parapet');box(p.w+.35,.32,.32,p.x,height,p.z+p.d/2,trim,g,b.id+'-parapet');for(let x of [-1,1])box(.32,.32,p.d,p.x+x*p.w/2,height,p.z,trim,g,b.id+'-parapet');if(b.detail!=='context')for(let x=-p.w/2+8;x<p.w/2;x+=9){let geo=new T.BufferGeometry().setFromPoints([new T.Vector3(p.x+x,height+.03,p.z-p.d/2+.4),new T.Vector3(p.x+x,height+.03,p.z+p.d/2-.4)]);g.add(new T.Line(geo,new T.LineBasicMaterial({color:'#828a802a',transparent:true,opacity:.5})))}}else{const rise=Math.min(3.2,p.d*.16),material=reveal(mat(p.style==='statistics'?'#68736f':p.style==='dorm'?'#916954':'#9f5944'),b.id+'-pitchedroof');material.side=T.DoubleSide;let mesh=new T.Mesh(roofGeometry(p.w,p.d,height,rise,p.roof==='hip'),material);mesh.position.set(p.x,0,p.z);mesh.castShadow=true;mesh.receiveShadow=true;mesh.name=b.id+'-pitchedroof';g.add(mesh);occluderMeshes.push(mesh);box(p.w+.9,.2,p.d+.9,p.x,height-.12,p.z,mat('#b8aa8c'),g,b.id+'-eave');box(Math.max(.5,p.w-(p.roof==='hip'?p.d*.5:0)),.15,.18,p.x,height+rise,p.z,mat(p.style==='statistics'?'#89928b':'#ba7c5d'),g,b.id+'-ridge')}}
function contextBlock(g,p,b){if(p.shape==='round'){let material=mat('#e4e3d7'),geo=new T.CylinderGeometry(p.w/2,p.w/2,p.h,36),mesh=new T.Mesh(geo,reveal(material,b.id+'-rounded-end'));mesh.position.set(p.x,p.h/2,p.z);mesh.castShadow=true;mesh.receiveShadow=true;mesh.name=b.id+'-rounded-end';g.add(mesh);occluderMeshes.push(mesh);let top=new T.Mesh(new T.CylinderGeometry(p.w/2+.12,p.w/2+.12,.22,36),mat('#c8cec2'));top.position.set(p.x,p.h,p.z);g.add(top);return}const wall=mat('#fff',architectureTexture(p.w,p.h,p.floors,p.style)),side=mat('#fff',architectureTexture(p.d,p.h,p.floors,p.style,true)),top=mat('#ffffff',textures.buildingroof);box(p.w,p.h,p.d,p.x,p.y,p.z,[side,side,top,top,wall,wall],g,b.id+'-body');box(p.w+.08,.34,p.d+.08,p.x,p.y,p.z,mat(p.style==='redwhite'?'#725a47':'#918575'),g,b.id+'-foundation');roof(g,p,b);if(b.detail!=='context'&&!['bookstore','gym'].includes(b.kind)){const mm=mat(p.style==='redtower'?'#a8715d':'#d5d1c0'),ledge=mat(p.style==='redwhite'?'#e4ddcb':'#ddd5be');for(let r=1;r<p.floors;r++){const y=p.y+r*p.h/p.floors;box(p.w+.18,.16,.38,p.x,y,p.z+p.d/2+.11,ledge,g,b.id+'-floor-ledge')}if(p.style==='academic'){for(let x=-p.w/2;x<=p.w/2;x+=p.w/Math.max(1,Math.round(p.w/6.2)))box(.19,p.h,.3,p.x+x,p.y,p.z+p.d/2+.13,mm,g,b.id+'-facadepier')}}}
function frontPlane(g,x,y,z,w,h,material,name){let a=new T.Mesh(new T.PlaneGeometry(w,h),reveal(material,name));a.position.set(x,y,z);a.castShadow=true;a.receiveShadow=true;a.name=name;g.add(a);occluderMeshes.push(a);return a}
function glassMat(){return mat('#6c8999')}
function opening(g,x,z,w,h,b){frontPlane(g,x,h/2+.15,z+.025,w,h,glassMat(),b.id+'-door');for(let k=-1;k<=1;k++)box(.07,h,.09,x+k*w/3,.15,z+.10,mat('#c8c7ae'),g,b.id+'-doorframe');box(w+.22,.12,.15,x,h+.15,z+.1,mat('#d5cbb4'),g,b.id+'-doorframe')}
function contextEntryCanopy(g,e,b){const x=e.x,z=e.z,type=e.porch||'double',w=b.kind==='activity'?12:type==='wide'?13:type==='glass'?8.8:9.5,col=type==='blue'?'#466a8d':type==='wide'?'#a66042':'#d6c9ac';opening(g,x,z,w*.55,3.1,b);if(type==='blue'){box(w+3,.95,2.2,x,3.2,z+1.0,mat(col),g,b.id+'-blue-fascia');return}box(w,.3,3.7,x,3.6,z+1.6,mat(col),g,b.id+'-canopy');if(b.kind==='activity')box(w,.28,.25,x,3.9,z+3.4,mat('#a7664f'),g,b.id+'-red-canopy-edge');if(type==='wide')box(w,.5,.16,x,3.85,z+3.4,mat('#9a5a40'),g,b.id+'-canopy-face');if(type==='redhip'){const p={x,z:z+1.6,w,d:3.7,h:3.9,y:0,style:'cream',roof:'hip'};roof(g,p,b)}for(let px of type==='single'?[x-3.5]:type==='glass'?[]:[x-4,x+4])box(.5,3.6,.5,px,0,z+2.1,mat(type==='single'?'#975f43':'#c8bda0'),g,b.id+'-entry-post');for(let i=0;i<3;i++)box(6,.12,1.05,x,(2-i)*.12,z+.5+i*.65,mat('#bcb9a9'),g,b.id+'-step')}
function archBank(g,b,count,w,z,height=4.0,depth=1.0,x=0){const sh=new T.Shape();sh.moveTo(-w/2,0);sh.lineTo(w/2,0);sh.lineTo(w/2,height+.65);sh.lineTo(-w/2,height+.65);sh.closePath();let gap=w/count,r=Math.min(gap*.40,height*.37),spring=height-r;for(let i=0;i<count;i++){let cx=-w/2+gap*(i+.5),h=new T.Path();h.moveTo(cx-r,0);h.lineTo(cx-r,spring);h.absarc(cx,spring,r,Math.PI,0,true);h.lineTo(cx+r,0);h.closePath();sh.holes.push(h);opening(g,cx+x,z+.01,r*1.75,height-.1,b)}const a=archMesh(sh,depth,mat(b.kind==='bookstore'?'#e2dfce':'#c7c3b5'),g,b.id+'-arcade');a.position.set(x,.1,z);box(w+.35,.28,depth+1.0,x,height+.7,z+.5,mat('#d6d0bb'),g,b.id+'-arcade-cornice')}
function archedWindow(g,x,y,z,w,h,b){const sh=new T.Shape(),r=w/2;sh.moveTo(-r,0);sh.lineTo(r,0);sh.lineTo(r,h-r);sh.absarc(0,h-r,r,0,Math.PI,false);sh.closePath();let ob=archMesh(sh,.10,glassMat(),g,b.id+'-arched-window');ob.position.set(x,y,z);let points=[];for(let i=0;i<=20;i++){const a=i/20*Math.PI;points.push(new T.Vector3(x+Math.cos(a)*(r+.1),y+h-r+Math.sin(a)*(r+.1),z+.16))}g.add(new T.Line(new T.BufferGeometry().setFromPoints(points),new T.LineBasicMaterial({color:'#b3b7a6'})));box(.06,h,.14,x,y,z+.15,mat('#aeb6a6'),g,b.id+'-arched-mullion')}
function glazing(g,x,y,z,w,h,b,cols=5,rows=4){frontPlane(g,x,y+h/2,z,w,h,glassMat(),b.id+'-curtain-glass');let mm=mat('#bac2b8');for(let k=0;k<=cols;k++)box(.10,h,.14,x-w/2+w*k/cols,y,z+.10,mm,g,b.id+'-mullion');for(let k=0;k<=rows;k++)box(w,.1,.14,x,y+h*k/rows,z+.1,mm,g,b.id+'-transom')}
function legacyArchitecturalBuilding(b){let g=new T.Group();g.name=b.id;g.position.set(b.center[0],0,b.center[1]);g.rotation.y=T.MathUtils.degToRad(b.rotation);root.add(g);if(b.kind==='watertower'){waterTower(g,b);return g}if(b.kind==='oldgate'){oldGate(g,b);return g}if(b.kind==='gym'){const p=b.parts[0];block(g,p,b);const y=4.5,h=17,w=100,d=66;let ps=[[-w/2+5,y,-d/2+4],[w/2-5,y,-d/2+4],[w/2-5,y,d/2-4],[-w/2+5,y,d/2-4],[-w/2,y+h,-d/2],[w/2,y+h,-d/2],[w/2,y+h,d/2],[-w/2,y+h,d/2]],faces=[[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7],[4,5,6,7]],verts=[];for(let q of faces)for(let i of [q[0],q[2],q[1],q[0],q[3],q[2]])verts.push(...ps[i]);let geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(verts,3));geo.computeVertexNormals();let mesh=new T.Mesh(geo,reveal(mat('#a75b47'),b.id+'-cantilever'));mesh.name=b.id+'-cantilever';mesh.castShadow=true;mesh.receiveShadow=true;g.add(mesh);occluderMeshes.push(mesh);for(let x=-44;x<=44;x+=7.3){let pts=[new T.Vector3(x,y+.15,d/2-3.95),new T.Vector3(x,y+h,d/2+.07)];let curve=new T.LineCurve3(...pts),rib=new T.Mesh(new T.TubeGeometry(curve,1,.13,4,false),mat('#b27a5c'));rib.castShadow=true;g.add(rib);box(.65,12.5,.13,x,y+4.6,d/2+.05,mat('#587782'),g,b.id+'-slit')}glazing(g,-43,7,30,10,12,b,5,6);for(let y1=8;y1<20;y1+=.8)box(12,.12,.4,-43,y1,30.35,mat('#d4b17b'),g,b.id+'-louver');for(let x of [-25,0,25])for(let z of [-12,12])box(8,.1,3,x,21.55,z,mat('#879c9c'),g,b.id+'-skylight');box(27,12,31,35,5,9,mat('#8d7960'),g,b.id+'-screened-end');for(let yy=5.2;yy<17;yy+=.55){box(27.2,.11,.16,35,yy,24.65,mat('#bdad89'),g,b.id+'-screen-front');box(.14,.11,31.3,48.6,yy,9,mat('#b6a582'),g,b.id+'-screen-side')}glazing(g,0,.2,35.1,82,3.5,b,22,1);opening(g,-25,35.15,8,3.4,b);return g}
 if(b.kind==='bookstore'){bookstoreBody(g,b);return g}
 for(const p of b.parts)block(g,b.kind==='statistics'&&p.y===0&&p.z>0?{...p,style:'statscol'}:p,b);
 if(b.kind==='dormcourt')return g;
 if(b.kind==='academic_link'){for(let e of b.entries)entryCanopy(g,e,b);return g}
 if(b.kind==='finance'){archBank(g,b,5,23,13,4.1,1.3);for(let x of [-26,-9,9,26])box(.65,Math.abs(x)>20?11.1:14.8,.55,x,0,Math.abs(x)>20?12.15:13.2,mat('#d1cdbf'),g,b.id+'-pilaster');for(let x of [-4.9,0,4.9]){frontPlane(g,x,9.4,13.05,3.7,9,mat('#545c55'),b.id+'-recess');for(let y of [5.4,8.4,11.4])glazing(g,x,y,13.16,2.9,2.25,b,2,1);for(let xx of [-1.9,1.9])box(.24,9.35,.65,x+xx,4.8,13.35,mat('#b8b9ac'),g,b.id+'-deep-window-jamb')}for(let x of [-7.45,7.45])for(let y of [7.2,11.3]){frontPlane(g,x,y,13.1,1.15,2.4,mat('#4b5b54'),b.id+'-ornament-recess');for(let yy of [-.65,0,.65]){let ob=new T.Mesh(new T.TorusGeometry(.40,.055,4,4),mat('#c7cbbd'));ob.position.set(x,y+yy,13.23);ob.scale.y=1.1;g.add(ob)}}for(let y of [5.1,10.8])box(54.2,.20,.65,0,y,12.2,mat('#d8d0bd'),g,b.id+'-belt');return g}
 if(b.kind==='bookstore'){archBank(g,b,4,22,6,3.8,.6,-3);for(let y of [4.7,7.9])for(let x of [-11,-5,1,7])archedWindow(g,x,y,6.1,1.5,2.3,b);let x=10;opening(g,x,6.7,1.9,3.6,b);box(3,.22,1.5,x,4.1,6.7,mat('#c7c7b7'),g,b.id+'-balcony');for(let k=0;k<8;k++)box(.04,.85,.05,x-1.35+k*.39,4.3,7.35,mat('#45544b'),g,b.id+'-balconyrail');box(2.9,.06,.08,x,5.15,7.35,mat('#45544b'),g,b.id+'-rail');return g}
 if(b.kind==='library'){glazing(g,39,0,32.6,7.5,25.5,b,3,7);for(let y=4;y<26;y+=3.7)box(7.7,.12,.5,39,y,32.85,mat('#b8c1b5'),g,b.id+'-atriumfloor');glazing(g,-37,0,27.6,12,15,b,3,5)}
 if(b.kind==='research'){for(let x=-18;x<=18;x+=3)box(.22,51.8,.45,x,0,12.1,mat('#ae705a'),g,b.id+'-pier');glazing(g,0,0,22.15,12,7.2,b,4,2)}
 if(b.kind==='greenleaf'){for(let x=-25;x<30;x+=8){glazing(g,x,4.25,13.16,5.1,2.8,b,2,1);for(let yy of [4.7,5.65,6.6]){let loop=[];for(let i=0;i<=24;i++){let a=i/24*Math.PI*2;loop.push(new T.Vector3(x+Math.sin(a)*.55,yy+Math.cos(a)*.53,13.35))}g.add(new T.Line(new T.BufferGeometry().setFromPoints(loop),new T.LineBasicMaterial({color:'#e6e0ce'})))}}glazing(g,0,.4,13.2,51,3.0,b,14,1);box(3.7,.17,1.4,0,4.05,13.65,mat('#b9b3a0'),g,b.id+'-balcony');box(3.7,.8,.11,0,4.22,14.35,mat('#5a6357'),g,b.id+'-balconyrail')}
 if(b.kind==='halal'){archBank(g,b,12,69,12.02,3.35,.55);for(let y of [3.9,7.4])box(72.7,.22,.7,0,y,12.1,mat('#d0c4ac'),g,b.id+'-balconyband');for(let i=0;i<18;i++)box(3.0,.20,.70,38,(17-i)*.20,-10+i*.68,mat('#b9b6a5'),g,b.id+'-exterior-stair');box(3.3,.24,3,38,3.6,-10.5,mat('#b9b6a5'),g,b.id+'-stairlanding')}
 if(b.kind==='newcanteen'){frontPlane(g,-18,6.1,17.61,14,6.5,mat('#514f45'),b.id+'-stairwell');for(let yy of [3.7,7.4]){box(14,.22,3,-18,yy,18.8,mat('#95644e'),g,b.id+'-open-stair-slab');box(14,.8,.3,-18,yy+.22,20.2,mat('#9c6a54'),g,b.id+'-brick-balcony')}glazing(g,0,.35,17.6,15,10.3,b,4,3);box(58,.9,36,0,10.6,0,mat('#ad725d'),g,b.id+'-wide-cornice')}
 if(b.kind==='cafe'){glazing(g,0,.35,8.6,33,3.2,b,12,1);for(let x=-18;x<=18;x+=.7)box(.07,3.3,.12,x,3.8,8.57,mat('#cd8053'),g,b.id+'-corrugation')}
 if(b.kind==='cainiao'){glazing(g,0,.1,6.03,16,2.9,b,6,1);entryCanopy(g,{x:0,z:6,porch:'blue'},b);for(let x of [-10.5,10.5]){box(2.6,2.15,1.1,x,.1,4.5,mat('#607e89'),g,b.id+'-lockers');for(let y=.4;y<2;y+=.45)box(2.45,.025,.03,x,y,5.07,mat('#c9d1c4'),g,b.id+'-locker-dividers')}return g}
 if(['accounting','phoenix','economics','business'].includes(b.kind)){let z=b.kind==='accounting'?20:b.depth/2+.1;glazing(g,0,.4,z,Math.min(12,b.width*.25),b.kind==='accounting'?7:Math.min(15,b.height-1),b,4,4)}
 if(b.kind==='art'){for(let x of [-20,20])glazing(g,x,0,19.15,17,6.7,b,5,2);box(26,.35,22.5,0,14.7,-8,mat('#a36149'),g,b.id+'-stage-roof')}
 if(b.kind==='statistics'){opening(g,0,8.03,3.0,3.1,b);for(let i=0;i<3;i++)box(6,.12,1.05,0,(2-i)*.12,8.5+i*.65,mat('#b9b9ac'),g,b.id+'-innerstep');frontPlane(g,0,12.05,12.48,.65,1.25,glassMat(),b.id+'-gable-window');return g}
 if(b.kind==='redtile'){const p={x:0,z:0,w:b.width+1,d:b.depth+1,h:b.height,y:0,style:'brick',roof:'hip'};roof(g,p,b)}
 entryCanopy(g,{x:b.entryLocal[0],z:b.entryFace??b.depth/2,porch:b.porch||'double'},b);return g}

function bookstoreBody(g,b){const sh=new T.Shape();sh.moveTo(-14,6);sh.lineTo(8,6);sh.absarc(8,0,6,Math.PI/2,-Math.PI/2,true);sh.lineTo(-14,-6);sh.closePath();const mats=[reveal(mat('#bbc2b5'),b.id+'-unified-roof'),reveal(mat('#e5e3d8'),b.id+'-continuous-wall')],geo=new T.ExtrudeGeometry(sh,{depth:11.1,bevelEnabled:false,curveSegments:36}),mesh=new T.Mesh(geo,mats);mesh.rotation.x=-Math.PI/2;mesh.castShadow=true;mesh.receiveShadow=true;mesh.name=b.id+'-continuous-body';g.add(mesh);occluderMeshes.push(mesh);archBank(g,b,4,22,6.02,3.8,.55,-3);for(let y of [4.7,7.9])for(let x of [-11,-5,1,7])archedWindow(g,x,y,6.06,1.5,2.3,b);for(let y of [4.4,7.5,10.8])box(22,.12,.25,-3,y,6.10,mat('#d5d6c8'),g,b.id+'-belt');let end=new T.Group();end.position.set(14.03,0,0);end.rotation.y=Math.PI/2;g.add(end);for(let y of [.18,4.4,7.7])archedWindow(end,0,y,.04,1.85,y<1?3.65:2.45,b);box(2.9,.22,1.3,0,4.0,.7,mat('#d3d2c3'),end,b.id+'-balcony');for(let k=0;k<9;k++)box(.045,.85,.05,-1.35+k*.3375,4.15,1.30,mat('#45544b'),end,b.id+'-balconyrail');box(2.9,.06,.08,0,5.0,1.30,mat('#45544b'),end,b.id+'-rail')}

function terraceRoof(g,p,b){const h=p.y+p.h;box(p.w,.15,p.d,p.x,h,p.z,mat('#8c958b',textures.buildingroof),g,b.id+'-terrace-deck');let x=p.w/2+.5,z=p.d/2+.5,ix=x-2.3,iz=z-2.3,outer=[[-x,-z],[x,-z],[x,z],[-x,z]],inner=[[-ix,-iz],[ix,-iz],[ix,iz],[-ix,iz]],v=[];for(let i=0;i<4;i++){let j=(i+1)%4,a=[outer[i][0],h,outer[i][1]],bb=[outer[j][0],h,outer[j][1]],c=[inner[j][0],h+.85,inner[j][1]],d=[inner[i][0],h+.85,inner[i][1]];for(let q of [a,c,bb,a,d,c])v.push(...q)}const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(v,3));geo.computeVertexNormals();let mm=reveal(mat('#a35f48'),b.id+'-red-tile-border');mm.side=T.DoubleSide;let ob=new T.Mesh(geo,mm);ob.position.set(p.x,0,p.z);ob.name=b.id+'-red-tile-border';ob.castShadow=true;ob.receiveShadow=true;g.add(ob);occluderMeshes.push(ob);for(let x1 of [-p.w*.3,p.w*.3]){box(4.5,2,3.6,p.x+x1,h,p.z,mat('#d5cbb6'),g,b.id+'-roof-stair-room');const pp={x:p.x+x1,z:p.z,w:4.8,d:4.1,y:h,h:2,style:'cream',roof:'hip'};roof(g,pp,b)}if(p.w>70){box(11,1.4,5.2,p.x,h+.2,p.z,mat('#88a29e'),g,b.id+'-roof-glass-atrium');for(let k=-5;k<=5;k++)box(.07,.1,5.2,p.x+k,h+1.62,p.z,mat('#bac9be'),g,b.id+'-atriumribs')}}

function cylinderPart(g,b,rt,rb,h,x,y,z,color,name){let mesh=new T.Mesh(new T.CylinderGeometry(rt,rb,h,48),reveal(mat(color),b.id+'-'+name));mesh.position.set(x,y+h/2,z);mesh.name=b.id+'-'+name;mesh.castShadow=true;mesh.receiveShadow=true;g.add(mesh);occluderMeshes.push(mesh);return mesh}
function waterTower(g,b){cylinderPart(g,b,2.5,2.7,.35,0,0,0,'#bebba7','foot');cylinderPart(g,b,1.65,1.9,18.8,0,.35,0,'#cecdb9','shaft');cylinderPart(g,b,2.25,2.25,.55,0,18.6,0,'#c3c4b0','collar');cylinderPart(g,b,7.5,2.1,4.2,0,19.1,0,'#c6c3aa','bowl');cylinderPart(g,b,7.5,7.5,.45,0,23.3,0,'#8d6c59','rim');cylinderPart(g,b,2.3,2.5,.7,0,23.75,0,'#8f9486','cap');for(let y of [23.8,24.7]){let tor=new T.Mesh(new T.TorusGeometry(7.45,.035,5,60),mat('#778477'));tor.rotation.x=Math.PI/2;tor.position.y=y;g.add(tor)}for(let i=0;i<28;i++){let a=i/28*Math.PI*2;box(.055,1.0,.055,Math.cos(a)*7.45,23.7,Math.sin(a)*7.45,mat('#758073'),g,b.id+'-railing')}box(.045,3.1,.045,0,24.4,0,mat('#717f71'),g,b.id+'-antenna')}
function oldGate(g,b){const wall=mat('#d6d3c6');for(let p of b.parts)box(p.w,p.h,p.d,p.x,p.y,p.z,wall,g,b.id+'-masonry');box(18.6,.72,4.5,0,5.5,0,mat('#436b65'),g,b.id+'-frieze');box(18.4,.8,.2,0,5.1,2.95,mat('#477c7a'),g,b.id+'-visible-frieze');box(5.8,.45,.1,0,5.3,3.09,mat('#33556b'),g,b.id+'-blank-plaque');for(let x=-8;x<=8;x+=.8){let m=new T.Mesh(new T.TorusGeometry(.20,.045,4,4),mat('#c1b789'));m.position.set(x,5.87,2.29);g.add(m)}let mm=reveal(mat('#697a74'),b.id+'-roof');mm.side=T.DoubleSide;let ob=new T.Mesh(roofGeometry(20,6.2,6.25,1.4,true),mm);ob.castShadow=true;ob.receiveShadow=true;ob.name=b.id+'-roof';g.add(ob);occluderMeshes.push(ob);box(16,.18,.24,0,7.65,0,mat('#84958a'),g,b.id+'-ridge');for(let x of [-6.25,6.25]){let mesh=new T.Mesh(new T.CircleGeometry(.55,6),mat('#62463d'));mesh.rotation.z=Math.PI/6;mesh.position.set(x,3.0,2.03);g.add(mesh)}for(let s of [-1,1]){let pts=[new T.Vector3(s*8,7.7,0),new T.Vector3(s*9,7.95,0),new T.Vector3(s*9.8,8.3,0)],curve=new T.CatmullRomCurve3(pts);g.add(new T.Mesh(new T.TubeGeometry(curve,12,.10,5,false),mat('#788d81')))}}

function frontGableRoof(g,p,b){const h=p.y+p.h,rise=3.0,geo=roofGeometry(p.d,p.w,h,rise,false);geo.clearGroups();geo.addGroup(0,12,0);geo.addGroup(12,6,1);let a=reveal(mat('#68736e'),b.id+'-gable-roof'),c=reveal(mat('#b0b0a3'),b.id+'-gable-wall');a.side=c.side=T.DoubleSide;const mesh=new T.Mesh(geo,[a,c]);mesh.rotation.y=Math.PI/2;mesh.position.set(p.x,0,p.z);mesh.castShadow=true;mesh.receiveShadow=true;mesh.name=b.id+'-front-gable';g.add(mesh);occluderMeshes.push(mesh);box(.18,.16,p.d+.6,p.x,h+rise,p.z,mat('#89938b'),g,b.id+'-longitudinal-ridge')}

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

function prototypeBuilding(b){if(b.kind==='metro')return metroEntrance(b);
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

// The station follows the user's yellow marker. No labels are added to buildings.
function metroEntrance(b){
 const g=new T.Group();g.name=b.id;g.position.set(b.center[0],0,b.center[1]);root.add(g);
 const stone=mat('#aaa99e'),steel=mat('#637875'),glass=mat('#8bafac');
 for(const x of[-4.6,4.6]){
  box(.45,1.05,7.6,x,0,0,stone,g,'station-stair-cheek');
  for(const z of[-3.2,3.2])box(.12,3.6,.12,x,.3,z,steel,g,'station-canopy-post');
  box(.1,.12,7.5,x,1.8,0,steel,g,'station-handrail');
 }
 // Real layered treads inside a recessed access, with an open front forecourt.
 for(let k=0;k<7;k++)box(8.7,.12,.85,0,.85-k*.12,-3+k*.85,stone,g,'station-tread');
 box(9.9,.18,8.3,0,3.8,0,glass,g,'station-glass-canopy');
 for(let x=-4.8;x<5;x+=1.6)box(.07,.1,8.3,x,3.91,0,steel,g,'station-roof-rib');
 box(1.6,4.9,.4,6,0,1.2,steel,g,'station-wayfinding-pole');
 box(2.2,1.9,.5,6,4.1,1.2,mat('#b6473b'),g,'station-metro-sign');
 for(const x of[-.55,.55])box(.16,.9,.05,6+x,4.6,1.48,mat('#f3f0e5'),g,'station-symbol');
 box(1.25,.16,.05,6,5.3,1.48,mat('#f3f0e5'),g,'station-symbol');
 return g;
}
function mapBoundary(){
 const segments=m.campusWallSegments||m.site.map(p=>[...p.outer,p.outer[0]]);
 for(const segment of segments)wallLine(segment,2.2,.35,'校区围墙');
}
