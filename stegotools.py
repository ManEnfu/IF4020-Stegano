import sys
import util
import rc4
from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
       
        self.media = None
        self.message = b''
        self.result = None
        self.msgascii = True

        self.media_textbox = QtWidgets.QTextEdit(self)
        self.media_textbox.setReadOnly(True)
        self.open_media_button = QtWidgets.QPushButton('Open', self)

        self.message_textbox = QtWidgets.QTextEdit(self)
        self.message_textbox.setReadOnly(True)
        self.open_message_button = QtWidgets.QPushButton('Open', self)

        self.result_label = QtWidgets.QLabel("Result")
        self.result_textbox = QtWidgets.QTextEdit(self)
        self.result_textbox.setReadOnly(True)
        self.save_result_button = QtWidgets.QPushButton('Save', self)
        
        self.key_textbox = QtWidgets.QLineEdit(self)
        self.embed_button = QtWidgets.QPushButton('Embed', self)
        self.extract_button = QtWidgets.QPushButton('Extract', self)
        self.seq_radio = QtWidgets.QRadioButton('Sequential', self)
        self.rand_radio = QtWidgets.QRadioButton('Random', self)
        # self.media_label = QtWidgets.QLabel('Open File...', self)
        # self.message_label = QtWidgets.QLabel('Open File...', self)

        self.setWindowTitle('StegoTools')

        center = QtWidgets.QWidget(self)
        clayout = QtWidgets.QVBoxLayout(self)
        
        media_button_layout = QtWidgets.QVBoxLayout(self)
        message_button_layout = QtWidgets.QVBoxLayout(self)
        result_button_layout = QtWidgets.QVBoxLayout(self)

        embed_layout = QtWidgets.QVBoxLayout(self)
        extract_layout = QtWidgets.QVBoxLayout(self)
        result_layout = QtWidgets.QVBoxLayout(self)

        top_layout = QtWidgets.QHBoxLayout(self)
        bot_layout = QtWidgets.QHBoxLayout(self)

        media_button_layout.addWidget(QtWidgets.QLabel('Media'))
        media_button_layout.addWidget(self.media_textbox)
        media_button_layout.addWidget(self.open_media_button)

        message_button_layout.addWidget(QtWidgets.QLabel('Message'))
        message_button_layout.addWidget(self.message_textbox)
        message_button_layout.addWidget(self.open_message_button)
        
        result_button_layout.addWidget(self.result_label)
        result_button_layout.addWidget(self.result_textbox)
        result_button_layout.addWidget(self.save_result_button)

        top_layout.addLayout(media_button_layout)
        top_layout.addLayout(message_button_layout)
        top_layout.addLayout(result_button_layout)

        # embed_layout.addWidget(QtWidgets.QLabel('Embed'))
        embed_layout.addWidget(QtWidgets.QLabel('Insert Order:'))
        embed_layout.addWidget(self.seq_radio)
        embed_layout.addWidget(self.rand_radio)
        embed_layout.addStretch()
        embed_layout.addWidget(self.embed_button)
        # extract_layout.addWidget(QtWidgets.QLabel('Extract'))
        extract_layout.addStretch()
        extract_layout.addWidget(self.extract_button)
        bot_layout.addLayout(embed_layout)
        bot_layout.addLayout(extract_layout)

        clayout.addLayout(top_layout)
        clayout.addWidget(QtWidgets.QLabel('Encryption Key (Leave blank for no encryption)'))
        clayout.addWidget(self.key_textbox)
        # clayout.addStretch()
        clayout.addLayout(bot_layout)
        
        center.setLayout(clayout)
        self.setCentralWidget(center)
        self.seq_radio.click()

        self.open_media_button.clicked.connect(self.handle_open_media_button)
        self.open_message_button.clicked.connect(self.handle_open_message_button)
        self.save_result_button.clicked.connect(self.handle_save_result_button)

    def handle_open_media_button(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        if filename[0] != '':
            self.media = util.read_file_binary(filename[0])
            self.media_textbox.setText('Raw Binary Data (' + str(len(self.media)) + 'B)')
    
    def handle_open_message_button(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        if filename[0] != '':
            self.message = util.read_file_binary(filename[0])
            self.message_textbox.setText('Raw Binary Data (' + str(len(self.message)) + 'B)')

    def handle_save_result_button(self):
        if self.result != None:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.')
            if filename[0] != '':
                util.write_file_binary(filename[0], self.result)


    def handle_embed_button(self):
        pass

    def handle_extract_button(self):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(None)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
