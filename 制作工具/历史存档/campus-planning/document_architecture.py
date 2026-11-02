from pathlib import Path
import json,html,shutil
from PIL import Image
O=Path('/workspace/cc-practice/校园建筑版');R=Path('/workspace/cc-practice/建筑制作/参考资料');data=json.loads((O/'场景数据.json').read_text());idx={a['file']:a for a in json.loads((R/'照片索引.json').read_text())};web=json.loads((R/'网页图片索引.json').read_text());(O/'核对照片').mkdir(exist_ok=True)
items=[
('academic_link','信管—人工智能—第三教学楼',['campusTour-38.jpg','campusTour2-19.jpg'],'以用户确认的左右关系为布局依据；连续六层楼体，统一横窗带；左、中入口窄雨棚，右侧三教宽红褐雨棚；武东连廊接右段。'),
('wudonglecture','武东路梯教',[],'实拍参考-lecture及连廊侧面、下方照片；独立六层体量、横向窗带、双柱入口、跨路上层连廊。'),
('finance','毓秀楼',['finance-09.jpg','finance2-04.jpg','campusTour-30.jpg'],'中部四层、两翼三层；五连拱、中央三列凹入竖窗带、两侧菱形窄窗饰、灰石墙。'),
('activity','学生中心／明德楼',['studentReal-00.jpg','campusTour2-15.jpg'],'近景三层红砖白框门面、宽雨棚双柱；远景高塔属于后方建筑，不计入本体。翼体按校园图组织。'),
('research','科研实验楼',['researchAlt-00.jpg','campusTour-39.jpg'],'高红砖塔楼、连续竖向窄窗、低层裙房及中央玻璃入口。'),
('bookstore','匡时书店',['bookstore-38.jpg','bookstore-40.jpg','bookstore-42.jpg'],'三层白墙，长条楼身与圆弧端头共用平屋面；端头三层拱门窗、小铁艺阳台；长边底层拱廊。位置采用武东100号040幢与原18号楼区域关系。'),
('guoding_gym','综合体育馆',['campus-03.jpg','campusTour2-13.jpg','gym-02.jpg'],'橙红悬挑上部、下收斜面、细长竖缝、低基座、端部水平格栅与屋顶天窗；不把效果图作实景证据。'),
('teaching1','第一教学楼',['campusEnglish-04.jpg','campusTour2-16.jpg'],'国定教学区奶油色墙、成组竖窗、红瓦边檐与屋顶退台；补一教二教上层连廊，廊下地面独立可通行。'),
('teaching2','第二教学楼',['campusEnglish-04.jpg','campusTour2-17.jpg','campusTour-22.jpg'],'四层体量，红瓦边檐、屋顶楼梯间、浅色立面、红瓦入口门廊；与一教的连廊独立制作。'),
('guodinglecture','国定梯教',['campusTour2-18.jpg','campusEnglish-03.jpg'],'低层浅墙、平屋顶、长窗组和入口雨棚；所在教学组团布局以用户初始校园图为准。'),
('statistics','统计与管理学院',['campusTour-34.jpg','campusTour2-27.jpg'],'灰褐砖、三层立面、中央山墙、窄竖窗与凹入口；不复制教学楼的长窗带。'),
('greenleaf_canteen','绿叶／第一食堂',['canteens-03.jpg','food22-00.jpg'],'两层浅墙、红坡屋顶、落地玻璃、上层叶形窗饰与小阳台。'),
('sufe_cafe','第六食堂／SUFE Café',['canteens-10.jpg','heritage-58.jpg','food26-16.jpg'],'橙色波纹金属、两层长条体量、底层通透玻璃、较高的玻璃端部；水塔在其后方独立制作。'),
('halal_canteen','第二／清真食堂',['food17-08.jpg','food22-04.jpg'],'两层砖楼、底层连续拱窗、上层横向长窗、端部外楼梯。'),
('third_canteen','第三／新食堂',['food17-20.jpg','food22-08.jpg'],'三层红砖楼、宽屋顶檐口、中央竖向玻璃厅、侧边开放楼梯阳台。'),
('cainiao_station','菜鸟驿站',['services23-12.jpg','services22-08.jpg'],'单层大厅、宽蓝檐、玻璃入口、两侧快递柜；第二张用于核对柜体，不计成第二个外观角度。'),
('library','英贤图书馆',['libraryAerial-00.jpg','campusTour2-21.jpg'],'七层主翼与五层附翼，保留围合内院；主高翼端面留大块白墙，嵌入竖向玻璃厅。两张航拍为同一构图，仅按一个角度计，官网简介用于核对层数。'),
('accounting','会计学院',['campusTour-31.jpg','campusTour2-32.jpg','accounting-129.jpg'],'浅暖色体量、上层方窗、下部横向凹入带、中央玻璃入口与台阶。两张长立面照片为同一构图。'),
('economics','经济学院',['campusTour-35.jpg','campusTour2-24.jpg'],'浅灰高楼、转角窗带、纵向主楼和侧翼；重复照片按一构图记。'),
('phoenix','凤凰楼',['campusTour-37.jpg','campusTour2-29.jpg'],'暖浅墙、中央大面积玻璃入口、规则方窗；重复照片按一构图记。'),
('enterprise','创业中心',['campusTour2-20.jpg','campusTour-16.jpg'],'三层红砖与玻璃门厅；第二张仅作同校区材料参照，不计作本栋角度。'),
('old_gate','复建老校门',['campusTour-15.jpg','campusTour2-05.jpg'],'位于武东入口与毓秀楼轴线之间；白石墙、中间贯通门洞、深色歇山屋顶、青绿彩梁、两侧六角窗；取消文字匾额。'),
('water_tower','水塔',['heritage-64.jpg','heritage17-14.jpg'],'国定校区咖啡厅后方；细圆柱、上扩锥碗、环形顶缘、轻栏杆和顶盖。'),
]
# Local team photos are actual photos; exclude its old generated sprites and game screenshots.
local=Path('/workspace/cc-practice/sufe-campus-adventure/docs/c1_wudong_link_20261030')
for fn in ['reference-lecture.jpg','reference-corridor-side.jpg','reference-corridor-under.jpg']:
 if (local/fn).exists():
  with Image.open(local/fn) as im:im.convert('RGB').save(O/'核对照片'/fn,quality=88)
manifest=[]
for id,title,files,features in items:
 refs=[]
 for fn in files:
  a=idx.get(fn)
  if not a or not (R/fn).exists():continue
  im=Image.open(R/fn).convert('RGB');im.thumbnail((1100,900));im.save(O/'核对照片'/fn,quality=88)
  refs.append(dict(file=fn,imageURL=a['url'],pageURL=web.get(a['key'],{}).get('url','https://itcs-sufe.github.io/ITCS-Workshop2026/' if a['key']=='researchAlt' else 'https://m.baike.com/wikiid/2114891045630780431')))
 if id=='wudonglecture':refs=[{'file':fn,'pageURL':'https://github.com/i-m-not-sufer/sufe-campus-adventure/tree/main/docs/c1_wudong_link_20261030','imageURL':'原工程实拍参考'} for fn in ['reference-lecture.jpg','reference-corridor-side.jpg','reference-corridor-under.jpg']]
 manifest.append(dict(id=id,title=title,features=features,references=refs))
(O/'原型核对索引.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
intro='''<!DOCTYPE html><html lang="zh-CN"><meta charset="utf-8"><title>校园建筑原型与落位核对</title><style>body{font:16px/1.75 system-ui,sans-serif;max-width:1440px;padding:24px;margin:auto;background:#f2f2e9;color:#30483f}h1{font-weight:500}article{margin:30px 0;padding:20px;background:#fffdf5;border:1px solid #d8dfce;border-radius:8px}section{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;max-width:32%}img{width:100%;max-height:340px;object-fit:contain}figcaption{font-size:12px}a{color:#456d62}.model{max-width:100%;width:100%;max-height:640px}small{color:#677769}</style><h1>校园建筑原型与落位核对</h1><p>建筑组团沿用用户确认的校园相对布局。模型统一采用35°轻俯视正交相机，楼层与角色共用尺度；不以占地框变形楼体。入口随真实模型立面接合。画面内不显示楼名。</p><p>主要建筑优先保留轮廓、层数、入口和窗带节奏；宿舍及办公背景按同类建筑简化，不逐室制作。照片用于原型核对；游戏建筑表面为无文字绘制材质，未把整楼照片贴成竖牌。</p><p><b>证据计数：</b>同图转发只算一个构图；内部照片只证明室内或柜体；效果图、旧游戏截图及生成素材不计实景。校园航拍与门口近景分别核对总体体量和入口。各条下列出实际用到的照片与来源。</p>'''
parts=[intro]
for a in manifest:
 parts.append('<article><h2>'+html.escape(a['title'])+'</h2><p>'+html.escape(a['features'])+'</p><img class="model" src="模型逐栋/'+a['id']+'.jpg"><section>')
 for r in a['references']:parts.append('<figure><img src="核对照片/'+r['file']+'"><figcaption><a href="'+html.escape(r['pageURL'])+'">来源页面</a> · <a href="'+html.escape(r['imageURL'])+'">原图</a></figcaption></figure>')
 parts.append('</section></article>')
parts.append('<p>完整75组建筑及两个校园构件见《建筑清单.json》和《模型逐栋》。武川与国定—武东保持独立围墙及双向传送。体育场保留整体长方形围墙。</p></html>');(O/'原型核对.html').write_text(''.join(parts))
(O/'建筑清单.json').write_text(json.dumps([{'id':m['id'],'name':m['label'],'map':m['map'],'lot':m['lot'],'style':m['kind'],'center':m['center'],'rotation':m['rotation'],'entry':m['entry'],'arrival':m['arrival'],'tier':m['detail'],'placementShift':m['placementShift']} for m in data['models']],ensure_ascii=False,indent=2))
(O/'使用说明.txt').write_text('校园建筑版\n\n解压后双击“打开校园.html”。主程序自带模型、材质、人物与Three.js，离线运行，无需Godot、Node或本地服务器。\nWASD／方向键行走；Shift奔跑；点击地面自动前往；E在传送门旁切换校区。\n右下角“武川”“国定·武东”可直接切换两张地图；全景／跟随切换相机取景。\n建筑内外使用同一正交投影；遇前景遮挡，角色周围局部让出视野。\n模型不显示建筑名称；原型与照片见“原型核对.html”。\n本次为校园外部建筑与道路行走版本，室内剧情、教学任务等沿用原项目后续接入。\n')
(O/'制作与检查说明.txt').write_text('本轮制作\n\n1. 以已接受正交底图为基础，两张地图、围墙和武川路111号传送保持。\n2. 信管—人工智能—三教合为连续楼体，人工智能位于1154,939；三教在右，连廊接右段。\n3. 主体不从旧占地轮廓直接拉伸，模型部件共用尺度，按实际体量小幅调整落位。\n4. 所有建筑文字均取消。主要地点保留独立入口与原型特征，宿舍、办公楼简化。\n5. 真实实体重算碰撞与导航；预留框不参与碰撞。屋顶、连廊等上层结构不封死地面。\n6. 一教二教补上层连廊及廊下步道。十九号楼保留西开口、院内独立楼体。\n7. 地形小改：三连体南侧道路直线微移；一二教间补直线步道；门前铺装按真实入口连接。\n8. 屋面和窗格在统一局部坐标绘制，不能采用非等比压扁或拉长。\n\n场景中的楼名关闭；本目录资料标题用于核对原型，不绘入游戏。\n')
print('manifest',len(manifest),'source photos',len(list((O/'核对照片').glob('*.jpg'))))
