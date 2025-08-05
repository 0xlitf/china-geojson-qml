import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 1024
    height: 768
    title: qsTr("PySide6 QML Application")

    Component.onCompleted: {
        console.log("Application initialized")
    }
}