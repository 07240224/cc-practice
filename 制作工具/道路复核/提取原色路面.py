from pathlib import Path
import argparse,json,sys,hashlib,base64,io
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont

P=Path(__file__).resolve().parents[2]
S=P/'道路俯视复核R5'/'校方高清辅助参考.jpg'
O=P/'道路俯视复核R5';O.mkdir(exist_ok=True)
F=json.loads((P/'占地复核图/轮廓与道路.json').read_text())
im=cv2.imread(str(S));h,w=im.shape[:2];sx=w/2048;sy=h/1143
rgb=im[:,:,::-1].astype(np.int16);lo=rgb.min(2);hi=rgb.max(2)
raw=((lo>=235)&(hi-lo<=20)).astype(np.uint8)
# Recover only the printed caption over the 111-gate paving; retain the original edge colours.
text_roi=np.zeros((h,w),np.uint8)
cv2.rectangle(text_roi,(round(730*sx),round(687*sy)),(round(835*sx),round(732*sy)),255,-1)
ink=((lo<115)&(hi-lo<60)&(text_roi>0)).astype(np.uint8)*255
ink=cv2.dilate(ink,np.ones((3,3),np.uint8))
recovered=cv2.inpaint(im,ink,3,cv2.INPAINT_TELEA)[:,:,::-1].astype(np.int16)
printed_floor=((recovered.min(2)>=235)&(recovered.max(2)-recovered.min(2)<=20)&(ink>0))
raw[printed_floor]=1
# The green-leaf promenade is a pale yellow tiled ROAD, not a gap between white roads.
promenade=np.zeros((h,w),np.uint8)
cv2.fillPoly(promenade,[np.round(np.array([[1215,474],[1533,474],[1533,498],[1215,501]])*[sx,sy]).astype(np.int32)],1)
r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
tiled=(r>=180)&(g>=180)&(b>=140)&(abs(r-g)<12)&(r-b>15)&(r-b<100)&(promenade>0)
raw[tiled]=1
poly=lambda points:np.round(np.array(points)*[sx,sy]).astype(np.int32)
site=np.zeros((h,w),np.uint8)
for c in F['campuses']:
 if c['id'] in ['W','G','D','A']:cv2.fillPoly(site,[poly(c['polygon'])],1)
# Margin is for anti-aliased original perimeter roads, never for widening road surfaces.
site=cv2.dilate(site,np.ones((int(sx*5)//2*2+1,)*2,np.uint8))
raw*=site
buildings=np.zeros_like(site)
for b in F['buildings']:
 cv2.fillPoly(buildings,[poly(b.get('referenceOutline',b)['outer'])],1)
# Keep every white connected fragment. Exclude only provably roof-enclosed islands or hairlines.
n,labels,stats,cent=cv2.connectedComponentsWithStats(raw,8)
dist=cv2.distanceTransform(raw,cv2.DIST_L2,5)
roads=raw.copy();excluded=[];kept=[]
for k in range(1,n):
 x,y,ww,hh,area=map(int,stats[k]);mask=labels[y:y+hh,x:x+ww]==k
 max_width=2*float(dist[y:y+hh,x:x+ww][mask].max())/sx
 outside=np.count_nonzero(mask & (buildings[y:y+hh,x:x+ww]==0))
 ground_bridge=(x/sx<1722 and (x+ww)/sx>1630 and y/sy<475 and (y+hh)/sy>422)
 reason='建筑内部独立白块' if outside==0 and not ground_bridge else '极细白线或印刷亮点' if max_width<.85 else None
 row={'id':k,'bbox':[x/sx,y/sy,(x+ww)/sx,(y+hh)/sy],'sourcePixels':area,'maxWidth':max_width}
 if reason:
  roads[y:y+hh,x:x+ww][mask]=0;excluded.append({**row,'reason':reason})
 else:kept.append(row)
Image.fromarray((roads*255).astype(np.uint8)).save(O/'道路原色面.png')
# Data renderer: draw geometry masks, not an edited copy of the reference image.
canvas=np.empty((h,w,3),np.uint8);canvas[:]=[226,232,225];canvas[site>0]=[154,176,147]
canvas[buildings>0]=[178,171,152]
for s in F['spaces']:
 if s['kind']=='water':cv2.fillPoly(canvas,[poly(s['polygon'])],(139,178,181))
# Location context only; road faces always remain on top.
for a in F['spaces']:
 if a['kind'] in ['sport','track']:cv2.fillPoly(canvas,[poly(a['polygon'])],(179,181,159))
for a in F['sports']:
 cv2.fillPoly(canvas,[poly(a['outer'])],(185,167,147))
 for hole in a.get('holes',[]):cv2.fillPoly(canvas,[poly(hole)],(157,181,145))
canvas[roads>0]=[255,255,250]
Image.fromarray(canvas).save(O/'核对图底层.png')
rgba=np.zeros((h,w,4),np.uint8);rgba[roads>0]=[255,255,250,255]
Image.fromarray(rgba).save(O/'道路面透明层.png')
(O/'路面分类核对.json').write_text(json.dumps({'source':'校方高清辅助参考.jpg','size':[w,h],'kept':kept,'excluded':excluded,'rawPixels':int(raw.sum()),'retainedPixels':int(roads.sum()),'method':'白色原色面及绿叶街浅色铺装；无中心线、无道路闭运算、无RDP简化；独立碎段逐项保留；建筑内白块与极细对象单列，架空连廊下T形地面面不按楼体删除。'},ensure_ascii=False,indent=2))
print('components',n,'kept',len(kept),'excluded',len(excluded),'white',raw.sum(),'retained',roads.sum())
