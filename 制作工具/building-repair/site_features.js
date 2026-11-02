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
