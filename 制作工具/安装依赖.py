"""Install build dependencies in this recovered workspace only."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', action='store_true')
    args = parser.parse_args()
    tools = Path(__file__).resolve().parent
    root = tools.parent
    env = root / '.venv'
    if env.is_symlink():
        raise SystemExit('拒绝使用符号链接 .venv')
    if not env.exists():
        venv.EnvBuilder(with_pip=True).create(env)
    python = env / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    cache = root / '.cache'
    cache.mkdir(exist_ok=True)
    subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check', '--cache-dir', str(cache / 'pip'), '-r', str(tools / 'requirements.txt')], check=True)
    result = {'python': str(python), 'requirements': str(tools / 'requirements.txt')}
    if args.browser:
        npm = shutil.which('npm') or shutil.which('npm.cmd')
        if not npm:
            raise SystemExit('需要已安装 Node.js/npm 才能安装浏览器验证工具')
        subprocess.run([npm, 'install', '--prefix', str(tools), '--cache', str(cache / 'npm'), '--no-audit', '--no-fund'], check=True)
        node = shutil.which('node')
        if not node:
            raise SystemExit('找不到 node')
        system_browser = any(Path(p).is_file() for p in ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome'])
        if not system_browser:
            browser_env = os.environ.copy()
            browser_env.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(cache / 'ms-playwright'))
            subprocess.run([node, str(tools / 'node_modules/playwright/cli.js'), 'install', 'chromium'], env=browser_env, check=True)
        result['browserTools'] = str(tools)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
