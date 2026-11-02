from pathlib import Path
import zipfile,hashlib,json,shutil
source=Path('/workspace/cc-practice/校园动作继承版')
destination=Path('/workspace/cc-practice-transfer')
name='campus-original-motion-v2.zip'
assert (source/'本轮独立复核.txt').is_file()
runtime=(source/'运行脚本.js').read_text()
html=(source/'打开校园.html').read_text()
assert html[html.rindex('<script>')+8:-16]==runtime
assert (source/'建筑建模.js').read_text() in runtime
baseline=json.loads((source/'动作继承基线.json').read_text())
assert hashlib.sha256((source/'场景数据.json').read_bytes()).hexdigest()==baseline['geometrySHA256']
for entry in baseline['sourceFiles']:
 assert hashlib.sha256((source/'原动作来源'/Path(entry['path']).name).read_bytes()).hexdigest()==entry['sha256']
target=destination/source.name
if target.exists():shutil.rmtree(target)
shutil.copytree(source,target)
archive=destination/'传送'/name
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for file in sorted(target.rglob('*')):
  if file.is_file():z.write(file,file.relative_to(destination))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert z.read(source.name+'/运行脚本.js').decode()==runtime
 assert z.read(source.name+'/场景数据.json')==(source/'场景数据.json').read_bytes()
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
description=f'''最新版：{name}

解压后打开“校园动作继承版/打开校园.html”。
WASD/方向键移动，Shift跑步，F骑车/下车；也可点击地面前往。
沿用原项目人物帧、走跑姿势、原自行车绘制动作。相对此前试玩版本，步行×3、跑步×10；骑车保留原项目骑行/步行速度比例。
本轮只修复动作、速度及相应的高速移动/跟镜/局部显隐。建筑与道路数据保持原版，后续方案见“建筑修复方案.txt”。
源文件哈希、动作验证及独立复核随包提供。

SHA256：{digest}

队友原始版本campus-map-windows.zip继续单独保留。
'''
for base in [destination/'传送',Path('/workspace/cc-practice/传送')]:
 base.mkdir(exist_ok=True)
 old=base/'campus-buildings-v1.zip'
 if old.exists():old.unlink()
 if base!=archive.parent:shutil.copy2(archive,base/name)
 (base/'最新版本说明.txt').write_text(description)
(destination/'.gitattributes').write_text('传送/*.zip filter=lfs diff=lfs merge=lfs -text\n"传送/campus-original-motion-v2.zip" -filter -diff -merge -text\n')
result={'file':name,'bytes':archive.stat().st_size,'sha256':digest,'runtimeSHA256':hashlib.sha256(runtime.encode()).hexdigest()}
Path('/workspace/scratch/original-motion/package_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
