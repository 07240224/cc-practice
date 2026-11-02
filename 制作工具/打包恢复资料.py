"""Package the latest runtime or its production inputs; refuse existing output files."""
from pathlib import Path
import argparse, hashlib, json, zipfile

ROOT = Path(__file__).resolve().parent.parent
def digest(p):
    return dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--kind', choices=['runtime','recovery'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    if args.output.exists():raise SystemExit('输出已存在，未覆盖')
    selected={}
    def add(p,name=None):
        selected[name or p.relative_to(ROOT).as_posix()]=p
    if args.kind=='runtime':
        for p in (ROOT/'校园道路修复版').rglob('*'):
            if p.is_file():add(p)
        inventory={'format':1,'files':{n:digest(p) for n,p in sorted(selected.items())}}
        (ROOT/'制作工具/V4文件清单.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    else:
        for p in (ROOT/'制作工具').rglob('*'):
            if p.is_file() and not any(x in ['node_modules','__pycache__'] for x in p.parts):add(p)
        groups={
          '校园动作继承版':['打开校园.html','运行脚本.js','建筑建模.js','场景数据.json','动作继承基线.json','原动作图集.png','原动作帧表.json','更新内嵌版本.py','动作继承说明.txt'],
          '校园建筑版':['打开校园.html','运行脚本.js','建筑建模.js','场景数据.json','原型核对索引.json'],
          '占地复核图':['轮廓与道路.json','核对说明.txt','独立名称锚点.csv'],
        }
        for folder,names in groups.items():
            for name in names:add(ROOT/folder/name)
        for folder in ['校园动作继承版/原动作来源','校园建筑版/核对照片','图片发送助手']:
            for p in (ROOT/folder).rglob('*'):
                if p.is_file():add(p)
        for name in ['原工程固定版本.json','.gitignore','后续建筑与道路整改方案.md']:add(ROOT/name)
        add(ROOT/'传送/新对话接续上下文.md','新对话接续上下文.md')
        inventory={'format':1,'files':{n:digest(p) for n,p in sorted(selected.items())},'scope':'V4有效制作链及历史V3输入；两个完整运行版本另取固定ZIP。'}
    manifest=(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,'x') as archive:
        def write(name,content):
            info=zipfile.ZipInfo(name,date_time=(2026,11,2,0,0,0));info.external_attr=0o100644<<16
            archive.writestr(info,content,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        for name,p in sorted(selected.items()):write(name,p.read_bytes())
        if args.kind=='recovery':write('恢复资料清单.json',manifest)
    with zipfile.ZipFile(args.output) as archive:
        assert archive.testzip() is None
        count=len(archive.infolist())
    assert args.output.stat().st_size<100*1024*1024, '超过GitHub单文件上限'
    result={'file':args.output.name,**digest(args.output),'files':count}
    if args.kind=='recovery':result.update(manifestSHA256=hashlib.sha256(manifest).hexdigest(),manifestBytes=len(manifest))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
