from pathlib import Path
import json,hashlib,zipfile,shutil
O=Path('/workspace/cc-practice/校园建筑修复版');P=Path('/workspace/cc-practice-transfer');name='campus-building-repair-v3.zip'
r=(O/'运行脚本.js').read_text();h=(O/'打开校园.html').read_text();assert h[h.rindex('<script>')+8:-16]==r
assert (O/'建筑建模.js').read_text() in r
start=h.index('const DATA=')+len('const DATA=');end=h.index(';const ASSETS=',start);assert json.loads(h[start:end])==json.loads((O/'场景数据.json').read_text())
checks=json.loads((O/'通行验证.json').read_text());assert len(checks['arrivals'])==77 and len(checks['roadArrivals'])==29
assert all(a['segments'] and not a['remaining'] and a['error']<.05 and not a['invalid'] for a in checks['arrivals'])
assert all(a['segments'] and not a['remaining'] and a['error']<.05 and not a['offRoad'] for a in checks['roadArrivals'])
assert not checks['errors'] and not checks['requests'];assert (O/'本轮独立复核.txt').is_file()
for source in json.loads((O/'动作保留校验.json').read_text())['sourceFiles']:assert hashlib.sha256((O/'原动作来源'/Path(source['path']).name).read_bytes()).hexdigest()==source['sha256']
T=P/O.name
if T.exists():shutil.rmtree(T)
shutil.copytree(O,T)
archive=P/'传送'/name
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(T.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(P))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
explain=f'''最新版：{name}

解压后打开“校园建筑修复版/打开校园.html”，离线可玩。
WASD/方向键移动，Shift跑步，F骑车/下车；Q/R转向全校镜头，V门前视角。点击地面自动前往。
科研楼整组朝向、裙房与门厅重建，楼前道路西接G8、东接G18R。27组重点建筑使用各自立面规则，29个入口与道路明确衔接。
两张围墙地图、111号双向传送、连廊和体育场围墙保留；人物走跑和骑车动作、步行13.2/跑步80/骑车35.357142857保持。
实景对照、运行画面、77处到达检查、29入口道路专用检查及独立复核随包提供。

SHA256：{sha}

队友原始地图campus-map-windows.zip单独保留。
'''
for folder in [P/'传送',Path('/workspace/cc-practice/传送')]:
 old=folder/'campus-original-motion-v2.zip'
 if old.exists():old.unlink()
 if folder!=archive.parent:shutil.copy2(archive,folder/name)
 (folder/'最新版本说明.txt').write_text(explain)
(P/'.gitattributes').write_text('传送/*.zip filter=lfs diff=lfs merge=lfs -text\n"传送/campus-building-repair-v3.zip" -filter -diff -merge -text\n')
result=dict(file=name,size=archive.stat().st_size,sha256=sha,entries=len(list(T.rglob('*'))),runtimeSHA256=hashlib.sha256(r.encode()).hexdigest());Path('/workspace/scratch/building-repair/package-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
