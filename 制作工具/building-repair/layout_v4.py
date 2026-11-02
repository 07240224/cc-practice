"""Explicit reference-based local corrections; no nearest-road layout inference."""
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union


def apply_layout(data, reference, part, world, rings):
    models = {m['id']: m for m in data['models']}
    west = data['maps']['wuchuan']
    east = data['maps']['guoding']
    roads = {r['id']: r for r in west['roads']}

    def road(id, points, width=7, name=None):
        return dict(id=id, points=points, width=width, map='wuchuan',
                    name=name or id, basis='初始校园图与用户蓝黄批注：保留真实转折与分支')

    roads['W1']['points'] = [[230, 687], [390, 625], [542, 560], [694, 480]]
    roads['W4']['points'] = [[694, 480], [689, 501], [691, 516], [702, 537], [736, 619], [770, 696], [791, 716]]
    roads['W-ECON-FRONT'] = road('W-ECON-FRONT', [[694, 480], [724, 477], [739, 469], [752, 455], [757, 443]], name='经济学院南侧转折道路')
    roads['W-RESEARCH-EAST'] = road('W-RESEARCH-EAST', [[757, 443], [747, 422], [734, 397], [725, 383]], name='高等研究院东侧边路')
    roads['W-METRO-EDGE'] = road('W-METRO-EDGE', [[757, 443], [764, 438], [850, 390], [858, 388.5], [865, 387]], name='裁区南缘至地铁站边路')
    roads['W-CANTEEN-BRANCH'] = road('W-CANTEEN-BRANCH', [[739, 469], [745, 484], [757, 511], [757, 521]], width=6, name='第四食堂西侧与宿舍分支')
    roads['W-DORM-LINK'] = road('W-DORM-LINK', [[691, 516], [705, 536], [757, 521]], width=6, name='连体宿舍北侧接路')
    roads['W-METRO-ACCESS'] = road('W-METRO-ACCESS', [[865, 387], [872, 385.5]], width=5, name='黄圈地铁站口前场')
    west['roads'] = list(roads.values())

    # Remove the whole marked park, while keeping the complete widths of its edge roads.
    original_west = unary_union([Polygon(r['outer'], r.get('holes', [])) for r in west['site']])
    park = Polygon([[722, 330], [882, 330], [882, 345], [860, 351], [870, 373],
                    [868, 380], [858, 382], [759, 433], [754, 434], [750, 430],
                    [738, 406], [725, 380]])
    retained = unary_union([LineString(roads[id]['points']).buffer(roads[id]['width']/2 + 1.6, cap_style=1, join_style=2, quad_segs=8)
                           for id in ['W-RESEARCH-EAST', 'W-METRO-EDGE', 'W-METRO-ACCESS']])
    station_pad = Point(872, 382).buffer(8, quad_segs=8).intersection(original_west)
    cut = original_west.intersection(park).difference(retained.union(station_pad))
    playable_west = original_west.difference(cut)
    assert playable_west.geom_type == 'Polygon'
    west['site'] = rings(playable_west)
    west['campusWallSegments'] = [list(g.coords) for g in _lines(original_west.boundary.intersection(playable_west.buffer(.005)))]
    west['mapCuts'] = [dict(id='USER-BLUE-PARK', name='蓝圈北侧绿地：退出可玩地图', polygons=rings(cut))]
    west['protectedRoadCorridors'] = rings(retained)

    # One six-storey stepped building, with two identities and two separate doors.
    joined = models['w13']
    joined.update(label='21、22号连体楼', center=[804, 510], rotation=25, width=78, depth=24,
                  height=22.2, parts=[part(-19, -1, 40, 18, 6, 'dorm', 'hip'),
                                      part(18, 5.5, 38, 17, 6, 'dorm', 'hip')],
                  entryLocal=[18, 17], entryFace=14, sourceFootprint='C081',
                  joinedIdentities=['w14', 'w13'], placementShift=[0, 0])
    joined['entries'] = [dict(id='w14', x=-19, z=8, porch='glass'), dict(id='w13', x=18, z=14, porch='glass')]
    joined['entry'] = world(joined, 18, 17)
    data['models'] = [m for m in data['models'] if m['id'] != 'w14']
    for identity in data['identities']:
        if identity['id'] == 'w14':
            identity['model'] = 'w13'
    station = dict(id='metro_station', lot='W-METRO', label='地铁站口', map='wuchuan', kind='metro',
                   center=[872, 379], rotation=0, width=10, depth=8, height=4.4,
                   parts=[part(0, -.45, 8.7, 6, 1, 'gray', h=.9)],
                   entryLocal=[0, 6.5], entryFace=2, entry=[872, 385.5],
                   detail='context', basis='本轮用户黄圈落点；原红校界内、蓝色剔除区外')
    data['models'].append(station)
    data['identities'].append(dict(id='metro_station', model='metro_station'))

    # The research-side projection is a boundary error, not a building wing.
    original_east = unary_union([Polygon(r['outer'], r.get('holes', [])) for r in east['site']])
    tip = Polygon([[1340, 645], [1362, 680], [1339, 672], [1332, 649]])
    playable_east = original_east.difference(tip)
    east['site'] = rings(playable_east)
    east['mapCuts'] = [dict(id='RESEARCH-SPUR', name='科研楼南侧多余凸地', polygons=rings(original_east.intersection(tip)))]
    east_roads = {r['id']: r for r in east['roads']}
    del east_roads['G20R']
    east_roads['G3']['points'] = [[1220, 291], [1220, 439], [1210, 489], [1257, 525], [1310, 573]]
    east_roads['G16']['points'] = [[1310, 573], [1363, 550], [1370, 559], [1451, 562], [1600, 562]]
    east_roads['G17R']['points'] = [[1363, 489], [1363, 550]]
    east_roads['G18R']['points'] = [[1310, 573], [1324, 588], [1339, 615], [1439, 615]]
    east['roads'] = list(east_roads.values())
    for space in data['spaces']:
        if space['id'] == 'G-LAWN':
            space['polygon'] = [[1162, 551], [1212, 503], [1292, 571], [1190, 618]]
    for mp in data['maps'].values():
        site = unary_union([Polygon(r['outer'], r.get('holes', [])) for r in mp['site']])
        mp['bounds'] = list(site.bounds)
    data['layoutRevision'] = 'V4：蓝黄批注、连体21/22、科研南界和真实折线道路'


def _lines(geometry):
    if geometry.is_empty:
        return []
    if geometry.geom_type == 'LineString':
        return [geometry]
    return [line for item in geometry.geoms for line in _lines(item)]
