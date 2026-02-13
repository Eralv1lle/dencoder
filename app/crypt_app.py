from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget,
                             QLabel, QPushButton, QTextEdit, QApplication, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt
from sqlalchemy.exc import NoResultFound

from db import get_by_id, Session, engine, create_data
from db.models import Data
from cryptography_service import encrypt, decrypt

import sys


def log_uncaught_exceptions(ex_type, ex_value, ex_traceback):
    err = f"{ex_type.__name__}: {ex_value}"
    print(err)
    QMessageBox.critical(None, "Ошибка", err)

sys.excepthook = log_uncaught_exceptions


class CryptApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Криптография")

        self.resize(1000, 700)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        crypt_layout = QHBoxLayout()

        encrypt_layout = QVBoxLayout()

        label_encrypt = QLabel("Шифровка данных")
        self.text_encrypt = QTextEdit()
        self.text_encrypt.setMaximumHeight(30)
        self.text_encrypt.setText("Введите данные для шифровки")
        self.button_encrypt = QPushButton("Зашифровать")
        self.copy_button = QPushButton("Скопировать шифр")
        self.copy_button.clicked.connect(self.copy_encrypt)
        self.button_encrypt.clicked.connect(self.encrypt_text)
        self.encrypted_label = QLabel("")
        self.encrypted_label.setWordWrap(True)
        self.encrypted_label_id = QLabel("")
        self.encrypted_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.encrypted_label.setWordWrap(True)
        encrypt_layout.addWidget(label_encrypt)
        encrypt_layout.addWidget(self.text_encrypt)
        encrypt_layout.addWidget(self.button_encrypt)
        encrypt_layout.addWidget(self.copy_button)
        encrypt_layout.addWidget(self.encrypted_label)
        encrypt_layout.addWidget(self.encrypted_label_id)

        decrypt_layout = QVBoxLayout()

        label_decrypt = QLabel("Расшифровка данных")
        self.text_decrypt = QTextEdit()
        self.text_decrypt.setMaximumHeight(30)
        self.text_decrypt.setText("Введите зашифрованное сообщение")
        self.id_decrypt = QTextEdit()
        self.id_decrypt.setMaximumHeight(30)
        self.id_decrypt.setText("Введите айди зашифрованного сообщения")
        self.button_decrypt = QPushButton("Расшифровать")
        self.copyd_button = QPushButton("Скопировать расшифровку")
        self.copyd_button.clicked.connect(self.copy_decrypt)
        self.button_decrypt.clicked.connect(self.decrypt_text)
        self.decrypted_label = QLabel("")
        self.decrypted_label.setWordWrap(True)
        self.decrypted_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.encrypted_label.setWordWrap(True)
        decrypt_layout.addWidget(label_decrypt)
        decrypt_layout.addWidget(self.text_decrypt)
        decrypt_layout.addWidget(self.id_decrypt)
        decrypt_layout.addWidget(self.button_decrypt)
        decrypt_layout.addWidget(self.copyd_button)
        decrypt_layout.addWidget(self.decrypted_label)

        crypt_layout.addLayout(encrypt_layout, stretch=1)
        crypt_layout.addLayout(decrypt_layout, stretch=1)

        main_layout.addLayout(crypt_layout)


        get_by_id_layout = QVBoxLayout()
        get_by_id_layout.addSpacing(0)
        get_by_id_label = QLabel("Получить по id")
        self.get_by_id_text = QTextEdit()
        self.get_by_id_text.setMaximumHeight(30)
        self.button_get_by_id = QPushButton("Получить")
        self.button_get_by_id.clicked.connect(self.get_data_by_id)
        self.text_id = QLabel("")
        self.text_salt = QLabel("")
        self.text_encrypted = QLabel("")
        self.text_encrypted.setWordWrap(True)
        self.text_encrypted.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        get_by_id_layout.addWidget(get_by_id_label)
        get_by_id_layout.addWidget(self.get_by_id_text)
        get_by_id_layout.addWidget(self.button_get_by_id)
        get_by_id_layout.addWidget(self.text_id)
        get_by_id_layout.addWidget(self.text_salt)
        get_by_id_layout.addWidget(self.text_encrypted)

        main_layout.addLayout(get_by_id_layout)

        self.logs = QLabel("Логи:")
        main_layout.addWidget(self.logs)

    def encrypt_text(self):
        with Session(engine) as session:
            data = Data()
            create_data(data, session)
            session.flush()
            data.salt = data.id
            data_id = data.id
            text = self.text_encrypt.toPlainText()
            encrypted_text = encrypt(text, data.salt)
            data.encrypted = encrypted_text
            print(encrypted_text)
            self.logs.setText(f"Логи: зашифрованное сообщение под айди {data_id}: {encrypted_text}")
            session.commit()
            session.close()

        n = 44
        result = "\n".join([encrypted_text.decode("utf-8")[i:i+n] for i in range(0, len(str(encrypted_text.decode("utf-8"))), n)])
        self.encrypted_label.setText(result)
        self.encrypted_label_id.setText(f"Под айди: {data_id}")

    def decrypt_text(self):
        text = self.text_decrypt.toPlainText()
        data_id = int(self.id_decrypt.toPlainText())
        print(text, data_id)
        decrypted = decrypt(text, data_id)
        print(decrypted)
        n = 44
        result = "\n".join([decrypted[i:i + n] for i in range(0, len(decrypted), n)])
        self.decrypted_label.setText(result)
        self.logs.setText(f"Логи: расшифровано сообщение под айди {data_id}: {decrypted}")


    def get_data_by_id(self):
        data_id = self.get_by_id_text.toPlainText()
        data = None
        with Session(engine) as session:
            try:
                data = get_by_id(int(data_id), session)
            except NoResultFound:
                self.logs.setText("Логи: ДАННЫХ С ТАКИМ ID НЕ СУЩЕСТВУЕТ")

        if data:
            self.text_id.setText(f"Айди: {data.id}")
            self.text_salt.setText(f"Соль: {data.salt}")
            self.text_encrypted.setText(f"Зашифрованное: {data.encrypted.decode("utf-8")}")
            self.logs.setText(f"Логи: получена дата с айди {data.id}, {repr(data)}")
            print(data)
            print(data.id)
            print(data.salt)
            print(data.encrypted)

    def copy_encrypt(self):
        clip = QApplication.clipboard()
        text = self.encrypted_label.text()
        clip.setText(text)
        self.logs.setText(f'Логи: скопирован в буфер обмена: "{text}"')

    def copy_decrypt(self):
        clip = QApplication.clipboard()
        text = self.decrypted_label.text()
        clip.setText(text)
        self.logs.setText(f'Логи: скопирован в буфер обмена: "{text}"')

def main():
    app = QApplication(sys.argv)

    crypt_app = CryptApp()
    crypt_app.show()

    sys.exit(
        app.exec()
    )

if __name__ == '__main__':
    main()