"""把修改后的场景数据与运行脚本写回离线HTML。只用Python标准库。"""
from pathlib import Path
import json
root=Path(__file__).resolve().parent
p=root/'打开校园.html'
s=p.read_text(encoding='utf-8')
a=s.index('const DATA=')+len('const DATA=');b=s.index(';const ASSETS=',a)
s=s[:a]+json.dumps(json.loads((root/'场景数据.json').read_text(encoding='utf-8')),ensure_ascii=False,separators=(',',':'))+s[b:]
a=s.rindex('<script>')+len('<script>');s=s[:a]+(root/'运行脚本.js').read_text(encoding='utf-8')+'</script></html>'
p.write_text(s,encoding='utf-8');print('已更新打开校园.html')
