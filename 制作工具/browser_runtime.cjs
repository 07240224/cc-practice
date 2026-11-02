const fs = require('node:fs');
const path = require('node:path');
process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve(__dirname, '../.cache/ms-playwright');
let playwright;
try { playwright = require('playwright'); }
catch { throw new Error('缺少 Playwright：在制作工具目录执行 npm install，或运行 安装依赖.py --browser。'); }
function browserExecutable() {
  if (process.env.CAMPUS_CHROMIUM) {
    if (!fs.existsSync(process.env.CAMPUS_CHROMIUM)) throw new Error('CAMPUS_CHROMIUM 指定的文件不存在');
    return process.env.CAMPUS_CHROMIUM;
  }
  for (const p of ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome']) {
    if (fs.existsSync(p)) return p;
  }
  const bundled = playwright.chromium.executablePath();
  if (fs.existsSync(bundled)) return bundled;
  throw new Error('缺少浏览器：运行 安装依赖.py --browser，或设置 CAMPUS_CHROMIUM。');
}
module.exports = { chromium: playwright.chromium, browserExecutable };
