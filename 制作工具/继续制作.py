"""Build into a NEW output directory. Approved V3 and its evidence remain intact."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verify-reproduction', action='store_true')
    args = parser.parse_args()
    tools = Path(__file__).resolve().parent
    root = tools.parent
    baseline = root / '校园建筑修复版'
    out = (args.output or root / '工作输出' / '校园建筑修复版').absolute()
    for p in [out, *out.parents]:
        if p.is_symlink():
            raise SystemExit('输出路径包含符号链接，拒绝写入')
    out = out.resolve()
    if out.exists():
        raise SystemExit('输出已存在，未更改任何文件；请指定新的 --output')
    protected = [root / n for n in ['校园建筑修复版', '校园动作继承版', '校园建筑版', '制作工具', '占地复核图', '图片发送助手', '参考资料', '传送']]
    if out == root or any(out == p or p in out.parents or out in p.parents for p in protected):
        raise SystemExit('拒绝覆盖或嵌入已发布基线、工具或资料目录')
    if not (baseline / '打开校园.html').is_file():
        raise SystemExit('缺少V3基线，请先运行恢复脚本')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.campus-build-', dir=out.parent) as tmp:
        staging = Path(tmp) / 'output'
        shutil.copytree(baseline, staging)
        # Old screenshots and approvals must never certify a newly edited build.
        for folder in ['模型核对']:
            shutil.rmtree(staging / folder, ignore_errors=True)
        for p in staging.glob('*.png'):
            if p.name[:2].isdigit():
                p.unlink()
        for name in ['本轮独立复核.txt', '通行验证.json', '本轮修复记录.json', '道路与落位检查.json', '原型对照.html', '动作继承记录.json', '动作保留校验.json']:
            (staging / name).unlink(missing_ok=True)
        env = os.environ.copy()
        env['CAMPUS_WORK_ROOT'] = str(root)
        env['CAMPUS_OUTPUT_DIR'] = str(staging)
        for name in ['prepare_scene.py', 'build_runtime.py']:
            subprocess.run([sys.executable, str(tools / 'building-repair' / name)], env=env, check=True)
        frozen = json.loads((tools / '已发布基线.json').read_text(encoding='utf-8'))
        actual = {name: hashlib.sha256((staging / name).read_bytes()).hexdigest() for name in frozen}
        same = actual == frozen
        if args.verify_reproduction and not same:
            raise SystemExit('重现哈希不一致，未写入目标；差异：' + ', '.join(n for n in frozen if actual[n] != frozen[n]))
        (staging / '构建结果.json').write_text(json.dumps({'reproducesPublishedV3': same, 'sha256': actual, 'validation': '新输出不继承原版验收记录；编辑后的版本须重新验证并复核。'}, ensure_ascii=False, indent=2), encoding='utf-8')
        # The target has not existed. Linux renameat2 is used by the restore module when available.
        from 恢复支持 import install_new_directory
        install_new_directory(staging, out)
    print(json.dumps({'output': str(out), 'reproducesPublishedV3': same, 'entry': str(out / '打开校园.html')}, ensure_ascii=False))

if __name__ == '__main__':
    main()
