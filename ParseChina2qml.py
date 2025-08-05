import json


x_min = 73.4766
x_max = 135.0879
y_min = 18.1055
y_max = 53.5693


def geojson_to_svg_path(feature):
    global x_min, x_max, y_min, y_max

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

            x = x - x_min
            y = y_max - y
            x *= 800 / (x_max - x_min)
            y *= 600 / (y_max - y_min)
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

print(x_min, x_max, y_min, y_max)  # 73.4766 96.416 34.3213 49.1748