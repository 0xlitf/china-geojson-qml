// SvgShape.qml
import QtQuick 2.15
import QtQuick.Shapes 1.15

Shape {
    id: root

    // 暴露给外部的属性
    property string path: ""          // SVG 路径数据
    property color fillColor: "#ff53D6FF"  // 默认填充色
    property color hoverColor: "#ff00C2FF" // 悬停时的填充色
    property color strokeColor: "white"    // 边框颜色
    property real strokeWidth: 1            // 边框宽度

    // 内部逻辑
    containsMode: Shape.FillContains

    HoverHandler {
        id: hoverHandler
    }

    TapHandler {
        onTapped: console.info("Shape clicked")
    }

    ShapePath {
        id: shapePath
        strokeColor: root.strokeColor
        strokeWidth: root.strokeWidth
        capStyle: ShapePath.FlatCap
        joinStyle: ShapePath.MiterJoin
        miterLimit: 4
        fillColor: hoverHandler.hovered ? root.hoverColor : root.fillColor
        fillRule: ShapePath.WindingFill
        PathSvg {
            path: root.path  // 绑定到外部传入的 path
        }
    }
}