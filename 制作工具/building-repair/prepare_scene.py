from pathlib import Path
import os
ROOT = Path(os.environ.get('CAMPUS_WORK_ROOT', str(Path(__file__).resolve().parents[2]))).resolve()
OUTPUT = Path(os.environ.get('CAMPUS_OUTPUT_DIR', str(ROOT / '工作输出' / '校园建筑修复版'))).resolve()
OUTPUT.mkdir(parents=True, exist_ok=True)
from pathlib import Path
import json, math, sys, base64, copy
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union, nearest_points
from shapely.prepared import prep
O = OUTPUT
D = json.loads((ROOT / '校园动作继承版' / '场景数据.json').read_text(encoding='utf-8'))
D['maps']['guoding']['spawn'] = [1140, 984]
F = json.loads((ROOT / '占地复核图' / '轮廓与道路.json').read_text(encoding='utf-8'))
M = {m['id']: m for m in D['models']}

def part(x, z, w, d, f=3, style='cream', roof='flat', y=0, h=None, role=None):
    p = dict(x=x, z=z, w=w, d=d, floors=f, h=h or f * 3.7, style=style, roof=roof, y=y)
    if role:
        p['role'] = role
    return p

def world(m, x, z):
    a = math.radians(m['rotation'])
    return [m['center'][0] + math.cos(a) * x + math.sin(a) * z, m['center'][1] - math.sin(a) * x + math.cos(a) * z]

def rect(m, x, z, w, d):
    return Polygon([world(m, x - w / 2, z - d / 2), world(m, x + w / 2, z - d / 2), world(m, x + w / 2, z + d / 2), world(m, x - w / 2, z + d / 2)])

def rings(q):
    if q.is_empty:
        return []
    if q.geom_type == 'Polygon':
        return [dict(outer=list(q.exterior.coords)[:-1], holes=[list(h.coords)[:-1] for h in q.interiors])]
    return [r for a in q.geoms for r in rings(a)]

def shape(m):
    return unary_union([Point(world(m, p['x'], p['z'])).buffer(p['w'] / 2, quad_segs=20) if p.get('shape') == 'round' else rect(m, p['x'], p['z'], p['w'], p['d']) for p in m['parts'] if p['y'] < 0.1])

def entrance(m, x, z, road, angle=0, width=7, canopy='slab', columns=None, steps=3, rise=0.12, run=0.65, canopyDepth=3.5, canopyHeight=3.6, route=None):
    e = dict(x=x, z=z, angle=angle, road=road, width=width, canopy=canopy, columns=columns or [], steps=steps, rise=rise, run=run, landing=1.0, canopyDepth=canopyDepth, canopyHeight=canopyHeight)
    a = math.radians(angle)
    n = [math.sin(a), math.cos(a)]
    e['normal'] = n
    e['outerLocal'] = [x + n[0] * (steps * run + e['landing'] + 1.2), z + n[1] * (steps * run + e['landing'] + 1.2)]
    e['world'] = world(m, *e['outerLocal'])
    if route:
        e['via'] = route
    m.setdefault('entrances', []).append(e)
    return e
from layout_v4 import apply_layout
apply_layout(D, F, part, world, rings)
M = {m['id']: m for m in D['models']}
r = M['research']
r.update(rotation=25, width=128, depth=64, height=51.8, parts=[part(-7, 1, 42, 27, 14, 'redtower', role='research-tower'), part(-59, 0, 70, 64, 2, 'redtower', h=7.8, role='research-podium'), part(16, -3, 28, 58, 2, 'redtower', h=7.8, role='research-podium'), part(-11, 20, 26, 12, 2, 'redtower', h=7.8, role='research-podium')])
entrance(r, -10, -25, 'RESEARCH_FRONT', 180, 22, 'research-portico', [-10.2, 10.2], 3, 0.12, 0.7, 7, 7.8)
roadmap = {a['id']: a for a in D['maps']['guoding']['roads']}
g8 = LineString(roadmap['G8']['points'])
front = LineString([world(r, -150, -43), world(r, 30, -43)])
cross = g8.intersection(front)
assert cross.geom_type == 'Point'
D['maps']['guoding']['roads'].append(dict(id='RESEARCH_FRONT', name='科研楼前连续道路', map='guoding', width=7, points=[[cross.x, cross.y], world(r, 30, -43), roadmap['G18R']['points'][0]], connects=['G8', 'G18R'], basis='沿科研楼北侧前沿连接外围道路，不穿三角草坪'))
r['frontRoad'] = 'RESEARCH_FRONT'
r['prototype'] = '红砖外框、连续窄竖窗槽、低裙房与深凹玻璃门厅；整体与武东片区同轴。'
w = M['wudonglecture']
w['parts'] = [part(0, -3, 48, 10, 6, 'academic'), part(-19.5, 5, 9, 6, 6, 'academic'), part(11.75, 5, 24.5, 6, 6, 'academic')]
entrance(w, -6.5, 2, 'RED3', 0, 10.4, 'lecture', [-4.1, 4.1], 3, 0.12, 0.7, 6.5)
a = M['academic_link']
for x, kind in [(-44, 'single'), (0, 'single'), (44, 'academic-wide')]:
    entrance(a, x, 10, 'D5', 0, 9 if x < 40 else 13, kind, [-3.5] if x < 40 else [-4.8, 4.8])
entrance(M['statistics'], 0, 8, 'RED2', 0, 6, 'none', [], 3)
entrance(M['finance'], 0, 13, 'D3', 0, 17, 'none', [], 3, route=[[842.0521, 836.3618], [837.9479, 847.6382], [864, 923]])['approachWidth'] = 5.2
a = M['activity']
a['parts'] = [part(0, -16, 37, 11, 3, 'redwhite'), part(-13, 0, 11, 22, 3, 'redwhite'), part(0.5, -4, 16, 6, 3, 'redwhite'), part(13, -4, 11, 20, 3, 'redwhite'), part(0, 16, 37, 11, 3, 'redwhite')]
entrance(a, -18.5, 0, 'D2', -90, 12, 'activity', [-4.6, 4.6], 4, 0.12, 0.7, 4.5)
for id, road, width in [('teaching1', 'G14', 12), ('teaching2', 'TEACHING_LINK', 18)]:
    m = M[id]
    entrance(m, 0, m['depth'] / 2, road, 0, width, 'red-tile', [-7, -3.5, 3.5, 7] if id == 'teaching2' else [-4.5, 4.5])
entrance(M['guodinglecture'], 0, 12.5, 'G14', 0, 10, 'hall', [-4.2, 4.2])
entrance(M['guoding_gym'], -25, 35, 'G3', 0, 14, 'none', [], 3)
entrance(M['greenleaf_canteen'], 0, 13, 'G1', 0, 8, 'greenleaf', [], 3)
M['halal_canteen']['rotation'] = 180
M['halal_canteen']['parts'][0]['roof'] = 'flat'
entrance(M['halal_canteen'], 0, 12, 'G16', 0, 9, 'none', [], 3)
m = M['third_canteen']
m['parts'] = [part(0, -5, 57, 25, 3, 'brick', role='canteen-rear'), part(11.5, 12.5, 34, 10, 3, 'brick', role='canteen-solid-front'), part(-28.1, 12.5, 0.8, 10, 3, 'brick', role='canteen-pier'), part(-11.8, 12.5, 0.6, 10, 3, 'brick', role='canteen-pier')]
entrance(m, -8.5, 17.5, 'INNER_AXIS', 0, 7, 'newcanteen', [], 3)
M['cainiao_station']['rotation'] = -65
entrance(M['cainiao_station'], 0, 6, 'G21R', 0, 18, 'blue', [], 3, 0.12, 0.65, 2.5)
entrance(M['bookstore'], 14, 0, 'G8', 90, 3, 'none', [], 2, 0.12, 0.6)
m = M['sufe_cafe']
m['parts'] = [part(-3, 0, 32, 17, 2, 'cafe', h=7.6), part(15.3, 0, 5.4, 17, 2, 'cafe', h=8.5, role='cafe-glass')]
entrance(m, 15.3, 8.5, 'G1', 0, 5.4, 'cafe', [], 2)
m = M['accounting']
m['parts'] = [part(0, -8, 82, 28, 2, 'pink'), part(-14, 12, 42, 15, 2, 'pink'), part(30, 12, 10, 15, 2, 'pink'), part(0, -2, 82, 40, 2, 'pink', y=7.4, role='accounting-upper')]
entrance(m, 16, 6, 'W1', 0, 18, 'accounting', [], 4, 0.12, 0.75, 14)
m = M['phoenix']
m['parts'] = [part(0, -5, 72, 20, 5, 'cream'), part(-24, 10, 24, 10, 5, 'cream'), part(24, 10, 24, 10, 5, 'cream'), part(0, 10, 24, 10, 2, 'cream', y=11.1, role='phoenix-upper')]
entrance(m, 0, 15, 'W1', 0, 9, 'phoenix', [], 3)
m = M['teaching4']
m.update(height=14.8, parts=[part(0, 0, 92, 30, 4, 'cream', 'terrace')])
entrance(m, 0, 15, 'W7', 0, 16, 'red-tile', [-6, -2.8, 2.8, 6])
entrance(M['economics'], 0, 15.5, 'W-ECON-FRONT', 0, 11, 'economics', [], 3, route=[[723, 474]])
joined = M['w13']
entrance(joined, -19, 8, 'W-DORM-LINK', 0, 6, 'none', [], 0,
         route=[world(joined, -42, 11), world(joined, -43, -6)])['identity'] = 'w14'
entrance(joined, 18, 14, 'W-DORM-LINK', 0, 6, 'none', [], 0,
         route=[world(joined, -3, 17), world(joined, -42, 11), world(joined, -43, -6)])['identity'] = 'w13'
entrance(M['library'], 39, 32.5, 'W5', 0, 8, 'library', [], 3)
M['library']['parts'][3].update(z=17.75, d=29.5)
entrance(M['enterprise'], 0, 12.5, 'W1', 0, 13, 'steel-frame', [], 3)
for id in ['exchange', 'wuchuan_pool', 'wuchuan_hall', 'badminton', 'wuchuan_canteen']:
    m = M[id]
    road = {'exchange': 'W2', 'wuchuan_pool': 'W1', 'wuchuan_hall': 'W6', 'badminton': 'W1', 'wuchuan_canteen': 'W-CANTEEN-BRANCH'}[id]
    entrance(m, 0, m.get('entryFace', m['depth'] / 2), road, 0, 12, 'sports' if 'hall' in m['kind'] else 'canteen', [], 3, route=[[413, 720]] if id == 'exchange' else None)
primary = set(['research', 'academic_link', 'wudonglecture', 'statistics', 'finance', 'activity', 'bookstore', 'guoding_gym', 'teaching1', 'teaching2', 'guodinglecture', 'greenleaf_canteen', 'sufe_cafe', 'halal_canteen', 'third_canteen', 'cainiao_station', 'library', 'accounting', 'economics', 'phoenix', 'enterprise', 'teaching4', 'exchange', 'wuchuan_pool', 'wuchuan_hall', 'badminton', 'wuchuan_canteen'])
report = dict(revision='road-layout-repair-v4', roadBuildingOverlaps=[], buildingOverlaps=[], entrances=[], prototypeProfiles=[], roadConnectivity={}, placementPolicy='主楼保留，21/22按参考图重连；转折、接站及边界显式修复，无自动腾挪。')
for m in D['models']:
    m['posts'] = []
    m['groundFixtures'] = []
    m['steps'] = []
    m['actualBuildingFootprint'] = rings(shape(m))
    if m['kind'] == 'metro':
        m['groundFixtures'] = [rings(rect(m, x, 0, .45, 7.6))[0] for x in [-4.6, 4.6]]
        m['groundFixtures'].append(rings(rect(m, 6, 1.2, 1.6, .4))[0])
    if m['id'] in primary:
        m['facadeProfile'] = m['id']
        report['prototypeProfiles'].append(m['id'])
    if m.get('entrances'):
        m['entryLocal'] = m['entrances'][0]['outerLocal']
        m['entry'] = m['entrances'][0]['world']
        for e in m['entrances']:
            a = math.radians(e['angle'])
            cx, cz = (e['x'], e['z'])
            for x in e['columns']:
                z = e['canopyDepth'] * 0.65
                p = world(m, cx + math.cos(a) * x + math.sin(a) * z, cz - math.sin(a) * x + math.cos(a) * z)
                m['posts'].append(dict(center=p, size=0.55))
            for i in range(e['steps']):
                m['steps'].append(dict(entry=e, along0=i * e['run'] + (e['landing'] if i else 0), along1=(i + 1) * e['run'] + e['landing'], height=(e['steps'] - i) * e['rise'], width=min(e['width'], 12)))
    else:
        if m['kind'] == 'cainiao':
            m['groundFixtures'] = [rings(rect(m, x, 4.5, 2.6, 1.1))[0] for x in [-10.5, 10.5]]
        entries = m.get('entries') or [dict(x=m['entryLocal'][0], z=m.get('entryFace', m['depth'] / 2), porch=m.get('porch', 'double'))]
        if m['kind'] in ['finance', 'bookstore', 'dormcourt', 'gym', 'cainiao', 'oldgate', 'watertower', 'statistics', 'metro']:
            entries = []
        for e in entries:
            if e.get('porch') in ['single', 'double', 'wide', 'redhip', 'frame']:
                for x in [e['x'] - 3.5] if e['porch'] == 'single' else [e['x'] - 4, e['x'] + 4]:
                    m['posts'].append(dict(center=world(m, x, e['z'] + 2.1), size=0.5))
    if m['kind'] == 'cainiao':
        m['groundFixtures'] = [rings(rect(m, x, 4.5, 2.6, 1.1))[0] for x in [-10.5, 10.5]]
    if m['kind'] == 'halal':
        m['groundFixtures'] = [rings(rect(m, 38, -4, 3.0, 13.4))[0]]
    if m['id'] == 'research':
        m['groundFixtures'].append(rings(rect(m, -10, -25, 18, 0.2))[0])
        p = m['parts'][0]
        bw = (p['w'] - 3.2) / 12
        sd = (p['d'] - 3.2) / 7
        for face in [-1, 1]:
            for i in range(1, 12):
                m['groundFixtures'].append(rings(rect(m, p['x'] - p['w'] / 2 + 1.6 + i * bw, p['z'] + face * (p['d'] / 2 + 0.14), bw * 0.45, 0.7))[0])
            for x in [-1, 1]:
                m['groundFixtures'].append(rings(rect(m, p['x'] + x * (p['w'] / 2 - 0.8), p['z'] + face * (p['d'] / 2 + 0.14), 1.6, 0.7))[0])
            for i in range(1, 7):
                m['groundFixtures'].append(rings(rect(m, p['x'] + face * (p['w'] / 2 + 0.14), p['z'] - p['d'] / 2 + 1.6 + i * sd, 0.7, sd * 0.45))[0])
    if m['id'] == 'phoenix':
        m['groundFixtures'].append(rings(rect(m, 0, 15, 23, 0.2))[0])
    if m['id'] == 'third_canteen':
        m['groundFixtures'].append(rings(rect(m, -8.5, 17.5, 6, 0.2))[0])
for mid, mp in D['maps'].items():
    ms = [m for m in D['models'] if m['map'] == mid]
    site = unary_union([Polygon(r['outer'], r.get('holes', [])) for r in mp['site']])
    lines = {r['id']: LineString(r['points']) for r in mp['roads']}
    asphalt = unary_union([lines[r['id']].buffer(r['width'] / 2, cap_style=2, join_style=2) for r in mp['roads']])
    if mid == 'wuchuan':
        # Seven-wide edge road narrows to the five-wide station forecourt over this segment.
        a, b = lines['W-METRO-ACCESS'].coords
        dx, dz = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dz)
        nx, nz = -dz / length, dx / length
        taper = Polygon([[a[0] + nx * 3.5, a[1] + nz * 3.5], [b[0] + nx * 2.5, b[1] + nz * 2.5],
                         [b[0] - nx * 2.5, b[1] - nz * 2.5], [a[0] - nx * 3.5, a[1] - nz * 3.5]])
        asphalt = asphalt.union(taper)
    junctions = []
    for i, line in enumerate(lines.values()):
        for other in list(lines.values())[i + 1:]:
            hit = line.intersection(other)
            pts = [hit] if hit.geom_type == 'Point' else list(hit.geoms) if hit.geom_type == 'MultiPoint' else []
            for p in pts:
                if not any((p.distance(q) < 2 for q in junctions)):
                    junctions.append(p)
    repaired_ids = ({'W1', 'W4', 'W-ECON-FRONT', 'W-RESEARCH-EAST', 'W-METRO-EDGE',
                     'W-METRO-ACCESS', 'W-CANTEEN-BRANCH', 'W-DORM-LINK'} if mid == 'wuchuan'
                    else {'G3', 'G16', 'G17R', 'G18R', 'RESEARCH_FRONT'})
    repaired_junctions = []
    for p in junctions:
        touching = [r for r in mp['roads'] if lines[r['id']].distance(p) < 1e-7]
        if any(r['id'] in repaired_ids for r in touching):
            repaired_junctions.append((p, min(r['width'] for r in touching)))
        else:
            asphalt = asphalt.union(p.buffer(4.4, quad_segs=10))
    # Close only the inside corners. Straight stems retain their specified width.
    for p, width in repaired_junctions:
        radius = min(1.25, width * .18)
        rounded = asphalt.buffer(radius, quad_segs=8).buffer(-radius, quad_segs=8)
        asphalt = asphalt.union(rounded.intersection(p.buffer(width * 2, quad_segs=8)))
    asphalt = asphalt.intersection(site)
    for i, m in enumerate(ms):
        sh = shape(m)
        area = sh.intersection(asphalt).area
        if area > 0.015:
            report['roadBuildingOverlaps'].append([m['id'], round(area, 3)])
        for n in ms[:i]:
            area = sh.intersection(shape(n)).area
            if area > 0.015:
                report['buildingOverlaps'].append([m['id'], n['id'], round(area, 3)])
    solids = [shape(m) for m in ms]
    for m in ms:
        solids.extend([Point(p['center']).buffer(p['size'] / 2, quad_segs=6) for p in m['posts']])
        solids.extend((Polygon(q['outer']) for q in m['groundFixtures']))
    if mid == 'guoding':
        solids.extend((Point(p).buffer(0.3) for b in D['bridges'] for p in b['posts']))
    water = unary_union([Polygon(s['polygon']) for s in D['spaces'] if s['kind'] == 'water' and Polygon(s['polygon']).intersects(site)])
    excluded = unary_union([Polygon(s['polygon']) for s in F['exclusions']])
    # The old approximate hatch boundary must not shave the verified edge road.
    if mp.get('protectedRoadCorridors'):
        excluded = excluded.difference(unary_union([Polygon(s['outer'], s.get('holes', [])) for s in mp['protectedRoadCorridors']]))
    wall = unary_union([LineString(l).buffer(0.3) for l in D['sportsEnclosure']['wallSegments']]) if mid == 'guoding' else Polygon()
    obstacles = unary_union(solids + [water, excluded, wall])
    walk = site.buffer(-0.85).difference(obstacles.buffer(0.65))
    paving = asphalt.buffer(1.4, join_style=2)
    approaches = []
    for m in ms:
        endpoints = []
        for e in m.get('entrances', []):
            origin = e['world']
            line = lines[e['road']]
            last = e.get('via', [])[-1] if e.get('via') else origin
            dest = nearest_points(line, Point(last))[0]
            points = [origin] + e.get('via', []) + [[dest.x, dest.y]]
            path = LineString(points)
            approachWidth = e.get('approachWidth', max(5.2, min(10, e['width'] * 0.6)))
            apron = path.buffer(approachWidth / 2, cap_style=2, join_style=2).union(Point(origin).buffer(approachWidth / 2, quad_segs=12))
            door = world(m, e['x'], e['z'])
            apron = apron.union(LineString([door, origin]).buffer(min(6, e['width'] / 2), cap_style=2))
            approaches.append(dict(building=m['id'], road=e['road'], points=points, width=approachWidth))
            collision = apron.intersection(unary_union([shape(n) for n in ms if n is not m]))
            report['entrances'].append(dict(id=m['id'], road=e['road'], door=door, arrival=origin, foreignOverlap=round(collision.area, 3), length=round(path.length, 2)))
            paving = paving.union(apron)
            endpoints.append(origin)
        if not endpoints:
            e = m['entry']
            dest = nearest_points(asphalt, Point(e))[0]
            seg = LineString([e, [dest.x, dest.y]])
            paving = paving.union(seg.buffer(2.4, cap_style=2, join_style=2))
            endpoints = [e]
        q = nearest_points(walk.buffer(-0.12), Point(endpoints[0]))[0]
        m['arrival'] = [q.x, q.y]
    paving = paving.intersection(site).difference(unary_union(solids).buffer(0.04))
    routeSurface = walk.intersection(asphalt.union(paving))
    mp['approaches'] = approaches
    mp['roadWalkSurface'] = rings(routeSurface)
    nav = prep(walk.buffer(-1.12))
    roadnav = prep(routeSurface.buffer(-0.65))
    prs = prep(asphalt.buffer(0.2))
    x0, y0, x1, y1 = site.bounds
    step = 1.5
    cols = math.ceil((x1 - x0) / step) + 1
    rows = math.ceil((y1 - y0) / step) + 1
    grid = bytearray(cols * rows)
    roadgrid = bytearray(cols * rows)
    for y in range(rows):
        for x in range(cols):
            p = Point(x0 + x * step, y0 + y * step)
            i = y * cols + x
            if nav.contains(p):
                grid[i] = 1 if prs.contains(p) else 2
            if roadnav.contains(p):
                roadgrid[i] = 1
    assert walk.contains(Point(mp['spawn'])), (mid, 'spawn blocked')
    assert walk.contains(Point(mp['portal'])), (mid, 'portal blocked')
    mp.update(walkSurface=rings(walk), asphalt=rings(asphalt), paving=rings(paving), junctions=[[p.x, p.y] for p in junctions], grid=dict(origin=[x0, y0], step=step, cols=cols, rows=rows, data=base64.b64encode(grid).decode()), roadGrid=base64.b64encode(roadgrid).decode())
    print(mid, 'asphalt components', len(rings(asphalt)), 'entrances', len(approaches), flush=True)
D['revision'] = 'campus-road-layout-repair-v4'
(O / '场景数据.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')), encoding='utf-8', newline='\n')
(O / '道路与落位检查.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
print('road overlaps', report['roadBuildingOverlaps'], 'building overlaps', report['buildingOverlaps'])
print('apron foreign collisions', [a for a in report['entrances'] if a['foreignOverlap'] > 0.1])
