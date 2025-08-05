import json


def geojson_to_svg_path(feature):
    coordinates = feature['geometry']['coordinates']
    svg_paths = []

    for polygon in coordinates:
        path = []

        inner_element = []
        if feature['geometry']['type'] == 'Polygon':
            inner_element = polygon
        elif feature['geometry']['type'] == 'MultiPolygon':
            inner_element = polygon[0]
        else:
            ...

        for i, point in enumerate(inner_element):  # 只取外环坐标
            x, y = point
            if i == 0:
                path.append(f"M {x} {y}")
            else:
                path.append(f"L {x} {y}")
        path.append("Z")  # 闭合路径
        svg_paths.append(" ".join(path))

    return svg_paths


# 读取 GeoJSON 文件
with open('china.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 为每个省份生成 SVG 路径
for feature in data['features']:
    province_name = feature['properties']['name']
    svg_paths = geojson_to_svg_path(feature)

    print(f"// {province_name}")
    for path in svg_paths:
        print(f'SvgShape {{ path: "{path}" }}')
    print()