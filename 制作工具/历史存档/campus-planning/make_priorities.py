from pathlib import Path
import json,html
out=Path('/workspace/cc-practice/地图规划/制作方案R2');base=json.loads(Path('/workspace/cc-practice/地图规划/全校布局规划.json').read_text());old=json.loads(Path('/workspace/cc-practice/sufe-campus-adventure/locations/campus_map/painted/data/campus.json').read_text())
scene={'teaching3':'a50（三教外部与楼层）','greenleaf_canteen':'b1021（餐厅）','student_dormitory':'dormitory（寝室）','cainiao_station':'a40（菜鸟驿站）','track':'d1（田径场）'}
items=[]
for b in old['buildings']:
 id=b['id'];level='A' if id in scene else 'B';detail='入口、门牌、到达前场、镜头可见立面精做；屋顶与背面简化' if level=='A' else '轮廓、主材质、特色立面与介绍入口单独制作；重复窗格与背面复用'
 if id=='finance':detail='B级重点主景：保留五道拱门、浅灰石墙、石阶；背面简化'
 if id=='wudonglecture':detail='B级重点主景：保留横向窗带、凹入楼梯间与红砖基座；连廊按结构节点制作'
 items.append({'id':id,'name':b['name'],'artTier':level,'existingRole':'场景入口绑定＋介绍' if id in scene else '建筑介绍','sceneBinding':scene.get(id),'treatment':detail})

placement={
'finance':('D02 · 运动场西侧金融学院','独立识别楼体'),
 'teaching3':('D09 · 武东南端三教','与信管保持连体组关系，独立入口'),
 'scai':('武东院楼组 · 学院节点','保留独立介绍和双柱雨棚；楼体归属按学院地址核对，不沿用旧图南北拼接'),
 'sime':('D10 · 三教西端信管','共享连续楼体，独立介绍锚点'),
 'activity':('G48 · 学生中心所在活动组团（规划迁移）','由该组团承接原活动中心介绍；这是内容落位决定，不将两者认定为同一历史建筑'),
 'research':('G43＋G44 · 西南科研组团','一个科研节点，塔楼与裙房共同制作'),
 'bookstore':('绿叶—湖畔景观支线','独立店面识别；沿用原节点内容，实体门址核对后放置'),
 'greenleaf_canteen':('G26 · 第一食堂','沿用绿叶餐厅入口绑定'),
 'sufe_cafe':('国定餐饮服务组','保留六食堂与咖啡内容；以实体餐饮门址归位'),
 'teaching2':('G21 · 国定教学组北侧','与一教各自保留介绍，统一投影'),
 'teaching1':('G22 · 国定教学组南侧','与梯教保持图示相邻关系'),
 'guodinglecture':('G23 · 一教西侧梯教','低层体块单独识别'),
 'guoding_gym':('G17 · 国定北部体育馆','保留大跨度屋顶与入口'),
 'student_dormitory':('国定南部宿舍组 · 代表入口','只设一个原图寝室入口，不为整组楼逐栋新增室内'),
 'halal_canteen':('国定生活服务支线','保留介绍与区域传送目的地；实体门址核对后放置'),
 'cainiao_station':('国定生活服务支线','保留快递场景入口、门头与取件前场；实体门址核对后放置'),
 'third_canteen':('G10 · 国定片区西侧第三食堂','纠正旧图武东标签，保留原介绍内容'),
 'statistics':('D07＋D12 · 运动场东侧统计院楼组','一组统计内容，两块校园占地；一个介绍锚点，不复制两份功能'),
 'wudonglecture':('D08 · 三教北侧梯教','保持与三教的通行联系')}
for item in items:
 item['newMapTarget'],item['placementRule']=placement[item['id']]

D={'revision':'R2','purpose':'按原地图内容决定美术投入；以用户俯视图约束三片布局','mainBuildings':items,'sceneBindings':scene,'retainedFunctions':['19处主要建筑内容及原有介绍节点','5类场景入口绑定；开放条件沿用现有状态','水塔攀爬与观景','老校门庭院往返','春晖湖桥面通行与水体碰撞','两处教学连廊下方地面通路、柱脚及遮挡','8个区域传送点，更新名称与落点对应新布局','宿主其他地点菜单与现有返回路径'],'backgroundPolicy':{'W':'武川片区整体按C级背景制作；图书馆、会计学院、四教保留独特轮廓，大草坪和道路保留；不新增室内与交互。','G':'保留原图教学、住宿、餐饮、快递与景观节点。宿舍只精做主角所住的一栋及其前场，其余同组楼共享模块；行政/教技/办公等作为C级背景。','D':'三教与田径场为A级功能节点；梯教、金融、计算机、信管、统计等原图主楼为B级，门前与特色立面优先；沿街办公及次要院楼C级。'},'tiers':{'A':'可进入/可操作节点与结构性通路：入口、操作区、标识、碰撞、遮挡和返回落点完整制作；无需精做每一面。','B':'原图主要介绍建筑与标志景观：独立识别轮廓和主立面，保留介绍；不扩展新室内或新交易功能。','C':'无原图独立内容的背景建筑：基础体块＋统一窗带/屋顶模块；按组团共享素材，保留实际道路、间距和天际线。'},'workAllocation':{'A_and_structural_nodes':'55%','B_and_signature_landscape':'30%','C_background':'15%','meaning':'制作资源分配目标，不是建筑数量或实测工时'},'navigation':{'guoding_daily_loop':'主角宿舍—餐饮节点—一教/二教/国定梯教—宿舍；清真与菜鸟作为生活支线接入','wudong_academic_loop':'校园入口—金融与运动场—院楼/三教/梯教—主路返回','landscape_branch':'绿叶步行街—书店—湖畔与水塔；保留原图标志景观与介绍','wuchuan_branch':'跨路连接后沿图书馆、四教及大草坪形成观光支线；不把整片宿舍/办公庭院变成逐栋任务点','constraints':'以上是功能连接方案，线路的实际落点服从校园路网；不沿旧工程坐标重新拼接三个片区。'},'simplification':['重复宿舍组共享2—3套立面模块，用层数、窗带、屋顶和色调变化区分','次要行政与办公楼只保留轮廓及临路面，背面降低细节','原图未承载内容的附属房、车库、机房采用简化体块','大面积草坪保持留白；仅保留有地点特征的树阵、标志树、水岸与必要设施','不为每个占位新增招牌、精细门廊、室内或交互','组团合批不等于合并碰撞，楼间原有穿行通道保持开放'],'qualityRules':['细节量可减，素材清晰度、画风与投影保持统一；不靠低像素缩图做背景','植物保持独立体积与接地，不剪切成长条平片','楼前设施不能被楼墙误遮挡；背向入口用正确拆层和局部淡出保证可用','A/B级地点正常行走可读楼名；C级减少悬浮标牌','主楼保留旧ID；同步entry、places、交互区、返回落点及小地图/区域传送数据'],'deliveryOrder':['先在总图标清A/B/C和旧内容ID，锁定保留与简化清单','先做国定日常功能圈与武东三教—梯教—运动场核心的可走白模','优先完成A级入口与结构性通路，再完成B级识别立面','最后用统一模块补齐C级背景和武川观光支线，整图检查布局与风格'],'sourceFiles':['locations/campus_map/painted/building_links.json','modules/a3/locations/a50/location_definition.tres:63','locations/campus_map/walking_campus_host.gd:configure/request_interact','locations/campus_map/painted/scripts/main.gd:_process/show_building','locations/campus_map/painted/data/campus.json'],'placementRules':{'semanticIDs':'19个内容ID不等于19座独立新楼；连体楼共享体块，入口与介绍分别保留','detailGate':'名单中按组团登记的点先完成门址对照，再进入白模入口定位；不以旧图自由拼接坐标代替校园位置'},'plotPolicy':'底图沿用P01的几何关系，仅用于表示片区与投入层次；有明确对应名称的主楼着色，未逐栋对应的原图节点列入区域任务框，不伪造具体门位或新建筑。'}
(out/'制作分级与保留清单.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
# A/B colouring applies only to identifiable plan plots. Regional cards retain all unmatched original content.
A={'G26','D09'};B={'G21','G22','G23','G17','G10','G43','G44','D02','D08','D10','D07','D12','G48'}
svg=['<svg viewBox="140 180 1760 900" xmlns="http://www.w3.org/2000/svg" aria-label="全校制作精度分级图"><defs><pattern id="h" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="9" height="9" fill="#e2e4e0"/><path d="M0 0V9" stroke="#b3bcb6" stroke-width="2"/></pattern></defs>']
pts=lambda v:' '.join(','.join(str(round(n,2)) for n in p) for p in v)
for c in base['campuses']:svg.append(f'<polygon points="{pts(c["polygon"])}" fill="#eef1e9" stroke="#a8b4a8" stroke-width="2"/>')
for x in base['exclusions']:svg.append(f'<polygon points="{pts(x["polygon"])}" fill="url(#h)" stroke="#b3bcb6"/>')
for s in base['spaces']:
 color='#e9a690' if s['id']=='D-TRACK' else '#cadbcc' if s['kind']=='green' else '#c9dfe1' if s['kind']=='water' else '#d8e0d6'
 svg.append(f'<polygon points="{pts(s["polygon"])}" fill="{color}" stroke="#b1c2b3"/>')
for r in base['roads']:
 svg.append(f'<polyline points="{pts(r["points"])}" fill="none" stroke="#fffdf5" stroke-width="{r["width"]}" stroke-linecap="round" stroke-linejoin="round"/>')
for b in base['buildings']:
 color='#c9d0c9';stroke='#98a79c'
 if b['id'] in A:color='#df896d';stroke='#b9614a'
 elif b['id'] in B:color='#c6b075';stroke='#948252'
 svg.append(f'<polygon points="{pts(b["polygon"])}" fill="{color}" stroke="{stroke}" stroke-width="1.2"><title>{html.escape(b["name"])}</title></polygon>')
# Follow existing road geometry for production corridors; no new cross-building shortcuts.
priority_roads={'G1','G3','G5','G7','D1','D2','D3','D4','D5','D6'}
for r in base['roads']:
 if r['id'] in priority_roads:
  svg.append(f'<polyline points="{pts(r["points"])}" fill="none" stroke="#6b948b" stroke-width="3" stroke-dasharray="9 6" opacity=".85"/>')
# Main-player dormitory is an area allocation, not an invented choice of a numbered dorm.
svg.append('<rect x="1234" y="492" width="287" height="69" rx="9" fill="none" stroke="#c86f54" stroke-width="3" stroke-dasharray="7 5"/>')
labels=[('C 武川背景片区',495,380),('图书馆 · 保留轮廓',652,729),('会计学院 · 保留轮廓',436,463),('四教 · 简化立面',619,562),('国定教学与生活核心',1450,252),('B 新体育馆',1293,287),('B 二教',1663,407),('B 一教',1705,448),('B 国定梯教',1634,483),('A 绿叶餐厅 / 第一食堂',1406,460),('主角宿舍精做1栋，其余宿舍组团',1373,582),('B 第三食堂',1047,432),('B 科研楼群',1259,651),('B 活动组团',1178,712),('A 田径场',1038,752),('B 金融学院',861,782),('B 统计院楼组',1219,818),('B 梯教',1188,878),('A 三教',1156,940)]
for t,x,y in labels:svg.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="16" fill="#304440" stroke="#f9faf5" stroke-width="4" paint-order="stroke" font-weight="600">{html.escape(t)}</text>')
svg.append('<path d="M260 270 L270 232 L280 270 L270 261Z" fill="#38594b"/><text x="270" y="218" text-anchor="middle" font-size="19" fill="#38594b">N</text></svg>')
(out/'分级底图.svg').write_text(''.join(svg))
cards=''
for title,text in [('A｜把功夫放在玩家真正使用的位置','三教、主角宿舍、绿叶餐厅、菜鸟驿站、田径场。精做入口、门牌、到达前场与可操作区；背面和重复窗格简化。'),('B｜原图主要建筑，一栋一套识别特征','其余15处主要建筑保留介绍。金融、梯教作为重点主景；其他楼突出轮廓、材质、特色窗带和入口，背面复用。'),('C｜其余背景按组团制作','普通宿舍、行政办公、附属房及武川新增背景采用统一模块。图书馆、会计学院、四教保留识别轮廓，保持草坪、道路与间距。'),('必须保留｜功能与导航骨架','水塔攀爬、老校门往返、湖桥、两处连廊下通路、8个区域传送点及其他地点菜单。功能保留与美术等级分别检查。')]:cards+=f'<section><h3>{title}</h3><p>{text}</p></section>'
rows=''.join(f'<tr><td>{x["artTier"]}</td><td>{html.escape(x["name"])}</td><td>{x["newMapTarget"]}<br><small>{x["placementRule"]}</small></td><td>{x["existingRole"]}</td><td>{x["treatment"]}</td></tr>' for x in items)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>财大地图制作方案 R2</title><style>*{box-sizing:border-box}body{margin:0;background:#f3f5ef;color:#263e37;font:15px 'Noto Sans CJK SC','Microsoft YaHei',sans-serif}header{padding:25px 34px;background:#fff;border-bottom:1px solid #dce4db;display:flex;justify-content:space-between;align-items:center}h1{margin:0;font-size:27px}header p{margin:7px 0 0;color:#687b70}.pill{border:1px solid #c9d7cc;padding:10px;border-radius:8px;font-size:13px}.body{display:grid;grid-template-columns:minmax(0,1fr) 345px;padding:20px;gap:20px}.map{background:#f9faf5;border:1px solid #dce3da;border-radius:10px;overflow:hidden}.map svg{width:100%;display:block}.legend{display:flex;gap:24px;padding:14px 22px;border-top:1px solid #dce3da;background:#fff}.legend i{display:inline-block;width:12px;height:12px;margin-right:7px}.caption{font-size:12px;padding:0 22px 15px;background:#fff;color:#66786d;line-height:1.8}.aside section{background:#fff;border:1px solid #dce3da;border-radius:9px;margin-bottom:13px;padding:16px}h3{font-size:16px;margin:0 0 8px}.aside p{font-size:14px;line-height:1.85;margin:0}.budget{padding:15px;background:#e5ece1;border-radius:8px;line-height:1.8}.below{margin:0 20px 25px;background:#fff;border:1px solid #dce3da;border-radius:10px;padding:24px}h2{font-size:20px;margin:0 0 15px}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:12px 10px;text-align:left;border-bottom:1px solid #e2e7df;vertical-align:top}th{background:#f0f3ec}.routes{display:grid;grid-template-columns:1fr 1fr;gap:15px}.routes p{line-height:1.8}.foot{padding:0 24px 25px;font-size:12px;color:#66786d}@media(max-width:900px){.body{grid-template-columns:1fr}.aside{display:grid;grid-template-columns:1fr 1fr;gap:12px}.routes{grid-template-columns:1fr}h1{font-size:21px}header .pill{display:none}}</style><header><div><h1>全校地图制作方案 · R2</h1><p>校园布局决定位置，原地图内容决定制作重点。</p></div><div class="pill">保留19处主要建筑内容 · 保留5类场景入口绑定</div></header><div class="body"><div class="map">'''+''.join(svg)+'''<div class="legend"><span><i style="background:#df896d"></i>A 核心功能节点</span><span><i style="background:#c6b075"></i>B 原图主要建筑</span><span><i style="background:#c9d0c9"></i>C 简化背景</span><span style="color:#537d73">┄ 优先制作的通行街面</span></div><div class="caption">分级图表达片区、楼群和优先制作街面。主角宿舍按区域框登记，只精做原图绑定的一栋。菜鸟、六食堂、清真、书店、计算机学院等原图内容全部保留在下方清单；按原有身份逐项落位，不用未标名的图块冒充。</div></div><div class="aside">'''+cards+'''<div class="budget"><b>制作投入目标</b><br>A及结构节点 55% · B及特色景观 30% · C背景 15%<br><small>精度减少的是细节数量，画风、清晰度和透视保持统一。</small></div></div></div><div class="below"><h2>地图怎样组织</h2><p><b>三个制作单元：</b>国定片区负责日常教学与生活；武东片区负责三教、院楼和运动场；武川片区保留空间轮廓与地标参照。19个旧内容ID分别迁移，连体楼共用体块，不拆成19座新楼。</p><div class="routes"><p><b>国定日常圈</b><br>主角宿舍 → 餐饮 → 一教 / 二教 / 国定梯教 → 宿舍。清真、菜鸟作为生活支线接入；绿叶步行街、书店、湖畔水塔保留为特色景观支线。</p><p><b>武东学习圈</b><br>校园入口 → 金融与田径场 → 院楼 / 三教 / 梯教 → 主路。武川片区保留图书馆、四教、大草坪等方位参照，以观光支线连接，背景组团降低投入。</p></div><p>连接关系服从校园真实路网；角色到达的入口前场精做，经过的街面次之，远处背面简化。合并素材不合并楼间通路，原有道路和空隙继续保留。</p></div><div class="below"><h2>19处主要建筑：保留什么，制作到什么程度</h2><table><thead><tr><th>等级</th><th>原图对象</th><th>新图落位与处理规则</th><th>现有作用</th><th>处理决定</th></tr></thead><tbody>'''+rows+'''</tbody></table></div><div class="below"><h2>具体删减与验收</h2><p>普通宿舍采用2—3套共享立面模块；次要办公楼保留体块和临路面；附属房、车库与机房用简单体块。取消逐栋独立门廊、满图招牌、随机雕塑和重复花坛。草坪保留留白，步行街树阵、湖岸和标志树保留特色。</p><p>A级入口正常视距能读楼名、能走到、能触发并正确返回；B级主楼能从轮廓和特色立面辨认；C级风格统一、背景安静。灌木不得剪切成平片，楼前设施不得被楼体误挡。三教等文字独立绘制，正常行走视距目标16—20屏幕像素。</p><p>制作顺序：分级与旧ID清单 → 两个主要功能圈白模 → A级入口和结构 → B级特色立面 → C级组团补齐。旧工程场景、故事、介绍和开放条件沿用；本方案不新增交易或室内玩法。</p></div><div class="foot">本轮只修订制作规划，原始游戏和建筑素材未改动。依据：campus.json、building_links.json、a50场景元数据与现有地图交互脚本。</div></html>'''
(out/'打开制作方案.html').write_text(page)
print('retained buildings',len(items),'scene bindings',len(scene),'A building count',sum(x['artTier']=='A' for x in items))
