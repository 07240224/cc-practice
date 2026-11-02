const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium,browserExecutable}=require('../browser_runtime.cjs');
const O=process.env.CAMPUS_OUTPUT_DIR||path.resolve(__dirname,'../../工作输出/校园道路修复V4');
(async()=>{
 const browser=await chromium.launch({executablePath:browserExecutable(),headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader','--disable-dev-shm-usage']});
 try{
  const context=await browser.newContext({viewport:{width:1600,height:1000}});await context.setOffline(true);
  const p=await context.newPage(),errors=[],requests=[];p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(!r.url().startsWith('data:'))requests.push(r.url())});
  await p.evaluate(()=>requestAnimationFrame=()=>0);await p.setContent(fs.readFileSync(path.join(O,'打开校园.html'),'utf8'));await p.waitForFunction(()=>game.state().ready,{timeout:90000});
  const result=await p.evaluate(()=>{
   const r={cuts:[],routes:[],station:[],stationWalls:[],joined:[],camera:game.state().camera};
   for(const[map,point]of[['wuchuan',[790,382]],['guoding',[1347,667]]]){game.setMap(map);r.cuts.push({map,valid:game.valid(...point),road:game.validRoad(...point),route:game.navigate({x:player.x,y:player.y},{x:point[0],y:point[1]}).length})}
   game.setMap('wuchuan');for(const q of[[867.4,382],[876.6,382],[872,380]])r.stationWalls.push({point:q,valid:valid(...q),road:validRoad(...q)});
   const ids=['W-ECON-FRONT','W-RESEARCH-EAST','W-METRO-EDGE','W-METRO-ACCESS','W-CANTEEN-BRANCH','W-DORM-LINK'];
   for(const id of ids){const road=m.roads.find(q=>q.id===id);for(const riding of[false,true]){game.placeActor(...road.points[0]);player.riding=riding;keys.clear();path=road.points.slice(1).map(([x,y])=>({x,y}));let n=0,bad=0;while(path.length&&n++<10000){game.step(.04);if(!validRoad(player.x,player.y)||!valid(player.x,player.y))bad++}r.routes.push({id,riding,bad,remaining:path.length,error:Math.hypot(player.x-road.points.at(-1)[0],player.y-road.points.at(-1)[1])})}}
   for(const riding of[false,true]){game.placeActor(...m.spawn);player.riding=riding;keys.clear();const goal=game.building('metro_station').entry;const segments=game.walkRoadTo(...goal);let n=0,bad=0;while(path.length&&n++<30000){game.step(.04);if(!validRoad(player.x,player.y)||!valid(player.x,player.y))bad++}r.station.push({riding,segments,bad,remaining:path.length,error:Math.hypot(player.x-goal[0],player.y-goal[1])})}
   const joined=game.building('w13');for(const e of joined.entrances){game.placeActor(...m.spawn);player.riding=false;keys.clear();const segments=game.walkRoadTo(...e.world);let n=0,bad=0;while(path.length&&n++<30000){game.step(.04);if(!validRoad(player.x,player.y)||!valid(player.x,player.y))bad++}r.joined.push({id:e.identity,segments,bad,remaining:path.length,error:Math.hypot(player.x-e.world[0],player.y-e.world[1])})}return r;
  });
  result.errors=errors;result.requests=requests;fs.writeFileSync(path.join(O,'修复专项通行验证.json'),JSON.stringify(result,null,2));
  assert(result.cuts.every(q=>!q.valid&&!q.road&&!q.route));
  assert(result.stationWalls.every(q=>!q.valid&&!q.road));
  assert(result.routes.every(q=>!q.bad&&!q.remaining&&q.error<.05));
  assert([...result.station,...result.joined].every(q=>q.segments&&!q.bad&&!q.remaining&&q.error<.05));assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
  for(const[id,v,file]of[['economics',200,'11-经济学院转折与接站道路.png'],['w13',135,'12-21与22连体楼.png'],['metro_station',50,'13-黄圈地铁站口.png'],['research',300,'14-科研三角外围道路.png']]){
   await p.evaluate(([id,v])=>{turnCampusCamera(12.5-T.MathUtils.radToDeg(az));player.riding=false;game.inspect(id,v);game.render()},[id,v]);await p.screenshot({path:path.join(O,file)});
  }
  console.log('PASS: removed areas blocked, six repaired roads foot/bike, station road-only arrival, both joined doors, offline');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
