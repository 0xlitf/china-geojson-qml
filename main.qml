import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "./china_province_svg2qml_converted/" as Provinces
import "."

ApplicationWindow {
    id: root
    visible: true
    width: 1024
    height: 768
    title: qsTr("PySide6 QML Application")

    Provinces.ZhongGuo {
        anchors.centerIn: parent
        width: 1000
        height: 1000
    }

    Component.onCompleted: {
        console.log("Application initialized")
    }
}