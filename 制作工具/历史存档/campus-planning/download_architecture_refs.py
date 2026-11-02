from pathlib import Path
import urllib.request,urllib.parse,json,re,concurrent.futures
from PIL import Image
from io import BytesIO
from html import unescape
out=Path('/workspace/cc-practice/建筑制作/参考资料');index=json.loads((out/'网页图片索引.json').read_text());more={'learning':'https://intlstu.sufe.edu.cn/ch/2d/fb/c12468a208379/page.htm','library':'https://intlstu.sufe.edu.cn/ch/2d/fd/c12468a208381/page.htm','shops':'https://intlstu.sufe.edu.cn/ch/2e/04/c12468a208388/page.htm','campusTour':'https://www.sohu.com/a/710669474_121124732','campusTour2':'https://www.sohu.com/a/575779661_121124732'}
for key,url in more.items():
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:s=r.read().decode('utf8')
  (out/(key+'.html')).write_text(s);imgs=[]
  for m in re.finditer(r'<img\b[^>]*>',s,re.I):
   src=re.search(r'(?:data-src|src)=["\']([^"\']+)',m.group(),re.I)
   if not src:continue
   u=urllib.parse.urljoin(url,unescape(src.group(1)))
   if u.startswith('data:'):continue
   ctx=re.sub('<[^>]+>',' ',s[max(0,m.start()-100):m.end()+200]).strip()
   if u not in [i['url'] for i in imgs]:imgs.append({'url':u,'context':unescape(ctx)[:300]})
  index[key]={'url':url,'images':imgs};print(key,len(imgs),flush=True)
 except Exception as e:index[key]={'url':url,'error':str(e)}
(out/'网页图片索引.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
jobs=[]
for key,page in index.items():
 for i,im in enumerate(page.get('images',[])):
  u=im['url']
  good=('/article/images/'in u or '/publish/'in u or '/pph/image/'in u or 'sh.people.com.cn/mediafile/pic/'in u or 'sghimages.shobserver.com' in u or 'p0.itc.cn' in u or 'p1.itc.cn' in u or re.search(r'p[0-9]+\.itc\.cn',u))
  if good:jobs.append((key,i,im))
# A second independent front view of the research building and the gym architect's massing view.
jobs.extend([('researchAlt',0,{'url':'https://itcs-sufe.github.io/ITCS-Workshop2026/img/research-building.png'}),('gymDesign',0,{'url':'https://v5.laungee.com/jzgl/upload/image/20220725/20220725114044_982.png'})])
def get(job):
 key,i,im=job;name=f'{key}-{i:02d}.jpg';path=out/name
 try:
  if path.exists():return {**im,'key':key,'index':i,'file':name}
  req=urllib.request.Request(im['url'],headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as r:raw=r.read()
  pic=Image.open(BytesIO(raw));w,h=pic.size
  if w<280 or h<140:return None
  path.write_bytes(raw);return{**im,'key':key,'index':i,'file':name,'size':[w,h]}
 except Exception:return None
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:results=[x for x in ex.map(get,jobs) if x]
(out/'照片索引.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print('downloaded',len(results),'photos',flush=True)
