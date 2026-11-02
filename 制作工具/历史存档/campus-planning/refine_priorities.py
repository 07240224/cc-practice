from pathlib import Path
p=Path('/workspace/scratch/campus-planning/make_priorities.py')
s=p.read_text()
s=s.replace("if id in ['finance','wudonglecture']:detail='B级重点主景：保留已确认外形，精做入口与特色立面；梯教连廊结构单独制作'", "if id=='finance':detail='B级重点主景：保留五道拱门、浅灰石墙、石阶；背面简化'\n if id=='wudonglecture':detail='B级重点主景：保留横向窗带、凹入楼梯间与红砖基座；连廊按结构节点制作'")
insert="""
placement={
'finance':('D02 · 运动场西侧金融学院','独立识别楼体'),
 'teaching3':('D09 · 武东南端三教','与信管保持连体组关系，独立入口'),
 'scai':('武东院楼组 · 学院节点','保留独立介绍和双柱雨棚；楼体归属按学院地址核对，不沿用旧图南北拼接'),
 'sime':('D10 · 三教西端信管','共享连续楼体，独立介绍锚点'),
 'activity':('国定—武东交界学生中心片区','保留活动中心内容；学生中心楼名对照后绑定，避免与学生艺术中心混用'),
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
"""
s=s.replace("D={'revision'",insert+"\nD={'revision'")
s=s.replace("'plotPolicy':'", "'placementRules':{'semanticIDs':'19个内容ID不等于19座独立新楼；连体楼共享体块，入口与介绍分别保留','detailGate':'名单中按组团登记的点先完成门址对照，再进入白模入口定位；不以旧图自由拼接坐标代替校园位置'},'plotPolicy':'")
s=s.replace("# Main-player dormitory", """# Follow existing road geometry for production corridors; no new cross-building shortcuts.
priority_roads={'G1','G3','G5','G7','D1','D2','D3','D4','D5','D6'}
for r in base['roads']:
 if r['id'] in priority_roads:
  svg.append(f'<polyline points="{pts(r["points"])}" fill="none" stroke="#6b948b" stroke-width="3" stroke-dasharray="9 6" opacity=".85"/>')
# Main-player dormitory""")
s=s.replace("('B 一教',1705,448),", "('B 一教',1705,448),('B 国定梯教',1634,483),")
s=s.replace("<td>{x[\"existingRole\"]}</td><td>{x[\"treatment\"]}</td>","<td>{x[\"newMapTarget\"]}<br><small>{x[\"placementRule\"]}</small></td><td>{x[\"existingRole\"]}</td><td>{x[\"treatment\"]}</td>")
s=s.replace('<th>现有作用</th>', '<th>新图落位与处理规则</th><th>现有作用</th>')
s=s.replace('C 简化背景</span></div>', 'C 简化背景</span><span style="color:#537d73">┄ 优先制作的通行街面</span></div>')
s=s.replace('分级图表达片区与投入，不新增门位。', '分级图表达片区、楼群和优先制作街面。')
s=s.replace('<h2>地图怎样组织</h2>', '<h2>地图怎样组织</h2><p><b>三个制作单元：</b>国定片区负责日常教学与生活；武东片区负责三教、院楼和运动场；武川片区保留空间轮廓与地标参照。19个旧内容ID分别迁移，连体楼共用体块，不拆成19座新楼。</p>')
p.write_text(s)
