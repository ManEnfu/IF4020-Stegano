import sys
import util
import rc4
import staudio
import stimage
from PyQt5 import QtCore, QtWidgets

images_format = ['png', 'bmp']
audio_format = ['wav']

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
       
        self.media = None
        self.mediaFname = ""
        self.mediaPath = ""
        self.message = None
        self.messageFname = ""
        self.messagePath = ""
        self.result = None
        self.result_format = ""

        self.media_textbox = QtWidgets.QTextEdit(self)
        self.media_textbox.setReadOnly(True)
        self.open_media_button = QtWidgets.QPushButton('Open File', self)

        self.message_textbox = QtWidgets.QTextEdit(self)
        self.message_textbox.setReadOnly(True)
        self.open_message_button = QtWidgets.QPushButton('Open File', self)

        self.result_label = QtWidgets.QLabel("Result")
        self.result_textbox = QtWidgets.QTextEdit(self)
        self.result_textbox.setReadOnly(True)
        self.save_result_button = QtWidgets.QPushButton('Save Result', self)
        
        self.key_textbox = QtWidgets.QLineEdit(self)
        self.embed_button = QtWidgets.QPushButton('Embed', self)
        self.extract_button = QtWidgets.QPushButton('Extract', self)
        self.seq_radio = QtWidgets.QRadioButton('Sequential', self)
        self.rand_radio = QtWidgets.QRadioButton('Random', self)
        self.reset_button = QtWidgets.QPushButton('Clear', self)
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
        clear_layout = QtWidgets.QVBoxLayout(self)

        top_layout = QtWidgets.QHBoxLayout(self)
        bot_layout = QtWidgets.QHBoxLayout(self)
        footer_layout = QtWidgets.QHBoxLayout(self)

        media_button_layout.addWidget(QtWidgets.QLabel('Media'))
        media_button_layout.addWidget(self.media_textbox)
        media_button_layout.addWidget(self.open_media_button)

        message_button_layout.addWidget(QtWidgets.QLabel('Message'))
        message_button_layout.addWidget(self.message_textbox)
        message_button_layout.addWidget(self.open_message_button)
        
        result_button_layout.addWidget(self.result_label)
        result_button_layout.addWidget(self.result_textbox)
        result_button_layout.addWidget(self.save_result_button)

        clear_layout.addWidget(self.reset_button)

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

        footer_layout.addLayout(clear_layout)

        clayout.addLayout(top_layout)
        clayout.addWidget(QtWidgets.QLabel('Encryption Key (Leave blank for no encryption)'))
        clayout.addWidget(self.key_textbox)
        # clayout.addStretch()
        clayout.addLayout(bot_layout)
        clayout.addLayout(footer_layout)
        
        center.setLayout(clayout)
        self.setCentralWidget(center)
        self.seq_radio.click()

        self.open_media_button.clicked.connect(self.handle_open_media_button)
        self.open_message_button.clicked.connect(self.handle_open_message_button)
        self.save_result_button.clicked.connect(self.handle_save_result_button)
        self.embed_button.clicked.connect(self.handle_embed_button)
        self.extract_button.clicked.connect(self.handle_extract_button)
        self.reset_button.clicked.connect(self.handle_reset)

    def handle_reset(self):
        self.media = None
        self.mediaFname = ""
        self.mediaPath = ""
        self.message = None
        self.messageFname = ""
        self.messagePath = ""
        self.result = None
        self.result_format = ""
        self.media_textbox.setText("")
        self.message_textbox.setText("")
        self.result_textbox.setText("")
        self.key_textbox.setText("")
        self.seq_radio.click()

    def handle_open_media_button(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', 'Image or Audio Files (*.bmp *.png *.wav)')
        if filename[0] != '':
            dirs = filename[0].split('/')
            self.mediaFname = dirs[len(dirs) - 1]
            self.mediaPath = filename[0]
            self.media = util.read_file_binary(filename[0])
            self.media_textbox.setText('{} ({} Bytes)'.format(self.mediaFname, len(self.media)))
    
    def handle_open_message_button(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', "")
        if filename[0] != '':
            dirs = str(filename[0]).split('/')
            self.messagePath = filename[0]
            self.messageFname = dirs[len(dirs) - 1]
            self.message = util.read_file_binary(filename[0])
            self.message_textbox.setText('{} ({} Bytes)'.format(self.messageFname, len(self.message)))

    def handle_save_result_button(self):
        if self.result != None:
            placeholder = ""
            if self.result_format in audio_format:
                placeholder = "Audio Files (*.{})".format(self.result_format)
            elif self.result_format in images_format:
                placeholder = "Image Files (*.{})".format(self.result_format)
            else:
                placeholder = ""

            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.', placeholder)
            if filename[0] != '':
                if type(self.result) is bytes:
                    util.write_file_binary(filename[0], self.result)
                else:
                    self.result.write(filename[0])
    
    def extract_format(self, fname):
        splitted = fname.split('.')
        if len(splitted) > 1:
            return splitted[1]
        return None

    def handle_embed_button(self):
        if self.message == None or self.media == None: 
            return
        
        stego_content = self.message
        if self.key_textbox.text() != '':
            stego_content = rc4.moencrypt(self.message, self.key_textbox.text())

        self.result_format = self.extract_format(self.mediaFname)
        isRandom = self.rand_radio.isChecked()
        if self.result_format in audio_format:
            res = staudio.embedMessage(self.mediaPath, stego_content, isRandom)
            self.result = res
            self.result_label = "Stego Audio File"
        else:
            res = stimage.embedMessage(self.mediaPath, stego_content, isRandom)
            self.result = res
            self.result_label = "Stego Image File"

        self.result_textbox.setText("{}_stego.{}".format(self.mediaFname.split('.')[0], self.result_format))
    
    def handle_extract_button(self):
        if self.media == None:
            return
        self.result_format = ""
        mediaFormat = self.extract_format(self.mediaFname)
        self.result_label = "Extracted message"
        if mediaFormat in audio_format:
            self.result = staudio.extractMessage(self.mediaPath)
        else:
            self.result = stimage.extractMessage(self.mediaPath)
        
        if self.key_textbox.text() != '':
            self.result = rc4.modecrypt(self.result, self.key_textbox.text())
        
        self.result_textbox.setText("Binary File Extracted from {}".format(self.mediaFname))
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(None)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
