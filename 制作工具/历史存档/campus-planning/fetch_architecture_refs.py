from pathlib import Path
import urllib.request,urllib.parse,re,json,concurrent.futures
from html import unescape
from PIL import Image
from io import BytesIO
out=Path('/workspace/cc-practice/建筑制作/参考资料')
pages={
'campus':'https://www.sufe.edu.cn/fxsc/list.htm',
'canteens':'https://m.thepaper.cn/newsDetail_forward_28589772',
'bookstore':'https://sh.people.com.cn/n2/2024/1118/c134768-41045798.html',
'bookstore2':'https://web.shobserver.com/sgh/detail?id=1582785',
'gym':'https://sports.sufe.edu.cn/63/a8/c1930a222120/page.htm',
'research':'https://lab.sufe.edu.cn/syzxjs/list.htm',
'finance':'https://sof.sufe.edu.cn/d5/f9/c7109a120313/page.htm',
'finance2':'https://sof.sufe.edu.cn/50/ed/c7109a217325/page.htm',
'bookstore3':'https://gongkai.sufe.edu.cn/74/58/c227a226392/page.htm',
}
def get(item):
 key,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=40) as r:raw=r.read()
  for enc in ['utf-8','gb18030']:
   try:s=raw.decode(enc);break
   except UnicodeError:continue
  (out/(key+'.html')).write_text(s)
  imgs=[]
  for m in re.finditer(r'<img\b[^>]*>',s,re.I):
   tag=m.group();cand=re.findall(r'(?:src|data-src|data-original)=["\']([^"\']+)',tag,re.I)
   for src in cand:
    if src.startswith('data:'):continue
    src=urllib.parse.urljoin(url,unescape(src));alt=re.search(r'alt=["\']([^"\']*)',tag,re.I)
    around=re.sub('<[^>]+>',' ',s[max(0,m.start()-120):m.end()+180])
    if src not in [i['url'] for i in imgs]:imgs.append({'url':src,'alt':alt.group(1) if alt else '', 'context':unescape(around).strip()[:280]})
  print(key,len(imgs),flush=True)
  return key,{'url':url,'images':imgs}
 except Exception as e:return key,{'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:result=dict(ex.map(get,pages.items()))
(out/'网页图片索引.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
