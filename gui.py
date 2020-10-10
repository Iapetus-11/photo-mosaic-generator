from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class BaseWindow(QWidget):
    def __init__(self, app):
        QWidget.__init__(self)

        self.app = app
        self.app_palette = QPalette()

        self.title = 'Window Title'

        # window positioning
        self.left = 50
        self.top = 50

        # window dimensions
        self.width = 300
        self.height = 10

    def init_theme(self):
        self.app.setStyle('Fusion')

        self.app_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.app_palette.setColor(QPalette.WindowText, Qt.white)
        self.app_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.app_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.app_palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.app_palette.setColor(QPalette.ToolTipText, Qt.white)
        self.app_palette.setColor(QPalette.Text, Qt.white)
        self.app_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.app_palette.setColor(QPalette.ButtonText, Qt.white)
        self.app_palette.setColor(QPalette.BrightText, Qt.red)
        self.app_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.app_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.app_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.app.setPalette(self.app_palette)

        self.app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)

    def init_layout(self):
        pass


class NewPaletteWindow(BaseWindow):
    def __init__(self, app):
        BaseWindow.__init__(self, app)

        self.title = 'Generate new Palette'

        self.init_theme()
        self.init_layout()

    def init_layout():
        self.layout = QVBoxLayout()
        self.sub_layouts = (QHBoxLayout(), QHBoxLayout(), QHBoxLayout(),)

        self.source_folder_label = QLabel('Source Folder: None Chosen')
        self.sub_layouts[0].addWidget(self.source_folder_label)

        self.source_count_label = QLabel('File Count (50+ Recommended): None')
        self.sub_layouts[1].addWidget(self.source_count_label)

        self.choose_folder_button = QPushButton('Choose Folder')
        self.choose_folder_button.clicked.connect(lambda: self.connect_choose_folder())
        self.sub_layouts[2].addWidget(self.choose_folder_button)

        self.show_button = QPushButton('Generate Palette')
        self.show_button.clicked.connect(lambda: self.connect_generate_pal())
        self.sub_layouts[3].addWidget(self.show_button)

    def connect_choose_folder(self):
        pass

    def connect_generate_pal(self):
        pass


class MainApp(BaseWindow):
    def __init__(self, app):
        BaseWindow.__init__(self, app)

        self.title = 'Image Mosaic Generator'

        self.init_theme()
        self.init_layout()

    def init_layout(self):
        self.layout = QVBoxLayout()
        self.sub_layouts = (QHBoxLayout(), QHBoxLayout(),)

        self.gen_pal_button = QPushButton('Generate Palette')
        self.gen_pal_button.clicked.connect(lambda: self.connect_gen_new_pal())
        self.sub_layouts[0].addWidget(self.gen_pal_button)

        self.use_pre_button = QPushButton('Use Preexisting')
        self.use_pre_button.clicked.connect(lambda: self.connect_show_button())
        self.sub_layouts[1].addWidget(self.use_pre_button)

        for sub_layout in self.sub_layouts:
            self.layout.addLayout(sub_layout)

        self.setLayout(self.layout)
        self.show()

    def connect_gen_new_pal(self):
        pass

    def connect_use_pre_pal(self):
        pass


if __name__ == '__main__':
    main = QApplication([])

    app = MainApp(main)

    main.exec()
