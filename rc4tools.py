#!/usr/bin/python

import sys
import util
import rc4
from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.plaintext = b''
        self.ciphertext = b''
        self.plainascii = True
        self.cipherascii = True
        self.open_plain_button = QtWidgets.QPushButton('Open', self)
        self.save_plain_button = QtWidgets.QPushButton('Save', self)
        self.plain_textbox = QtWidgets.QTextEdit(self)
        self.open_cipher_button = QtWidgets.QPushButton('Open', self)
        self.save_cipher_button = QtWidgets.QPushButton('Save', self)
        self.cipher_textbox = QtWidgets.QTextEdit(self)
        self.key_textbox = QtWidgets.QLineEdit(self)
        self.encrypt_button = QtWidgets.QPushButton('Encrypt', self)
        self.decrypt_button = QtWidgets.QPushButton('Decrypt', self)
        # self.seq_radio = QtWidgets.QRadioButton('Sequential', self)
        # self.rand_radio = QtWidgets.QRadioButton('Random', self)

        self.setWindowTitle('RC4Tools')

        center = QtWidgets.QWidget(self)
        clayout = QtWidgets.QVBoxLayout(self)
        plain_button_layout = QtWidgets.QVBoxLayout(self)
        cipher_button_layout = QtWidgets.QVBoxLayout(self)
        encrypt_layout = QtWidgets.QVBoxLayout(self)
        decrypt_layout = QtWidgets.QVBoxLayout(self)
        top_layout = QtWidgets.QHBoxLayout(self)
        bot_layout = QtWidgets.QHBoxLayout(self)

        plain_button_layout.addWidget(QtWidgets.QLabel('Plaintext'))
        plain_button_layout.addWidget(self.plain_textbox)
        plain_button_layout.addWidget(self.open_plain_button)
        plain_button_layout.addWidget(self.save_plain_button)
        cipher_button_layout.addWidget(QtWidgets.QLabel('Ciphertext'))
        cipher_button_layout.addWidget(self.cipher_textbox)
        cipher_button_layout.addWidget(self.open_cipher_button)
        cipher_button_layout.addWidget(self.save_cipher_button)
        top_layout.addLayout(plain_button_layout)
        top_layout.addLayout(cipher_button_layout)

        encrypt_layout.addWidget(self.encrypt_button)
        decrypt_layout.addWidget(self.decrypt_button)
        bot_layout.addLayout(encrypt_layout)
        bot_layout.addLayout(decrypt_layout)

        clayout.addLayout(top_layout)
        clayout.addWidget(QtWidgets.QLabel('Encryption Key'))
        clayout.addWidget(self.key_textbox)
        clayout.addLayout(bot_layout)
        
        center.setLayout(clayout)
        self.setCentralWidget(center)

        self.open_plain_button.clicked.connect(self.handle_open_plain_button)
        self.save_plain_button.clicked.connect(self.handle_save_plain_button)
        self.open_cipher_button.clicked.connect(self.handle_open_cipher_button)
        self.save_cipher_button.clicked.connect(self.handle_save_cipher_button)
        self.encrypt_button.clicked.connect(self.handle_encrypt_button)
        self.decrypt_button.clicked.connect(self.handle_decrypt_button)

    def handle_open_plain_button(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        if filename[0] != '':
            self.plaintext = util.read_file_binary(filename[0])
            self.plainascii = self.plaintext.isascii()
            if self.plainascii:
                self.plain_textbox.setReadOnly(False)
                self.plain_textbox.setText(self.plaintext.decode())
            else:
                self.plain_textbox.setReadOnly(True)
                self.plain_textbox.setText(
                    'Raw Binary Data (' + str(len(self.plaintext)) + 'B)')

    def handle_save_plain_button(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.')
        if filename[0] != '':
            if self.plainascii:
                self.plaintext = bytes(self.plain_textbox.toPlainText(), 
                    encoding='utf-8')
            util.write_file_binary(filename[0], self.plaintext) 

    def handle_open_cipher_button(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')
        if filename[0] != '':
            self.ciphertext = util.read_file_binary(filename[0])
            self.cipherascii = self.ciphertext.isascii()
            if self.cipherascii:
                self.cipher_textbox.setReadOnly(False)
                self.cipher_textbox.setText(self.ciphertext.decode())
            else:
                self.cipher_textbox.setReadOnly(True)
                self.cipher_textbox.setText(
                    'Raw Binary Data (' + str(len(self.ciphertext)) + 'B)')

    def handle_save_cipher_button(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.')
        if filename[0] != '':
            if self.cipherascii:
                self.ciphertext = bytes(self.cipher_textbox.toPlainText(),
                    encoding='utf-8')
            util.write_file_binary(filename[0], self.ciphertext) 

    def handle_encrypt_button(self):
        if self.plainascii:
            self.plaintext = bytes(self.plain_textbox.toPlainText(), 
                encoding='utf-8')
        K = bytes(self.key_textbox.text(), encoding='utf-8')
        self.ciphertext = rc4.moencrypt(self.plaintext, K)
        self.cipherascii = self.ciphertext.isascii()
        if self.cipherascii:
            self.cipher_textbox.setReadOnly(False)
            self.cipher_textbox.setText(self.ciphertext.decode())
        else:
            self.cipher_textbox.setReadOnly(True)
            self.cipher_textbox.setText(
                'Raw Binary Data (' + str(len(self.ciphertext)) + 'B)')
        
    def handle_decrypt_button(self):
        if self.cipherascii:
            self.ciphertext = bytes(self.cipher_textbox.toPlainText(),
                encoding='utf-8')
        K = bytes(self.key_textbox.text(), encoding='utf-8')
        self.plaintext = rc4.modecrypt(self.ciphertext, K)
        self.plainascii = self.plaintext.isascii()
        if self.plainascii:
            self.plain_textbox.setReadOnly(False)
            self.plain_textbox.setText(self.plaintext.decode())
        else:
            self.plain_textbox.setReadOnly(True)
            self.plain_textbox.setText(
                'Raw Binary Data (' + str(len(self.plaintext)) + 'B)')
        
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(None)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
