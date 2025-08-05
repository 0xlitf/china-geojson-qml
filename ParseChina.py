import json
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 加载GeoJSON数据
with open('china.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 基础数据解析
print(f"中国包含 {len(data['features'])} 个省级行政区")
print("\n前5个行政区信息：")
for feature in data['features'][:5]:
    props = feature['properties']
    print(f"{props['name']} (ID: {props['id']}) - 面积指数: {props['size']}")


# 3. 提取特定信息
def get_province_by_name(name):
    for feature in data['features']:
        if feature['properties']['name'] == name:
            return feature
    return None


xinjiang = get_province_by_name("新疆维吾尔自治区")
print(f"\n新疆的坐标点数: {len(xinjiang['geometry']['coordinates'][0])}")


# 4. 地理坐标处理
def calculate_centroid(coords):
    x, y = zip(*coords[0])  # 取第一个多边形
    return sum(x) / len(x), sum(y) / len(y)


beijing = get_province_by_name("北京市")
centroid = calculate_centroid(beijing['geometry']['coordinates'])
print(f"\n北京的地理中心坐标: {centroid}")


# 5. 可视化
def plot_provinces():
    fig, ax = plt.subplots(figsize=(15, 12))
    patches = []

    for feature in data['features']:
        geom = feature['geometry']
        props = feature['properties']

        if geom['type'] == 'Polygon':
            polygon = Polygon(geom['coordinates'][0], closed=True)
            patches.append(polygon)
        elif geom['type'] == 'MultiPolygon':
            for poly in geom['coordinates']:
                polygon = Polygon(poly[0], closed=True)
                patches.append(polygon)

    pc = PatchCollection(patches, alpha=0.4, edgecolor='black')
    ax.add_collection(pc)

    # 标注几个重要城市
    cities = {
        '北京': (116.4551, 40.2539),
        '上海': (121.4648, 31.2891),
        '广州': (113.4668, 23.1152)
    }
    for name, (x, y) in cities.items():
        ax.plot(x, y, 'ro')
        ax.text(x, y, name, fontsize=12)

    ax.set_xlim(70, 140)
    ax.set_ylim(15, 55)
    ax.set_title('中国省级行政区划地图', fontsize=16)
    plt.show()


# 6. 数据分析
size_stats = {
    'max': max(data['features'], key=lambda x: int(x['properties']['size'])),
    'min': min(data['features'], key=lambda x: int(x['properties']['size']))
}

print("\n面积分析:")
print(f"最大面积: {size_stats['max']['properties']['name']} ({size_stats['max']['properties']['size']})")
print(f"最小面积: {size_stats['min']['properties']['name']} ({size_stats['min']['properties']['size']})")

# 7. 输出所有省份列表
print("\n所有省级行政区列表:")
for i, feature in enumerate(data['features'], 1):
    print(f"{i:2d}. {feature['properties']['name']}")

# 执行可视化
plot_provinces()