import json


x_min = 180
x_max = -180
y_min = 90
y_max = -90


def calculate_box(feature):
    global x_min, x_max, y_min, y_max
    coordinates = feature['geometry']['coordinates']

    for polygon in coordinates:
        inner_element = []
        if feature['geometry']['type'] == 'Polygon':
            inner_element = polygon
        elif feature['geometry']['type'] == 'MultiPolygon':
            inner_element = polygon[0]
        else:
            ...

        for i, point in enumerate(inner_element):  # 只取外环坐标
            x, y = point

            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

    # print(x_min, x_max, y_min, y_max)


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
        # path.append("Z")  # 闭合路径
        svg_paths.append(" ".join(path))

    return svg_paths


# 读取 GeoJSON 文件
# ./geometryCouties/110100.json
# china.json
with open('./geometryCouties/110100.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for feature in data['features']:
    calculate_box(feature)

print(x_min, x_max, y_min, y_max)  # 73.4766 135.0879 18.1055 53.5693

# 为每个省份生成 SVG 路径
for feature in data['features']:
    province_name = feature['properties']['name']
    svg_paths = geojson_to_svg_path(feature)

    print(f"// {province_name}")
    for path in svg_paths:
        print(f'SvgShape {{ name: "{province_name}"; path: "{path}" }}')
    print()
