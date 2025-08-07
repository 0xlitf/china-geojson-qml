import os
import subprocess
from pathlib import Path
from pypinyin import pinyin, Style


# 配置路径
QT_BIN_PATH = r"C:\Qt\6.9.0\msvc2022_64\bin"
SVGTOQML_EXE = os.path.join(QT_BIN_PATH, "svgtoqml.exe")
SVG_SOURCE_DIR = r".\china_province_svg"
QML_TARGET_DIR = r".\china_province_qml"


def hanzi_to_pinyin(filename):
    """将文件名中的汉字转为拼音，保留其他字符"""
    result = []
    for char in filename:
        if '\u4e00' <= char <= '\u9fff':  # 判断是否是汉字
            # 获取拼音首字母（不带声调）
            py = pinyin(char, style=Style.NORMAL, heteronym=False)[0][0]
            py = py.capitalize()
            result.append(py)
        else:
            result.append(char)
    return ''.join(result)


def convert_svg_to_qml(svg_file: Path, relative_path: Path):
    """转换单个SVG文件为QML"""
    # 将路径中的汉字转为拼音
    pinyin_parts = []
    for part in relative_path.parts:
        pinyin_part = hanzi_to_pinyin(part)
        pinyin_parts.append(pinyin_part)
    pinyin_path = Path(*pinyin_parts)

    # 构建目标路径
    qml_file = Path(QML_TARGET_DIR) / pinyin_path.with_suffix('.qml')

    # 确保目标目录存在
    qml_file.parent.mkdir(parents=True, exist_ok=True)

    # 执行转换命令
    cmd = [
        SVGTOQML_EXE,
        str(svg_file),
        str(qml_file)
    ]
    subprocess.run(cmd, check=True)

    print(f"Converted: {svg_file} -> {qml_file}")


def process_directory():
    """处理整个目录树"""
    for root, _, files in os.walk(SVG_SOURCE_DIR):
        for file in files:
            if file.lower().endswith('.svg'):
                svg_path = Path(root) / file
                # 计算相对于源目录的路径
                relative_path = svg_path.relative_to(SVG_SOURCE_DIR)
                convert_svg_to_qml(svg_path, relative_path)


if __name__ == "__main__":
    # 验证工具存在
    if not os.path.exists(SVGTOQML_EXE):
        raise FileNotFoundError(f"svgtoqml.exe not found at {SVGTOQML_EXE}")

    print("Starting SVG to QML conversion...")
    process_directory()
    print("Conversion completed!")