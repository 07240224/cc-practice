#!/usr/bin/env python3
"""Restore the approved browser V3 and its editable production chain to a new workspace."""
import argparse
import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request

BASE_URL = 'https://raw.githubusercontent.com/07240224/cc-practice/main/%E4%BC%A0%E9%80%81/'
CAPSULE_MANIFEST_SHA = '8f8ed2c8fb47f5a8f2bf7a4bc9d4849ad499f5ddea96904b73ddc26b39a3ce2e'
CAPSULE_MANIFEST_BYTES = 42149
PACKAGES = [
    {'file':'campus-building-repair-v3.zip','bytes':27508585,'sha256':'b26d52297c03337f89bf272833a5368381a077636940497357ff372f01a409f4'},
    {'file':'campus-workspace-recovery-v1.zip','bytes':73977698,'sha256':'cf70f059bef7e9f32d06807c839d57d4f34a39870e9cc1b50b530d5a7a25de8c'},
]

def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1024*1024), b''):
            digest.update(data)
    return digest.hexdigest()

def reject_symlinks(path):
    for item in [path, *path.parents]:
        if item.is_symlink():
            raise ValueError('路径含符号链接，未写入：'+str(item))

def verify(root):
    reject_symlinks(root)
    manifest = root/'恢复完成.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('目标已存在但不是完整恢复目录，未覆盖；请使用新的 --target')
    data = json.loads(manifest.read_text(encoding='utf-8'))
    if data.get('format') != 1 or data.get('packages') != PACKAGES:
        raise ValueError('目录的恢复版本不匹配，未覆盖')
    inventory_path=root/'恢复资料清单.json'
    if not inventory_path.is_file() or inventory_path.is_symlink() or file_hash(inventory_path)!=CAPSULE_MANIFEST_SHA:
        raise ValueError('恢复资料清单不匹配，未覆盖')
    inventory=json.loads(inventory_path.read_text(encoding='utf-8'))['files']
    v3path=root/'制作工具'/'V3文件清单.json'
    reject_symlinks(v3path)
    if not v3path.is_file() or file_hash(v3path)!=inventory['制作工具/V3文件清单.json']['sha256']:
        raise ValueError('V3文件清单不匹配')
    expected_files=dict(inventory)
    expected_files.update(json.loads(v3path.read_text(encoding='utf-8'))['files'])
    expected_files['恢复资料清单.json']={'bytes':CAPSULE_MANIFEST_BYTES,'sha256':CAPSULE_MANIFEST_SHA}
    if data.get('files')!=expected_files:
        raise ValueError('恢复成员清单缺失或改变，未覆盖')
    failures=[]
    for name, expected in expected_files.items():
        rel = checked_member(name)
        path = root.joinpath(*rel.parts)
        reject_symlinks(path)
        if not path.is_file() or path.stat().st_size != expected['bytes'] or file_hash(path) != expected['sha256']:
            failures.append(name)
    if failures:
        raise ValueError('检测到缺失或已编辑文件，现有文件保持不变：'+', '.join(failures[:8]))
    return len(data['files'])

def checked_member(name):
    rel = PurePosixPath(name)
    if not name or '\\' in name or '\x00' in name or rel.is_absolute() or any(p in ('..','') for p in rel.parts) or (rel.parts and ':' in rel.parts[0]):
        raise ValueError('拒绝不安全ZIP成员：'+repr(name))
    return rel

def unpack(archive, root, seen, require_prefix=None):
    import zipfile
    count=0
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if sum(info.file_size for info in infos)>512*1024*1024:
            raise ValueError('恢复包展开大小异常')
        for info in infos:
            rel=checked_member(info.filename)
            if require_prefix and (not rel.parts or rel.parts[0]!=require_prefix):
                raise ValueError('运行包目录结构错误')
            mode=stat.S_IFMT(info.external_attr>>16)
            if mode not in (0,stat.S_IFREG,stat.S_IFDIR):
                raise ValueError('ZIP含符号链接或特殊文件')
            if info.is_dir():
                continue
            key=rel.as_posix().casefold()
            if key in seen:
                raise ValueError('恢复包含重复或重叠文件：'+rel.as_posix())
            seen.add(key)
            dest=root.joinpath(*rel.parts)
            dest.parent.mkdir(parents=True,exist_ok=True)
            with z.open(info) as src, dest.open('xb') as dst:
                shutil.copyfileobj(src,dst,1024*1024)
            count+=1
    return count

def install_new(source,target):
    if os.path.lexists(target):
        raise FileExistsError('目标已出现，未覆盖：'+str(target))
    if sys.platform.startswith('linux'):
        libc=ctypes.CDLL(None,use_errno=True)
        rename=getattr(libc,'renameat2',None)
        if rename is not None:
            rename.argtypes=[ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]
            rename.restype=ctypes.c_int
            if rename(-100,os.fsencode(source),-100,os.fsencode(target),1)==0:
                return
            error=ctypes.get_errno()
            if error not in (errno.ENOSYS,errno.EINVAL):
                raise OSError(error,os.strerror(error),str(target))
    if os.name=='nt':
        os.rename(source,target)
        return
    target.mkdir()
    try:
        for p in source.iterdir():
            if p.name=='恢复完成.json':
                continue
            q=target/p.name
            if p.is_dir():shutil.copytree(p,q)
            else:shutil.copy2(p,q)
        shutil.copy2(source/'恢复完成.json',target/'恢复完成.json')
    except BaseException:
        shutil.rmtree(target)
        raise

def fetch(spec,temp,local):
    dest=temp/spec['file']
    if local:
        source=local/spec['file']
        if source.stat().st_size!=spec['bytes'] or file_hash(source)!=spec['sha256']:
            raise ValueError('本地恢复包校验失败：'+spec['file'])
        return source
    print('下载 '+spec['file'],flush=True)
    request=urllib.request.Request(BASE_URL+spec['file'],headers={'User-Agent':'campus-workspace-restore/1'})
    with urllib.request.urlopen(request,timeout=90) as response,dest.open('xb') as out:
        total=0
        while True:
            block=response.read(1024*1024)
            if not block:break
            total+=len(block)
            if total>spec['bytes']:raise ValueError('下载大小超过记录值')
            out.write(block)
    if dest.stat().st_size!=spec['bytes'] or file_hash(dest)!=spec['sha256']:
        raise ValueError('下载包SHA256或大小不匹配：'+spec['file'])
    return dest

def setup(root,args):
    if args.setup_tools or args.browser:
        print('运行版和制作资料已恢复；现在安装本工作区的构建依赖。',flush=True)
        command=[sys.executable,str(root/'制作工具'/'安装依赖.py')]
        if args.browser:command.append('--browser')
        subprocess.run(command,check=True)

def main():
    if sys.version_info<(3,10):raise SystemExit('需要Python 3.10或更新版本')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',type=Path,default=Path.cwd()/'校园完整工作区')
    parser.add_argument('--verify',action='store_true',help='只核对已恢复目录，不写文件')
    parser.add_argument('--packages-dir',type=Path,help='使用本地已有的两个恢复ZIP，仍核对固定SHA256')
    parser.add_argument('--setup-tools',action='store_true',help='恢复后创建本目录.venv并安装构建依赖')
    parser.add_argument('--browser',action='store_true',help='另安装Playwright及需要的Chromium')
    args=parser.parse_args()
    target=args.target.expanduser().absolute()
    reject_symlinks(target)
    target=target.resolve()
    if args.verify or os.path.lexists(target):
        count=verify(target)
        print(json.dumps({'verified':True,'files':count,'root':str(target),'entry':str(target/'校园建筑修复版'/'打开校园.html')},ensure_ascii=False))
        if not args.verify:setup(target,args)
        return
    target.parent.mkdir(parents=True,exist_ok=True)
    reject_symlinks(target.parent)
    with tempfile.TemporaryDirectory(prefix='.campus-restore-',dir=target.parent) as name:
        temp=Path(name);work=temp/'workspace';work.mkdir();seen=set()
        for i,spec in enumerate(PACKAGES):
            archive=fetch(spec,temp,args.packages_dir)
            unpack(archive,work,seen,'校园建筑修复版' if i==0 else None)
        inventory=json.loads((work/'恢复资料清单.json').read_text(encoding='utf-8'))
        for name,item in inventory['files'].items():
            p=work.joinpath(*checked_member(name).parts)
            if p.stat().st_size!=item['bytes'] or file_hash(p)!=item['sha256']:
                raise ValueError('制作资料成员哈希不匹配：'+name)
        baseline=json.loads((work/'制作工具'/'已发布基线.json').read_text(encoding='utf-8'))
        for name,expected in baseline.items():
            if file_hash(work/'校园建筑修复版'/name)!=expected:
                raise ValueError('V3基线哈希不匹配：'+name)
        files={p.relative_to(work).as_posix():{'bytes':p.stat().st_size,'sha256':file_hash(p)} for p in sorted(work.rglob('*')) if p.is_file()}
        (work/'恢复完成.json').write_text(json.dumps({'format':1,'packages':PACKAGES,'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        install_new(work,target)
    count=verify(target)
    print(json.dumps({'restored':True,'files':count,'root':str(target),'entry':str(target/'校园建筑修复版'/'打开校园.html'),'tools':str(target/'制作工具')},ensure_ascii=False),flush=True)
    setup(target,args)

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        print('未覆盖原有文件。错误：'+str(exc),file=sys.stderr)
        sys.exit(1)
