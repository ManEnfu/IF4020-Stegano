from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.open_media_button = QtWidgets.QPushButton('Open', self)
        self.save_media_button = QtWidgets.QPushButton('Save', self)
        self.media_label = QtWidgets.QLabel('Open File...', self)
        self.open_message_button = QtWidgets.QPushButton('Open', self)
        self.save_message_button = QtWidgets.QPushButton('Save', self)
        self.message_label = QtWidgets.QLabel('Open File...', self)
        self.key_textbox = QtWidgets.QLineEdit(self)
        self.embed_button = QtWidgets.QPushButton('Embed', self)
        self.extract_button = QtWidgets.QPushButton('Extract', self)
        self.seq_radio = QtWidgets.QRadioButton('Sequential', self)
        self.rand_radio = QtWidgets.QRadioButton('Random', self)

        self.setWindowTitle('StegoTools')

        center = QtWidgets.QWidget(self)
        clayout = QtWidgets.QVBoxLayout(self)
        media_button_layout = QtWidgets.QVBoxLayout(self)
        message_button_layout = QtWidgets.QVBoxLayout(self)
        embed_layout = QtWidgets.QVBoxLayout(self)
        extract_layout = QtWidgets.QVBoxLayout(self)
        top_layout = QtWidgets.QHBoxLayout(self)
        bot_layout = QtWidgets.QHBoxLayout(self)

        media_button_layout.addWidget(QtWidgets.QLabel('Media'))
        media_button_layout.addWidget(self.media_label)
        media_button_layout.addWidget(self.open_media_button)
        media_button_layout.addWidget(self.save_media_button)
        message_button_layout.addWidget(QtWidgets.QLabel('Message'))
        message_button_layout.addWidget(self.message_label)
        message_button_layout.addWidget(self.open_message_button)
        message_button_layout.addWidget(self.save_message_button)
        top_layout.addLayout(media_button_layout)
        top_layout.addLayout(message_button_layout)

        embed_layout.addWidget(QtWidgets.QLabel('Embed'))
        embed_layout.addWidget(QtWidgets.QLabel('Insert Order:'))
        embed_layout.addWidget(self.seq_radio)
        embed_layout.addWidget(self.rand_radio)
        embed_layout.addWidget(self.embed_button)
        extract_layout.addWidget(QtWidgets.QLabel('Extract'))
        extract_layout.addStretch()
        extract_layout.addWidget(self.extract_button)
        bot_layout.addLayout(embed_layout)
        bot_layout.addLayout(extract_layout)

        clayout.addLayout(top_layout)
        clayout.addWidget(QtWidgets.QLabel('Encryption Key (Leave blank for no encryption)'))
        clayout.addWidget(self.key_textbox)
        clayout.addStretch()
        clayout.addLayout(bot_layout)
        
        center.setLayout(clayout)
        self.setCentralWidget(center)
