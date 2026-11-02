from pathlib import Path
import urllib.request,urllib.parse,json,re,concurrent.futures
from PIL import Image
from io import BytesIO
from html import unescape
out=Path('/workspace/cc-practice/建筑制作/参考资料');index=json.loads((out/'网页图片索引.json').read_text());photos=json.loads((out/'照片索引.json').read_text());seen={x['url'] for x in photos}
pages={'food22':'https://www.sohu.com/a/580347882_120731724','food17':'https://www.sohu.com/a/166937445_784785','food26':'https://www.sohu.com/a/1060332483_121124732'}
def pageget(kv):
 key,url=kv
 try:
  s=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read().decode('utf8');(out/(key+'.html')).write_text(s);imgs=[]
  for m in re.finditer('<img[^>]+>',s):
   for src in re.findall(r'(?:src|data-src|data-original)=[\"\']([^\"\']+)',m[0]):
    u=urllib.parse.urljoin(url,unescape(src))
    if u.startswith('data:'):continue
    context=re.sub('<[^>]+>',' ',s[max(0,m.start()-200):m.end()+220]);imgs.append({'url':u,'context':re.sub(r'\s+',' ',unescape(context))})
  return key,{'url':url,'images':imgs}
 except Exception as e:return key,{'url':url,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:more=dict(ex.map(pageget,pages.items()))
index.update(more)
jobs=[]
for key,page in more.items():
 for i,im in enumerate(page.get('images',[])):
  if im['url'] not in seen and ('/article/images/'in im['url'] or re.search(r'[pq][0-9]+\.itc\.cn',im['url']) or '20240328'in im['url'] or 'cdn.sohucs.com'in im['url']):jobs.append((key,i,im))

def get(job):
 key,i,im=job;file=f'{key}-{i:02d}.jpg';p=out/file
 try:
  raw=p.read_bytes() if p.exists() else urllib.request.urlopen(urllib.request.Request(im['url'].replace('http://','https://'),headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read();pic=Image.open(BytesIO(raw));w,h=pic.size
  if w<280 or h<140:return
  p.write_bytes(raw);return {**im,'key':key,'file':file,'size':[w,h]}
 except:pass
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:result=[r for r in ex.map(get,jobs) if r]
photos.extend(result);(out/'照片索引.json').write_text(json.dumps(photos,ensure_ascii=False,indent=2));(out/'网页图片索引.json').write_text(json.dumps(index,ensure_ascii=False,indent=2));print('new',len(result))
