from pathlib import Path
import os
ROOT = Path(os.environ.get('CAMPUS_WORK_ROOT', str(Path(__file__).resolve().parents[2]))).resolve()
OUTPUT = Path(os.environ.get('CAMPUS_OUTPUT_DIR', str(ROOT / '工作输出' / '校园建筑修复版'))).resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)
from pathlib import Path
import json, hashlib, shutil, html
from PIL import Image, ImageDraw, ImageFont
O = OUTPUT
B = ROOT / '校园动作继承版'
OLD = ROOT / '校园建筑版'
D = json.loads((O / '场景数据.json').read_text(encoding='utf-8'))
hash = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for p in O.glob('*-检查.png'):
    p.unlink()
(O / '预览错误.json').unlink(missing_ok=True)
source = json.loads((B / '动作继承基线.json').read_text(encoding='utf-8'))
source['sourceRepo'] = 'https://github.com/i-m-not-sufer/sufe-campus-adventure'
source['previousSceneSHA256'] = source.pop('geometrySHA256')
source.pop('runtimeSHA256', None)
a = (B / '运行脚本.js').read_text(encoding='utf-8')
b = (O / '运行脚本.js').read_text(encoding='utf-8')
adapter = lambda s: s[s.index('const SOURCE_MOTION='):s.index('window.game=')]
assert adapter(a) == adapter(b)
source['motionAdapterSHA256'] = hashlib.sha256(adapter(b).encode()).hexdigest()
source['atlasSHA256'] = hash(O / '原动作图集.png')
source['atlasUnchanged'] = hash(O / '原动作图集.png') == hash(B / '原动作图集.png')
source['frameTableUnchanged'] = (O / '原动作帧表.json').read_bytes() == (B / '原动作帧表.json').read_bytes()
(O / '动作保留校验.json').write_text(json.dumps(source, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
(O / '动作继承基线.json').unlink(missing_ok=True)
record = json.loads((ROOT / '校园建筑修复版' / '动作继承记录.json').read_text(encoding='utf-8'))
record['geometrySHA256'] = hash(O / '场景数据.json')
record['scope'] = 'V4修正局部校地边界、21/22连体、经济学院转折与接站路、科研前三角；原人物素材、走跑帧序、自行车绘制动作、位移速度与体力规则保持。'
(O / '动作继承记录.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
(O / '动作继承说明.txt').write_text('人物与自行车继续沿用原项目。四向帧、走跑姿势、7步/秒与[0,1,2,1]、停车帧、原自行车蹬踏、体力规则保持。\n步行13.2、跑步80；相较动作修改前的试玩版分别为3倍和10倍。骑车35.357142857。\n原图集、帧表和动作适配段与上一动作修复版完全一致；四份原动作文件的SHA256见“动作保留校验.json”。\n本包已更新建筑、入口、道路及全校镜头转向；场景数据为本轮版本。\n', encoding='utf-8', newline='\n')
(O / '使用说明.txt').write_text('校园道路与布局修复 V4\n\n解压后打开“打开校园.html”，离线运行，无需安装Godot或启动服务器。\n\nWASD/方向键：移动。Shift：跑步。F：骑车/下车。点击地面：自动前往；起终点在道路/步道上时，优先只沿道路/步道寻路。\nQ/R：转动全校镜头。V或“门前视角”：朝最近入口正面取景，继续正常行走与骑车。\nE：在111号传送门旁切换校区；靠近传送门也可自动切换。武川与国定—武东保持独立地图。\n+/-缩放；“全景/跟随”切换范围。\n\n本轮修复：科研南侧凸地；21/22连体及双入口；蓝圈北部裁区；黄圈站口与接路；经济学院真实转折/分支；科研前三角外围路网。\n11—14截图对应这四处近景，09是武川全景，10为俯视核对图。其他建筑与路网的继续整改方案见“后续建筑与道路整改方案.md”。\n\n角色素材、动作节奏、骑车和速度保持：步行13.2、跑步80、骑车35.357142857。游戏楼体无名称。\n编辑场景数据.json或运行脚本.js后，可用更新内嵌版本.py更新离线HTML。\n', encoding='utf-8', newline='\n')
features = {'research': '整组25°；红砖外框与连续窄窗槽采用真实进深；恢复完整西侧低翼与深凹门厅。西北侧7宽前路接G8与G18R。', 'activity': '三层连翼，窄红砖柱与白墙窗间板；西侧宽门廊接入主步行轴。', 'academic_link': '左信管、中人工智能、右三教保持同一连续楼身；三个独立入口，右侧连廊保留。灰褐砖、横窗带和单柱/宽雨棚分别制作。', 'wudonglecture': '六层灰褐砖体量、横向窗带与内凹门厅；双柱雨棚在凹入空间内，连廊及廊下通路保留。', 'finance': '中部较高，两侧较低；五连拱、中央三列凹窗带与菱形窗饰，灰石墙。门前步行轴穿过老校门。', 'statistics': '保留中央山墙、窄成对竖窗、灰褐砖和凹入口，采用自身窗组。', 'greenleaf_canteen': '二层叶形窗、一层普通玻璃窗及入口；红坡屋面与中央小阳台保留。', 'halal_canteen': '两层浅褐砖、连续底层拱廊、上部长窗和平屋面；保留端部外楼梯，入口朝北接宿舍南侧道路。', 'auth': '', 'sufe_cafe': '两层橙红金属长楼、下部大玻璃与较高玻璃端厅；水塔独立保留。', ' third_canteen': '', ' third': '', ' third_canteen_': '', ' thirdCanteen': '', ' thirdcanteen': '', ' thirdcanteen2': '', ' third_canteen_v3': '', 'cainiao_station': '单层玻璃服务大厅、宽蓝檐及两侧柜体；正面朝校内道路，前场接入内侧通路。', 'library': '七层主高翼与五层附翼连接完整，保留内院；白色端墙、大玻璃厅使用独立分格，屏蔽其后的普通窗框。', 'accounting': '上下体量退进；上部方窗与窄竖窗、下部凹廊及深玻璃门厅分别组织，步道从真实门厅引出。', 'phoenix': '两侧翼与中央通高玻璃厅、上部窄窗；窗台与玻璃厅分开，保持通高入口尺度。', 'economics': '高低侧翼、白墙、转角窄窗带及分组办公室窗；屋面与立面比例统一。', 'enterprise': '三层红砖与水平窗带；独立金属入口框架。', 'guoding_gym': '保留橙红悬挑上部、斜收面、竖缝、端部格栅、基座及天窗。', 'bookstore': '白墙连续圆弧端头、长边拱廊和端头小阳台；侧门从东侧步道接入。', 'guodinglecture': '低层浅墙，分组长窗和独立门厅。', ' teaching1': ''}
features['third_canteen'] = '三层红砖；左侧真凹廊、楼板与侧壁，中央窄高玻璃厅，右侧实墙和角窗，统一宽檐口。'
features['teaching1'] = '浅墙、成组成列竖窗与红瓦边檐；门廊及一二教上层连廊独立制作，廊下可通行。'
features['teaching2'] = '同一教学组团材质，使用长楼开间与宽门廊；四根落地柱给中央入口留通道。'
features['teaching4'] = '按第四教学楼实景保留浅墙、四层窗组、红瓦屋檐与宽门廊，采用第四教学楼照片作本栋依据。'
for id in ['wuchuan_pool', 'exchange', 'wuchuan_hall', 'badminton', 'wuchuan_canteen']:
    features[id] = '保留初始校园图位置，按低层场馆/服务楼简化；入口和前场明确接入对应道路。'
index = json.loads((OLD / '原型核对索引.json').read_text(encoding='utf-8'))
refs = {a['id']: a for a in index}
refs['teaching4'] = {'title': '第四教学楼', 'references': [{'file': 'campusTour2-17.jpg', 'pageURL': 'https://www.sohu.com/a/575779661_121124732', 'imageURL': 'https://p0.itc.cn/q_70/images03/20220810/902aa30627764ae8a45088c2fc90d8da.jpeg'}]}
for id in ['teaching1', 'teaching2']:
    refs[id]['references'] = [r for r in refs[id]['references'] if r['file'] != 'campusTour2-17.jpg']
photo = O / '核对照片'
photo.mkdir(exist_ok=True)
manifest = []
for m in D['models']:
    if not m.get('facadeProfile'):
        continue
    entry = refs.get(m['id'], {'title': m['label'], 'references': []})
    rs = entry['references']
    for r in rs:
        if (OLD / '核对照片' / r['file']).is_file():
            shutil.copy2(OLD / '核对照片' / r['file'], photo / r['file'])
    manifest.append(dict(id=m['id'], title=entry['title'], changes=features.get(m['id'], ''), references=rs))
(O / '原型对照索引.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
s = ['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>建筑与道路修复核对</title><style>body{font:16px/1.8 system-ui;max-width:1300px;margin:auto;padding:28px;background:#eeefe5;color:#304c40}article{background:#fffdf3;border:1px solid #cdd6c6;padding:22px;margin:24px 0;border-radius:8px}img{max-width:100%;max-height:650px}.sources{display:flex;gap:12px;flex-wrap:wrap}.sources figure{width:31%;margin:0}.sources img{width:100%;height:230px;object-fit:contain}a{color:#3a6b61}</style><h1>建筑与道路修复核对</h1><p><a href="打开校园.html">进入可行走地图</a> · <a href="10-俯视布局核对.png">俯视布局</a></p><p>统一35°正交投影；楼体无名称。Q/R转向全校，V朝最近入口取景；角色位置不变，继续正常行走/骑车。原动作与速度保留。</p><p>本页分别列出模型与实景，重复构图按同一证据；简化场馆使用初始校园图位置与低层体量，不冒充逐栋实景精细模型。</p>']
for a in manifest:
    s.append('<article><h2>' + html.escape(a['title']) + '</h2><p>' + html.escape(a['changes']) + '</p><img src="模型核对/' + a['id'] + '.png"><div class="sources">')
    for r in a['references']:
        s.append('<figure><img src="核对照片/' + r['file'] + '"><figcaption><a href="' + html.escape(r['pageURL']) + '">来源页面</a> · <a href="' + html.escape(r['imageURL']) + '">原图</a></figcaption></figure>')
    s.append('</div></article>')
s.append('</html>')
(O / '原型对照.html').write_text(''.join(s), encoding='utf-8', newline='\n')
scale = 1.02
image = Image.new('RGB', (2048, 1200), '#e9eee7')
q = ImageDraw.Draw(image)
pt = lambda a: (a[0] * scale - 20, a[1] * scale + 20)
fontpath = str(ROOT / '制作工具' / 'fonts' / 'NotoSansCJK-Regular.ttc')
font = ImageFont.truetype(fontpath, 12)
titlefont = ImageFont.truetype(fontpath, 25)
for mid, mp in D['maps'].items():
    for r in mp['site']:
        q.polygon([pt(p) for p in r['outer']], fill='#cdd8c4', outline='#637566', width=2)
    for space in D['spaces']:
        if space['kind'] in ['water', 'sport'] and any((min((p[0] for p in r['outer'])) <= space['polygon'][0][0] <= max((p[0] for p in r['outer'])) for r in mp['site'])):
            q.polygon([pt(p) for p in space['polygon']], fill='#9abbb8' if space['kind'] == 'water' else '#bcbca7')
    for key, color in [('paving', '#dfdcc7'), ('asphalt', '#fcfcf6')]:
        mask = Image.new('L', image.size)
        mq = ImageDraw.Draw(mask)
        for r in mp[key]:
            mq.polygon([pt(p) for p in r['outer']], fill=255)
            for h in r['holes']:
                mq.polygon([pt(p) for p in h], fill=0)
        image.paste(color, (0, 0), mask)
    if mid == 'guoding':
        for sport in D['sports']:
            q.polygon([pt(p) for p in sport['outer']], fill='#b99988')
            for h in sport.get('holes', []):
                q.polygon([pt(p) for p in h], fill='#b5c39b', outline='#f4f1df', width=2)
        for wall in D['sportsEnclosure']['wallSegments']:
            q.line([pt(p) for p in wall], fill='#657364', width=3)
    for m in [a for a in D['models'] if a['map'] == mid]:
        for r in m['actualBuildingFootprint']:
            q.polygon([pt(p) for p in r['outer']], fill='#b1997c' if m.get('facadeProfile') else '#9fa99e', outline='#607565', width=1)
        if m.get('facadeProfile'):
            a = next((a for a in manifest if a['id'] == m['id']))
            x, y = pt(m['center'])
            q.text((x, y), a['title'][:8], font=font, fill='#253f31', anchor='mm')
    for a in mp['approaches']:
        q.line([pt(p) for p in a['points']], fill='#b4b18e', width=2)
    q.ellipse([pt([mp['portal'][0] - 5, mp['portal'][1] - 5]), pt([mp['portal'][0] + 5, mp['portal'][1] + 5])], fill='#357b76')
q.text((35, 15), '校园建筑修复版 · 实际楼体占地与道路核对', font=titlefont, fill='#2b4b3d')
q.text((35, 60), '白色：道路\u3000米色：人行铺装\u3000棕色：重点建筑\u3000灰绿：简化背景\u3000青色：111号传送门', font=font, fill='#3b5a48')
image.save(O / '10-俯视布局核对.png')
report = json.loads((O / '道路与落位检查.json').read_text(encoding='utf-8'))
assert not report['roadBuildingOverlaps'] and (not report['buildingOverlaps']) and (not any((a['foreignOverlap'] > 0.01 for a in report['entrances'])))
summary = {'revision': D['revision'], 'sceneSHA256': hash(O / '场景数据.json'), 'runtimeSHA256': hash(O / '运行脚本.js'), 'prototypeProfiles': report['prototypeProfiles'], 'modelCount': len(D['models']), 'registeredEntrances': len(report['entrances']), 'roadBuildingOverlaps': 0, 'buildingOverlaps': 0, 'foreignApronOverlaps': 0, 'researchHeading': 25, 'researchFrontRoad': 'G8 → RESEARCH_FRONT → G18R', 'preserved': ['两张独立围墙地图', '111号双向传送', '两条上层连廊及廊下通行', '体育场矩形围墙', '红线补路与蓝线删路', '原人物/自行车动作、速度和体力']}
(O / '本轮修复记录.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
print('documented', len(manifest), 'profiles', len(report['entrances']), 'entrances')
