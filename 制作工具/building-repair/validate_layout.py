"""Layout checks against the reference and independent user-marked locations."""
from pathlib import Path
import os, json
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('CAMPUS_OUTPUT_DIR', str(ROOT/'工作输出/校园道路修复V4')))
D = json.loads((OUT/'场景数据.json').read_text(encoding='utf-8'))
F = json.loads((ROOT/'占地复核图/轮廓与道路.json').read_text(encoding='utf-8'))
surface = lambda rs: unary_union([Polygon(r['outer'], r.get('holes', [])) for r in rs])
report = {'cuts': [], 'revision': D['revision']}
for mp in D['maps'].values():
    for cut in mp.get('mapCuts', []):
        cp = surface(cut['polygons'])
        areas = {key: cp.intersection(surface(mp[key])).area for key in
                 ['site', 'walkSurface', 'asphalt', 'paving', 'roadWalkSurface']}
        assert all(area < 1e-7 for area in areas.values()), (cut['id'], areas)
        report['cuts'].append(dict(id=cut['id'], removedArea=cp.area, remainingAreas=areas))
west, east = D['maps']['wuchuan'], D['maps']['guoding']
assert not surface(west['site']).covers(Point(790, 382)), '蓝圈绿地未剔除'
assert not surface(east['site']).covers(Point(1347, 667)), '科研南凸未剔除'
assert not any(r['id'] == 'G20R' for r in east['roads']), '草坪内部道路仍在'
lawn = Polygon(next(s['polygon'] for s in D['spaces'] if s['id'] == 'G-LAWN'))
report['centralLawnRoadArea'] = surface(east['asphalt']).intersection(lawn).area
assert report['centralLawnRoadArea'] < 1e-7
joined = next(b for b in D['models'] if b['id'] == 'w13')
body = surface(joined['actualBuildingFootprint'])
reference = Polygon(next(b['outer'] for b in F['buildings'] if b['id'] == 'C081'))
report['joinedReferenceIoU'] = body.intersection(reference).area/body.union(reference).area
assert body.geom_type == 'Polygon' and report['joinedReferenceIoU'] > .9
assert len(joined['entrances']) == 2
assert next(i['model'] for i in D['identities'] if i['id'] == 'w14') == 'w13'
road_results = []
for r in west['roads']:
    if r['id'] not in ['W-ECON-FRONT', 'W-RESEARCH-EAST', 'W-METRO-EDGE', 'W-METRO-ACCESS', 'W-CANTEEN-BRANCH', 'W-DORM-LINK']:
        continue
    strip = LineString(r['points']).buffer(r['width']/2, cap_style=2, join_style=2)
    missing = strip.difference(surface(west['asphalt'])).area
    assert missing < 1e-7, (r['id'], missing)
    road_results.append(dict(id=r['id'], fullWidth=r['width'], missingArea=missing))
report['repairedRoadWidths'] = road_results
collisions = json.loads((OUT/'道路与落位检查.json').read_text(encoding='utf-8'))
assert not collisions['roadBuildingOverlaps'] and not collisions['buildingOverlaps']
assert all(e['foreignOverlap'] < .01 for e in collisions['entrances'])
(OUT/'布局专项核验.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
