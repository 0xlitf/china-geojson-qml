import os
import re
from pathlib import Path
import shutil

# 配置路径
QML_SOURCE_DIR = r".\china_province_qml"
QML_TARGET_DIR = r".\china_province_qml_proceed"


def process_qml_file(qml_file: Path):
    """处理单个QML文件，提取PathSvg数据"""
    with open(qml_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则匹配所有PathSvg路径
    pattern = re.compile(r'PathSvg\s*\{\s*path:\s*"([^"]+)"', re.DOTALL)
    matches = pattern.findall(content)

    if not matches:
        print(f"Warning: No PathSvg found in {qml_file}")
        return None

    paths_formatted = "\n        ".join(
        [f'SvgShape {{ name: "path_{index}"; path: "{path}" }}' for index, path in enumerate(matches, start=1)]
    )
    new_content = """
import QtQuick
import QtQuick.Shapes
import ".."
// import controls

Item {
    Rectangle {
        id: backgroundRect
        // color: "#333333"
        color: "transparent"

        anchors.centerIn: parent
        width: {
            if (parent.height / parent.width > 6/8) {
                return parent.width
            } else {
                return parent.height * 8 / 6
            }
        }
        height: width * (6/8)  // 固定比例

        Item {
            id: svg
            // anchors.centerIn: parent

            property var scale_: Math.min(parent.width / 800, parent.height / 600)
            onScale_Changed: {
                console.log("onScale_Changed: ", parent.width / 800, parent.height / 600, scale_)
            }
            transform: [
                Scale { xScale: svg.scale_; yScale: svg.scale_ }
            ]
            // height: parent.height - 50
            // width: parent.width - 50
    """ + f"""// Processed from {qml_file.name}

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