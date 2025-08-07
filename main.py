import sys
import os
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Slot, Signal


class Backend(QObject):
    """
    Python 后端逻辑，通过信号槽与 QML 交互
    """
    dataChanged = Signal(str)  # 定义信号

    def __init__(self):
        super().__init__()
        self._data = "Initial data"

    @Slot(result=str)
    def getData(self):
        """ QML 可调用的方法 """
        return self._data

    @Slot(str)
    def setData(self, value):
        """ QML 可调用的方法 """
        self._data = value
        self.dataChanged.emit(value)  # 触发信号


def main():
    # 创建应用实例
    app = QGuiApplication(sys.argv)

    # 创建 QML 引擎
    engine = QQmlApplicationEngine()

    # 获取 QML 文件绝对路径
    qml_file = Path(__file__).parent / "main.qml"
    # qml_file = Path(__file__).parent / "china_province_qml" / "zhongguo.qml"
    print(qml_file)
    qml_url = QUrl.fromLocalFile(os.fspath(qml_file.resolve()))
    print(qml_url)

    # 注册 Python 后端
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    # 加载 QML 文件
    engine.load(qml_url)

    # 检查 QML 是否加载成功
    # if not engine.rootObjects():
    #     sys.exit(-1)

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
