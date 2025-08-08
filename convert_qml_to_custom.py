import os
import re
from pathlib import Path
import shutil

# 配置路径
QML_SOURCE_DIR = r".\china_province_svg2qml"
QML_TARGET_DIR = r".\china_province_svg2qml_converted"


def process_qml_file(qml_file: Path):
    """处理单个QML文件，提取PathSvg数据"""
    with open(qml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    width_match = re.search(r'implicitWidth\s*:\s*(\d+)', content)
    height_match = re.search(r'implicitHeight\s*:\s*(\d+)', content)

    pattern = re.compile(r'PathSvg\s*\{\s*path:\s*"([^"]+)"', re.DOTALL)
    matches = pattern.findall(content)

    if not matches:
        print(f"Warning: No PathSvg found in {qml_file}")
        return None

    paths_formatted = "\n            ".join(
        [f'SvgShape {{ onBlockClicked: {{console.info(name," clicked");}} name: "path_{index}"; path: "{path}" }}' for index, path in enumerate(matches, start=0)]
    )
    new_content = """
import QtQuick
import QtQuick.Shapes
// import controls
import ".."

Item {
    Rectangle {
        id: backgroundRect
        // color: "#333333"
        color: "transparent"
""" + f"""
        property var convertWidth: {width_match.group(1)}
        property var convertHeight: {height_match.group(1)}
""" + """
        anchors.centerIn: parent
        width: {
            if (parent.height / parent.width > convertHeight/convertWidth) {
                return parent.width
            } else {
                return parent.height * convertWidth / convertHeight
            }
        }
        height: width * (convertHeight/convertWidth)  // 固定比例

        Item {
            id: svg
            // anchors.centerIn: parent

            property var scale_: Math.min(parent.width / parent.convertWidth, parent.height / parent.convertHeight)
            onScale_Changed: {
                console.log("onScale_Changed: ", parent.width / parent.convertWidth, parent.height / parent.convertHeight, scale_)
            }
            transform: [
                Scale { xScale: svg.scale_; yScale: svg.scale_ }
            ]
    """ + f"""
            // Processed from {qml_file.name}

            {paths_formatted}
    """ + """
        }
    }
}
"""
    return new_content


def process_directory():
    """处理整个目录树"""
    # 清空并创建目标目录
    if os.path.exists(QML_TARGET_DIR):
        shutil.rmtree(QML_TARGET_DIR)
    os.makedirs(QML_TARGET_DIR)

    for root, _, files in os.walk(QML_SOURCE_DIR):
        for file in files:
            if file.endswith('.qml'):
                qml_path = Path(root) / file
                relative_path = qml_path.relative_to(QML_SOURCE_DIR)

                # 处理文件
                processed_content = process_qml_file(qml_path)
                if processed_content is None:
                    continue

                # 写入新文件
                target_path = Path(QML_TARGET_DIR) / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)

                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(processed_content)

                print(f"Processed: {qml_path} -> {target_path}")


if __name__ == "__main__":
    print("Starting QML processing...")
    process_directory()
    print("Processing completed!")