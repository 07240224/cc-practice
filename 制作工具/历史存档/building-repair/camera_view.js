function updateCamera(immediate=false){
 let height=DATA.camera.viewHeight/zoom,target=new T.Vector3(player.x,.5,player.y);
 if(overview){
  const[x0,z0,x1,z1]=m.bounds;target.set((x0+x1)/2,0,(z0+z1)/2);
  const right=new T.Vector3(Math.cos(az),0,-Math.sin(az)),screenUp=new T.Vector3(-Math.sin(az)*Math.sin(elevation),Math.cos(elevation),-Math.cos(az)*Math.sin(elevation));
  const points=[];for(const x of[x0,x1])for(const z of[z0,z1])points.push(new T.Vector3(x,0,z));
  for(const b of DATA.models.filter(b=>b.map===mapId)){const a=T.MathUtils.degToRad(b.rotation);for(const p of b.parts)for(const x of[p.x-p.w/2,p.x+p.w/2])for(const z of[p.z-p.d/2,p.z+p.d/2])for(const y of[0,p.y+p.h+4])points.push(new T.Vector3(b.center[0]+Math.cos(a)*x+Math.sin(a)*z,y,b.center[1]-Math.sin(a)*x+Math.cos(a)*z))}
  const halfWidth=Math.max(...points.map(p=>Math.abs(p.clone().sub(target).dot(right)))),halfHeight=Math.max(...points.map(p=>Math.abs(p.clone().sub(target).dot(screenUp))));
  height=Math.max(halfWidth*2/(W/H),halfHeight*2)*1.14+20;follow.copy(target);
 }else if(immediate)follow.copy(target);else follow.lerp(target,1-Math.exp(-12*lastFrameDt));
 camera.left=-height*W/H/2;camera.right=height*W/H/2;camera.top=height/2;camera.bottom=-height/2;camera.position.copy(follow).addScaledVector(cameraOffset,1600);camera.lookAt(follow);camera.updateProjectionMatrix();camera.updateMatrixWorld();sun.position.set(player.x-45,70,player.y+35);sun.target.position.set(player.x,0,player.y);sun.target.updateMatrixWorld();
}
