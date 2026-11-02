from pathlib import Path
import json,hashlib,shutil
from zipfile import ZipFile,ZIP_DEFLATED
src=Path('/workspace/cc-practice/地图规划')
assert (src/'独立规划复核.json').exists()
files=sorted(p for p in src.iterdir() if p.is_file() and p.name!='交付校验.json')
manifest={'edition':'P01','date':'2026-11-01','scope':'只制作布局规划，无建筑美术；原始游戏未修改','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(src/'交付校验.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');files.append(src/'交付校验.json')
tmp=Path('/tmp/campus-layout-plan-P01.zip')
with ZipFile(tmp,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.name)
with ZipFile(tmp) as z:
 assert z.testzip() is None
 for name,h in manifest['files'].items():assert hashlib.sha256(z.read(name)).hexdigest()==h
for root in [Path('/workspace/cc-practice'),Path('/workspace/cc-practice-transfer')]:
 shutil.copy2(tmp,root/'传送'/tmp.name)
for p in files:
 target=Path('/workspace/cc-practice-transfer/地图规划')/p.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
print(json.dumps({'zip':tmp.name,'bytes':tmp.stat().st_size,'sha256':hashlib.sha256(tmp.read_bytes()).hexdigest(),'entries':len(files)},ensure_ascii=False))
